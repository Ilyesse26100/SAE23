import pymysql
import datetime


def db_connect():
    return pymysql.connect(host='localhost', user='root', password='', db='RealMadridDB', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

def get_equipes_data():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT equipe_id, nom, stade, entraineur FROM Equipes WHERE nom = %s"
            cursor.execute(sql, ('Real Madrid CF',))
            return cursor.fetchall()
    finally:
        conn.close()

def get_equipes_sans_realmadrid():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Modification de la requête pour exclure le Real Madrid
            sql = "SELECT equipe_id, nom, stade, entraineur FROM Equipes WHERE nom != %s"
            cursor.execute(sql, ('Real Madrid CF',))
            return cursor.fetchall()
    finally:
        conn.close()

def get_paris():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Requête SQL pour récupérer les informations des paris avec les noms des équipes domicile et extérieur
            sql = """
            SELECT p.paris_id, s.nom AS supporteur_nom, 
                   e1.nom AS equipe_domicile, e2.nom AS equipe_exterieur, 
                   p.match_id, p.mise, p.Resultat_prédit
            FROM Paris p
            JOIN Supporteurs s ON p.supporteur_id = s.supporteur_id
            JOIN Matches m ON p.match_id = m.match_id
            JOIN Equipes e1 ON m.equipe_domicile_id = e1.equipe_id
            JOIN Equipes e2 ON m.equipe_exterieur_id = e2.equipe_id
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Erreur lors de la récupération des paris: {e}")
    finally:
        conn.close()


def get_upcoming_matches():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Sélectionner les matchs à venir (ceux avec un résultat contenant '?')
            sql = """
            SELECT m.match_id, m.date, 
                   e1.nom AS equipe_domicile, 
                   e2.nom AS equipe_exterieur
            FROM Matches m
            JOIN Equipes e1 ON m.equipe_domicile_id = e1.equipe_id
            JOIN Equipes e2 ON m.equipe_exterieur_id = e2.equipe_id
            WHERE m.Resultat LIKE '%?%'
            ORDER BY m.date ASC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs à venir: {e}")
    finally:
        conn.close()


def get_past_matches():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Requête pour obtenir les matchs passés avec jointures pour récupérer les noms des équipes
            sql = """
            SELECT m.match_id, m.date, ed.nom AS equipe_domicile, ee.nom AS equipe_exterieur, m.resultat
            FROM Matches m
            JOIN Equipes ed ON m.equipe_domicile_id = ed.equipe_id
            JOIN Equipes ee ON m.equipe_exterieur_id = ee.equipe_id
            WHERE m.resultat NOT LIKE '%?%'
            ORDER BY m.date DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            print("Past Matches:", results)  # Debugging statement
            return results
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs passés: {e}")
        return []
    finally:
        conn.close()

def get_joueurs_par_equipe(equipe_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT joueur_id, nom, prenom, poste
            FROM Joueurs
            WHERE equipe_id = %s
            """
            cursor.execute(sql, (equipe_id,))
            joueurs = cursor.fetchall()
            return joueurs
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la récupération des joueurs: {e}")
    finally:
        conn.close()



def get_victoires_defaites_nuls_par_equipe():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT 
                e.equipe_id, e.nom, e.stade, e.entraineur,
                SUM(CASE WHEN m.Resultat IS NOT NULL AND m.Resultat != '?' AND CAST(SUBSTRING_INDEX(m.Resultat, '-', 1) AS UNSIGNED) > CAST(SUBSTRING_INDEX(m.Resultat, '-', -1) AS UNSIGNED) AND m.equipe_domicile_id = e.equipe_id THEN 1 ELSE 0 END) +
                SUM(CASE WHEN m.Resultat IS NOT NULL AND m.Resultat != '?' AND CAST(SUBSTRING_INDEX(m.Resultat, '-', -1) AS UNSIGNED) > CAST(SUBSTRING_INDEX(m.Resultat, '-', 1) AS UNSIGNED) AND m.equipe_exterieur_id = e.equipe_id THEN 1 ELSE 0 END) AS victoires,
                SUM(CASE WHEN m.Resultat IS NOT NULL AND m.Resultat != '?' AND CAST(SUBSTRING_INDEX(m.Resultat, '-', 1) AS UNSIGNED) < CAST(SUBSTRING_INDEX(m.Resultat, '-', -1) AS UNSIGNED) AND m.equipe_domicile_id = e.equipe_id THEN 1 ELSE 0 END) +
                SUM(CASE WHEN m.Resultat IS NOT NULL AND m.Resultat != '?' AND CAST(SUBSTRING_INDEX(m.Resultat, '-', -1) AS UNSIGNED) < CAST(SUBSTRING_INDEX(m.Resultat, '-', 1) AS UNSIGNED) AND m.equipe_exterieur_id = e.equipe_id THEN 1 ELSE 0 END) AS defaites,
                SUM(CASE WHEN m.Resultat IS NOT NULL AND m.Resultat != '?' AND CAST(SUBSTRING_INDEX(m.Resultat, '-', 1) AS UNSIGNED) = CAST(SUBSTRING_INDEX(m.Resultat, '-', -1) AS UNSIGNED) AND (m.equipe_domicile_id = e.equipe_id OR m.equipe_exterieur_id = e.equipe_id) THEN 1 ELSE 0 END) AS nuls
            FROM equipes e
            LEFT JOIN matches m ON e.equipe_id = m.equipe_domicile_id OR e.equipe_id = m.equipe_exterieur_id
            GROUP BY e.equipe_id, e.nom, e.stade, e.entraineur
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la récupération des victoires, défaites et nuls: {e}")
    finally:
        conn.close()

def get_combined_equipes_data(equipes_data):
    stats_data = get_victoires_defaites_nuls_par_equipe()

    # Convertir stats_data en dictionnaire pour un accès rapide
    stats_dict = {stat['equipe_id']: stat for stat in stats_data}

    # Combiner les données
    combined_data = []
    for equipe in equipes_data:
        equipe_id = equipe['equipe_id']
        if equipe_id in stats_dict:
            equipe.update(stats_dict[equipe_id])
        else:
            equipe.update({'victoires': 0, 'defaites': 0, 'nuls': 0})
        combined_data.append(equipe)

    return combined_data


def add_team(nom, stade, entraineur):
    # Vérifier que les champs ne contiennent pas de chiffres
    if any(char.isdigit() for char in nom) or any(char.isdigit() for char in stade) or any(char.isdigit() for char in entraineur):
        return False, "Les champs nom, stade et entraîneur ne doivent pas contenir de chiffres."
    
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO Equipes (nom, stade, entraineur) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nom, stade, entraineur))
        conn.commit()
        return True, "Équipe ajoutée avec succès."
    finally:
        conn.close()

def delete_team(equipe_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Equipes WHERE equipe_id = %s"
            cursor.execute(sql, (equipe_id,))
            if cursor.rowcount == 0:
                return False, "L'équipe avec cet ID n'existe pas."
        conn.commit()
        return True, "Équipe supprimée avec succès."
    finally:
        conn.close()

def get_all_equipes():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT equipe_id, nom FROM Equipes"
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()

def team_exists(equipe_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT COUNT(*) as count FROM Equipes WHERE equipe_id = %s"
            cursor.execute(sql, (equipe_id,))
            result = cursor.fetchone()
            return result['count'] > 0
    finally:
        conn.close()

def update_team(equipe_id, nom=None, stade=None, entraineur=None):
    if not team_exists(equipe_id):
        return False, "L'équipe avec cet ID n'existe pas."
    
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            if nom:
                if any(char.isdigit() for char in nom):
                    return False, "Le nom de l'équipe ne doit pas contenir de chiffres."
                cursor.execute("UPDATE Equipes SET nom = %s WHERE equipe_id = %s", (nom, equipe_id))
            if stade:
                if any(char.isdigit() for char in stade):
                    return False, "Le nom du stade ne doit pas contenir de chiffres."
                cursor.execute("UPDATE Equipes SET stade = %s WHERE equipe_id = %s", (stade, equipe_id))
            if entraineur:
                if any(char.isdigit() for char in entraineur):
                    return False, "Le nom de l'entraîneur ne doit pas contenir de chiffres."
                cursor.execute("UPDATE Equipes SET entraineur = %s WHERE equipe_id = %s", (entraineur, equipe_id))
        conn.commit()
        return True, "Équipe mise à jour avec succès."
    finally:
        conn.close()


def add_joueur(nom, prenom, poste, equipe_id):
    if any(char.isdigit() for char in nom) or any(char.isdigit() for char in prenom) or any(char.isdigit() for char in poste):
        return False, "Les champs nom, prénom et poste ne doivent pas contenir de chiffres."
    
    if not team_exists(equipe_id):
        return False, "L'équipe avec cet ID n'existe pas."
    
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO Joueurs (nom, prenom, poste, equipe_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nom, prenom, poste, equipe_id))
        conn.commit()
        return True, "Joueur ajouté avec succès."
    except pymysql.MySQLError as e:
        return False, f"Erreur MySQL : {str(e)}"
    finally:
        conn.close()

def delete_joueur(joueur_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Joueurs WHERE joueur_id = %s"
            cursor.execute(sql, (joueur_id,))
            if cursor.rowcount == 0:
                return False, "Le joueur avec cet ID n'existe pas."
        conn.commit()
        return True, "Joueur supprimé avec succès."
    except pymysql.MySQLError as e:
        return False, f"Erreur MySQL : {str(e)}"
    finally:
        conn.close()


def joueur_exists(joueur_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT COUNT(*) as count FROM Joueurs WHERE joueur_id = %s"
            cursor.execute(sql, (joueur_id,))
            result = cursor.fetchone()
            return result['count'] > 0
    except pymysql.MySQLError as e:
        return False
    finally:
        conn.close()

def update_joueur(joueur_id, nom=None, prenom=None, poste=None, equipe_id=None):
    if not joueur_exists(joueur_id):
        return False, "Le joueur avec cet ID n'existe pas."
    
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            if nom:
                if any(char.isdigit() for char in nom):
                    return False, "Le nom du joueur ne doit pas contenir de chiffres."
                cursor.execute("UPDATE Joueurs SET nom = %s WHERE joueur_id = %s", (nom, joueur_id))
            if prenom:
                if any(char.isdigit() for char in prenom):
                    return False, "Le prénom du joueur ne doit pas contenir de chiffres."
                cursor.execute("UPDATE Joueurs SET prenom = %s WHERE joueur_id = %s", (prenom, joueur_id))
            if poste:
                if any(char.isdigit() for char in poste):
                    return False, "Le poste du joueur ne doit pas contenir de chiffres."
                cursor.execute("UPDATE Joueurs SET poste = %s WHERE joueur_id = %s", (poste, joueur_id))
            if equipe_id:
                if not team_exists(equipe_id):
                    return False, "L'équipe avec cet ID n'existe pas."
                cursor.execute("UPDATE Joueurs SET equipe_id = %s WHERE joueur_id = %s", (equipe_id, joueur_id))
        conn.commit()
        return True, "Joueur mis à jour avec succès."
    except pymysql.MySQLError as e:
        return False, f"Erreur MySQL : {str(e)}"
    finally:
        conn.close()


def get_all_joueurs():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT joueur_id, nom, prenom, poste FROM Joueurs"
            cursor.execute(sql)
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        return []
    finally:
        conn.close()