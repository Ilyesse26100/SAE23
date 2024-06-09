import pymysql
import datetime


def db_connect():
    return pymysql.connect(host='localhost', user='root', password='', db='RealMadridDB', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)





# Create 
def create_match():
    conn = db_connect()
    try:
        # Demander à l'utilisateur de saisir les informations du match
        while True:
            date_str = input("Entrez la date du match (YYYY-MM-DD): ")
            try:
                # Validation de la date
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                if date:
                    break  # Si la date est valide, sortir de la boucle
            except ValueError as e:
                print(f"Date invalide ({e}). Veuillez entrer une date correcte.")
        
        while True:
            home_team_id = input("Entrez l'ID de l'équipe à domicile: ")
            away_team_id = input("Entrez l'ID de l'équipe à l'extérieur: ")
            if home_team_id == away_team_id:
                print("Les équipes ne peuvent pas être les mêmes.")
            else:
                break

        while True:
            result = input("Entrez le résultat du match (format 'X-Y' ou '?'): ")
            if result == '?' or (result.count('-') == 1 and all(part.isdigit() for part in result.split('-'))):
                break
            print("Format invalide. Le résultat doit être sous la forme 'X-Y' où X et Y sont des chiffres, ou '?' pour un match non joué.")
        
        with conn.cursor() as cursor:
            sql = "INSERT INTO Matches (date, equipe_domicile_id, equipe_exterieur_id, Resultat) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (date_str, home_team_id, away_team_id, result))
            conn.commit()
            print("Match créé avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la création du match: {e}")
    finally:
        conn.close()


def read_matches():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            print("Options d'affichage des matches :")
            print("1. Voir tous les matches")
            print("2. Voir seulement les matches à venir")
            print("3. Voir seulement les matches avec scores")
            choice = input("Choisissez une option (1-3): ")

            if choice == '1':
                sql = """
                SELECT Matches.match_id, Matches.date, A.nom as equipe_domicile, B.nom as equipe_exterieur, Matches.Resultat
                FROM Matches
                JOIN Equipes A ON Matches.equipe_domicile_id = A.equipe_id
                JOIN Equipes B ON Matches.equipe_exterieur_id = B.equipe_id
                ORDER BY Matches.date 
                """
            elif choice == '2':
                sql = """
                SELECT Matches.match_id, Matches.date, A.nom as equipe_domicile, B.nom as equipe_exterieur, Matches.Resultat
                FROM Matches
                JOIN Equipes A ON Matches.equipe_domicile_id = A.equipe_id
                JOIN Equipes B ON Matches.equipe_exterieur_id = B.equipe_id
                WHERE Matches.Resultat LIKE '%?%'
                ORDER BY Matches.date 
                """
            elif choice == '3':
                sql = """
                SELECT Matches.match_id, Matches.date, A.nom as equipe_domicile, B.nom as equipe_exterieur, Matches.Resultat
                FROM Matches
                JOIN Equipes A ON Matches.equipe_domicile_id = A.equipe_id
                JOIN Equipes B ON Matches.equipe_exterieur_id = B.equipe_id
                WHERE Matches.Resultat NOT LIKE '%?%'
                ORDER BY Matches.date 
                """
            else:
                print("Choix non valide. Veuillez réessayer.")
                return

            cursor.execute(sql)
            results = cursor.fetchall()
            
            if not results:
                print("Aucun match trouvé.")
                return

            espace= " " * 10
            espace1 = " " * 10
            espace_2 = " " * 15
            espace__3= " " * 5
            print(f"{'match_id':<10}{'Date'} {espace} {'equipe_domicile_id'} {espace } {'equipe_exterieur_id'} {espace}  {'Resultat'}")
            print("-" * 100)
            for result in results:
                print(f"{result['match_id']:<10}{result['date']} {espace1} {result['equipe_domicile']} {espace__3} {result['equipe_exterieur']} {espace_2} {espace__3} {result['Resultat']}")

    except Exception as e:
        print(f"Erreur lors de la lecture des matches: {e}")
    finally:
        conn.close()

def update_match():
    conn = db_connect()
    try:
        while True:
            match_id = input("Entrez l'ID du match à mettre à jour: ")
            if match_id.isdigit():
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM Matches WHERE match_id = %s", (match_id,))
                    match = cursor.fetchone()
                if match:
                    break
                else:
                    print("Aucun match trouvé avec cet ID.")
            else:
                print("L'ID du match doit être un nombre. Veuillez réessayer.")

        updates = []
        params = []

        # Entrée pour l'équipe à domicile
        while True:
            new_home_team_id = input("Entrez le nouvel ID de l'équipe à domicile (laissez vide pour ne pas changer): ")
            if new_home_team_id == '':
                break
            elif new_home_team_id.isdigit():
                updates.append("equipe_domicile_id = %s")
                params.append(new_home_team_id)
                break
            print("L'ID doit être un nombre. Veuillez réessayer.")

        # Entrée pour l'équipe à l'extérieur
        while True:
            new_away_team_id = input("Entrez le nouvel ID de l'équipe à l'extérieur (laissez vide pour ne pas changer): ")
            if new_away_team_id == '':
                break
            elif new_away_team_id.isdigit():
                updates.append("equipe_exterieur_id = %s")
                params.append(new_away_team_id)
                break
            print("L'ID doit être un nombre. Veuillez réessayer.")

        # Entrée pour le résultat
        while True:
            new_result = input("Entrez le nouveau résultat (format 'X-Y' ou '?', laissez vide pour ne pas changer): ")
            if new_result == '':
                break
            elif new_result == '?' or (new_result.count('-') == 1 and all(part.isdigit() for part in new_result.split('-'))):
                updates.append("resultat = %s")
                params.append(new_result)
                break
            print("Format invalide. Le résultat doit être sous la forme 'X-Y' où X et Y sont des chiffres, ou '?' pour un match non joué.")

        # Entrée pour la date
        while True:
            new_date_str = input("Entrez la nouvelle date du match (YYYY-MM-DD, laissez vide pour ne pas changer): ")
            if new_date_str == '':
                break
            try:
                datetime.datetime.strptime(new_date_str, '%Y-%m-%d')  # Validation de la date
                updates.append("date = %s")
                params.append(new_date_str)
                break
            except ValueError as e:
                print(f"Date invalide ({e}). Veuillez entrer une date correcte.")

        if updates:
            with conn.cursor() as cursor:
                params.append(match_id)
                sql = f"UPDATE Matches SET {', '.join(updates)} WHERE match_id = %s"
                cursor.execute(sql, tuple(params))
                conn.commit()
                print("Match mis à jour avec succès.")
        else:
            print("Aucune mise à jour effectuée.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la mise à jour du match: {e}")
    finally:
        conn.close()




# Delete
def delete_match():
    conn = db_connect()
    try:
        match_id = input("Entrez l'ID du match à supprimer: ")
        
        # Vérification de l'existence du match
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Matches WHERE match_id = %s", (match_id,))
            match = cursor.fetchone()
            if not match:
                print(f"Aucun match trouvé avec l'ID {match_id}. Veuillez vérifier et réessayer.")
                return  # Sortie anticipée si aucun match n'est trouvé
        
        # Demander confirmation avant de supprimer
        confirmation = input("Êtes-vous sûr de vouloir supprimer ce match et tous les paris associés ? (oui/non): ")
        if confirmation.lower() != 'oui':
            print("Suppression annulée.")
            return
        
        # Suppression des paris associés à ce match
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Paris WHERE match_id = %s", (match_id,))
            print("Tous les paris associés au match ont été supprimés.")

        # Suppression du match
        with conn.cursor() as cursor:
            sql = "DELETE FROM Matches WHERE match_id = %s"
            cursor.execute(sql, (match_id,))
            conn.commit()
            print("Le match a été supprimé avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la suppression du match: {e}")
    finally:
        conn.close()


# Create 

def create_equipe():
    conn = db_connect()
    try:
        print("\nAjout d'une nouvelle équipe:")
        
        # Boucle de saisie pour le nom de l'équipe
        while True:
            nom = input("Entrez le nom de l'équipe: ").strip()
            if nom.isalpha():
                break
            else:
                print("Le nom de l'équipe ne doit contenir que des lettres. Veuillez réessayer.")
        
        # Boucle de saisie pour le nom du stade
        while True:
            stade = input("Entrez le nom du stade: ").strip()
            if stade.isalpha():
                break
            else:
                print("Le nom du stade ne doit contenir que des lettres. Veuillez réessayer.")
        
        # Boucle de saisie pour le nom de l'entraîneur
        while True:
            entraineur = input("Entrez le nom de l'entraîneur: ").strip()
            if entraineur.replace(' ', '').isalpha():  # Autorise les espaces pour les noms composés
                break
            else:
                print("Le nom de l'entraîneur ne doit contenir que des lettres. Veuillez réessayer.")

        with conn.cursor() as cursor:
            sql = "INSERT INTO Equipes (nom, stade, entraineur) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nom, stade, entraineur))
            conn.commit()
            print(f"L'équipe '{nom}' a été ajoutée avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'ajout de l'équipe: {e}")
    finally:
        conn.close()




# Opération Read : Lire les équipes
def read_equipes():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            print("Options de visualisation des équipes :")
            print("1. Voir toutes les équipes")
            print("2. Voir les statistiques des équipes")

            choice = input("Choisissez une option (1-2): ")

            if choice == '1':
                sql = "SELECT equipe_id, nom, stade, entraineur FROM Equipes"
            elif choice == '2':
                sql = """
                SELECT e.equipe_id, e.nom, COUNT(p.buts) AS total_buts, COUNT(p.passes_decisives) AS total_passes
                FROM Equipes e
                LEFT JOIN Joueurs j ON j.equipe_id = e.equipe_id
                LEFT JOIN Performances p ON p.joueur_id = j.joueur_id
                GROUP BY e.equipe_id, e.nom
                """
            else:
                print("Choix non valide. Veuillez réessayer.")
                return

            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("Aucune information disponible.")
                return

            if choice == '1':
                print_equipe_details(results)
            elif choice == '2':
                print_equipe_stats(results)

    finally:
        conn.close()

def print_equipe_details(results):
    width_equipe_id = max(len(str(equipe['equipe_id'])) for equipe in results) + 2
    width_nom = max(len(equipe['nom']) for equipe in results) + 2
    width_stade = max(len(equipe['stade']) for equipe in results) + 2
    width_entraineur = max(len(equipe['entraineur']) for equipe in results) + 2
    print(f"{'ID':<{width_equipe_id}}{'Nom':<{width_nom}}{'Stade':<{width_stade}}{'Entraîneur':<{width_entraineur}}")
    print('-' * (width_equipe_id + width_nom + width_stade + width_entraineur))
    for equipe in results:
        print(f"{equipe['equipe_id']:<{width_equipe_id}}{equipe['nom']:<{width_nom}}{equipe['stade']:<{width_stade}}{equipe['entraineur']:<{width_entraineur}}")

def print_equipe_stats(results):
    print(f"{'ID':<10}{'Nom':<20}{'Total Buts':<15}{'Total Passes':<15}")
    print('-' * 60)
    for result in results:
        print(f"{result['equipe_id']:<10}{result['nom']:<20}{result.get('total_buts', 0):<15}{result.get('total_passes', 0):<15}")




# Opération Update : Mettre à jour les informations d'une équipe
def update_equipe():
    conn = db_connect()
    try:
        equipe_id = input("Entrez l'ID de l'équipe à mettre à jour: ")

        # Vérification de l'existence de l'équipe
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Equipes WHERE equipe_id = %s", (equipe_id,))
            equipe = cursor.fetchone()
            if not equipe:
                print(f"Aucune équipe trouvée avec l'ID {equipe_id}. Veuillez vérifier l'ID et réessayer.")
                return  # Sortir si l'équipe n'existe pas

        # Si l'équipe existe, demander les nouvelles informations
        while True:
            nom = input("Entrez le nom de l'équipe: ").strip()
            if nom.isalpha():
                break
            else:
                print("Le nom de l'équipe ne doit contenir que des lettres. Veuillez réessayer.")
        
        # Boucle de saisie pour le nom du stade
        while True:
            stade = input("Entrez le nom du stade: ").strip()
            if stade.isalpha():
                break
            else:
                print("Le nom du stade ne doit contenir que des lettres. Veuillez réessayer.")
        
        # Boucle de saisie pour le nom de l'entraîneur
        while True:
            entraineur = input("Entrez le nom de l'entraîneur: ").strip()
            if entraineur.replace(' ', '').isalpha():  # Autorise les espaces pour les noms composés
                break
            else:
                print("Le nom de l'entraîneur ne doit contenir que des lettres. Veuillez réessayer.")

        # Mise à jour de l'équipe
        with conn.cursor() as cursor:
            sql = "UPDATE Equipes SET nom = %s, stade = %s, entraineur = %s WHERE equipe_id = %s"
            cursor.execute(sql, (nom, stade, entraineur, equipe_id))
            conn.commit()
            print("Équipe mise à jour avec succès.")

    except pymysql.MySQLError as e:
        print(f"Erreur lors de la mise à jour de l'équipe: {e}")
    finally:
        conn.close()

# Opération Delete : Supprimer une équipe et  Il est important de supprimer d'abord les dépendances 
# (paris, performances) avant de supprimer les entités principales (matches, joueurs, équipes) pour éviter les violations de contraintes de clé étrangère.
def delete_equipe():
    conn = db_connect()
    try:
        # Affichage des équipes existantes
        with conn.cursor() as cursor:
            cursor.execute("SELECT equipe_id, nom FROM Equipes")
            equipes = cursor.fetchall()
            if not equipes:
                print("Aucune équipe disponible pour suppression.")
                return

            print("Équipes disponibles pour suppression:")
            for equipe in equipes:
                print(f"ID: {equipe['equipe_id']}, Nom: {equipe['nom']}")

            equipe_id = input("Entrez l'ID de l'équipe à supprimer: ")

            # Vérification que l'équipe existe
            cursor.execute("SELECT * FROM Equipes WHERE equipe_id = %s", (equipe_id,))
            if not cursor.fetchone():
                print("Aucune équipe trouvée avec cet ID.")
                return

            # Confirmation avant suppression
            confirmation = input("Êtes-vous sûr de vouloir supprimer cette équipe ? (oui/non): ")
            if confirmation.lower() == 'oui':
                # Suppression des paris liés aux matches où cette équipe est impliquée
                cursor.execute("""
                DELETE FROM Paris WHERE match_id IN (
                    SELECT match_id FROM Matches WHERE equipe_domicile_id = %s OR equipe_exterieur_id = %s
                )""", (equipe_id, equipe_id))

                # Suppression des matches où cette équipe est impliquée
                cursor.execute("DELETE FROM Matches WHERE equipe_domicile_id = %s OR equipe_exterieur_id = %s", (equipe_id, equipe_id))

                # Suppression des performances liées aux joueurs de cette équipe
                cursor.execute("DELETE FROM Performances WHERE joueur_id IN (SELECT joueur_id FROM Joueurs WHERE equipe_id = %s)", (equipe_id,))

                # Suppression de l'équipe et des joueurs associés
                cursor.execute("DELETE FROM Joueurs WHERE equipe_id = %s", (equipe_id,))
                cursor.execute("DELETE FROM Equipes WHERE equipe_id = %s", (equipe_id,))
                conn.commit()
                print("Équipe, joueurs associés, performances, matches et paris supprimés avec succès.")
            else:
                print("Suppression annulée.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la suppression de l'équipe: {e}")
    finally:
        conn.close()




#Fonction qui permet de faire le lien quand on modifie les performances des joueurs


def update_match_score_for_performance(match_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Calculer les buts pour chaque équipe basé sur les performances enregistrées
            sql = """
            SELECT SUM(buts) AS buts_domicile
            FROM Performances 
            JOIN Joueurs ON Performances.joueur_id = Joueurs.joueur_id
            WHERE Performances.match_id = %s AND Joueurs.equipe_id = 
            (SELECT equipe_domicile_id FROM Matches WHERE match_id = %s)
            """
            cursor.execute(sql, (match_id, match_id))
            buts_domicile = cursor.fetchone()['buts_domicile'] or 0

            sql = """
            SELECT SUM(buts) AS buts_exterieur
            FROM Performances 
            JOIN Joueurs ON Performances.joueur_id = Joueurs.joueur_id
            WHERE Performances.match_id = %s AND Joueurs.equipe_id = 
            (SELECT equipe_exterieur_id FROM Matches WHERE match_id = %s)
            """
            cursor.execute(sql, (match_id, match_id))
            buts_exterieur = cursor.fetchone()['buts_exterieur'] or 0

            new_result = f"{buts_domicile}-{buts_exterieur}"
            sql_update = "UPDATE Matches SET resultat = %s WHERE match_id = %s"
            cursor.execute(sql_update, (new_result, match_id))
            conn.commit()
            print(f"Score du match ID {match_id} mis à jour: {new_result}")
    finally:
        conn.close()


# Create 
def create_performance():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Affichage des joueurs disponibles
            cursor.execute("SELECT joueur_id, nom FROM Joueurs")
            joueurs = cursor.fetchall()
            if not joueurs:
                print("Aucun joueur disponible pour ajouter une performance.")
                return

            print("Liste des Joueurs:")
            for joueur in joueurs:
                print(f"ID: {joueur['joueur_id']}, Nom: {joueur['nom']}")

            joueur_id = input("Choisissez l'ID du joueur pour la performance: ")
            if not joueur_id.isdigit() or int(joueur_id) not in [j['joueur_id'] for j in joueurs]:
                print("ID invalide ou joueur non trouvé.")
                return

            # Affichage des matches disponibles
            cursor.execute("SELECT match_id, date FROM Matches")
            matches = cursor.fetchall()
            if not matches:
                print("Aucun match disponible pour ajouter une performance.")
                return

            print("Liste des Matches:")
            for match in matches:
                print(f"ID: {match['match_id']}, Date: {match['date']}")

            match_id = input("Choisissez l'ID du match pour la performance: ")
            if not match_id.isdigit() or int(match_id) not in [m['match_id'] for m in matches]:
                print("ID invalide ou match non trouvé.")
                return

            # Vérification de l'existence d'une performance pour ce joueur et ce match
            cursor.execute("SELECT * FROM Performances WHERE joueur_id = %s AND match_id = %s", (joueur_id, match_id))
            if cursor.fetchone():
                print("Une performance existe déjà pour ce joueur et ce match.")
                if input("Voulez-vous mettre à jour cette performance existante ? (oui/non): ").lower() == 'oui':
                    update_performance()
                return

            buts = input("Entrez le nombre de buts: ")
            passes_decisives = input("Entrez le nombre de passes décisives: ")
            if not all(x.isdigit() for x in [buts, passes_decisives]):
                print("Veuillez entrer des valeurs numériques valides pour les buts et les passes.")
                return

            sql = "INSERT INTO Performances (joueur_id, match_id, buts, passes_decisives) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (joueur_id, match_id, buts, passes_decisives))
            conn.commit()
            print("Performance ajoutée avec succès.")

    finally:
        conn.close()



def read_performances():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Sélectionner les informations nécessaires avec une jointure entre Performances et Joueurs
            sql = """
            SELECT performances.performances_id, joueurs.nom AS joueur_nom, performances.joueur_id, performances.buts, performances.passes_decisives, performances.match_id
            FROM Performances 
            JOIN Joueurs ON performances.joueur_id = joueurs.joueur_id
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results : 
                print("Il n'y a pas de performances à afficher.")

            else:

                # Affichage des résultats
                print(f"{'id':<15}{'Joueur Nom':<20}{'Joueur ID':<20}{'Match ID':<20}{'Buts':<20}{'Passes'}")
                print('-' * 100)
                espace= " " * 10
                espace1 = " " * 10
                espace_2 = " " * 15
                espace__3= " " * 5
                for performance in results:
                    print(f"{performance['performances_id']:<15}{performance['joueur_nom']:<20}{performance['joueur_id']:<10} {espace__3} {espace__3}   {performance['match_id']}  {espace__3}  {espace__3}  {performance['buts']:<5} {espace__3}  {espace__3}   {performance['passes_decisives']:<6}")
    finally:
        conn.close()


def list_and_choose_performance():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT Performances.performances_id, Joueurs.nom, Performances.match_id, Performances.buts, Performances.passes_decisives
            FROM Performances
            JOIN Joueurs ON Performances.joueur_id = Joueurs.joueur_id
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("Aucune performance trouvée.")
                return None

            print("Liste des performances:")
            read_performances()
            performance_id = input("Entrez l'ID de la performance à supprimer: ")
            if any(str(performance['performances_id']) == performance_id for performance in results):
                return performance_id
            else:
                print("ID non valide.")
                return None
    finally:
        conn.close()

def delete_performance():
    performance_id = list_and_choose_performance()
    if performance_id:
        conn = db_connect()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM Performances WHERE performances_id = %s"
                cursor.execute(sql, (performance_id,))
                conn.commit()
                print("Performance supprimée avec succès.")
        finally:
            conn.close()

def update_performance():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Affichage de toutes les performances pour faciliter la sélection
            cursor.execute("""
            SELECT Performances.performances_id, Joueurs.nom AS joueur_nom, Performances.match_id, Performances.buts, Performances.passes_decisives
            FROM Performances
            JOIN Joueurs ON Performances.joueur_id = Joueurs.joueur_id
            """)
            performances = cursor.fetchall()
            if not performances:
                print("Aucune performance trouvée.")
                return

            print("Liste des performances existantes:")
            for perf in performances:
                print(f"ID: {perf['performances_id']}, Joueur: {perf['joueur_nom']}, Match ID: {perf['match_id']}, Buts: {perf['buts']}, Passes: {perf['passes_decisives']}")

            match_id = None  # Initialisation de la variable pour stocker le match_id
            while True:
                performance_id = input("Entrez l'ID de la performance à mettre à jour: ")
                performance = next((p for p in performances if str(p['performances_id']) == performance_id), None)
                if performance:
                    match_id = performance['match_id']  # Sauvegarde du match_id pour utilisation ultérieure
                    break
                print("Performance non trouvée ou ID invalide. Veuillez réessayer.")

            while True:
                new_buts = input("Entrez le nouveau nombre de buts: ")
                if new_buts.isdigit():
                    break
                print("Veuillez entrer un nombre valide pour les buts.")

            while True:
                new_passes = input("Entrez le nouveau nombre de passes décisives: ")
                if new_passes.isdigit():
                    break
                print("Veuillez entrer un nombre valide pour les passes décisives.")

            sql = "UPDATE Performances SET buts = %s, passes_decisives = %s WHERE performances_id = %s"
            cursor.execute(sql, (new_buts, new_passes, performance_id))
            conn.commit()
            print("Performance mise à jour avec succès.")

            if match_id:
                update_match_score_for_performance(match_id)  # Mise à jour du score du match associé

    except pymysql.MySQLError as e:
        print(f"Erreur lors de la mise à jour de la performance: {e}")
    finally:
        conn.close()


def create_joueur():
    conn = db_connect()
    try:
        print("\nAjout d'un nouveau joueur:")

        nom = input("Nom du joueur: ")
        while any(char.isdigit() for char in nom):  # Vérification que le nom ne contient pas de chiffres
            print("Le nom ne doit pas contenir de chiffres.")
            nom = input("Nom du joueur: ")

        prenom = input("Prénom du joueur: ")
        while any(char.isdigit() for char in prenom):  # Vérification que le prénom ne contient pas de chiffres
            print("Le prénom ne doit pas contenir de chiffres.")
            prenom = input("Prénom du joueur: ")

        age = input("Âge du joueur: ")
        while not age.isdigit() or not (18 <= int(age) <= 45):  # Vérification que l'âge est un nombre entre 18 et 45
            print("Veuillez entrer un âge valide (entre 18 et 45 ans).")
            age = input("Âge du joueur: ")
        
        while True:  # Boucle spécifique pour la validation de la date de naissance
            date_naissance = input("Date de naissance (YYYY-MM-DD): ")
            try:
                datetime.datetime.strptime(date_naissance, '%Y-%m-%d')  # Validation de la date de naissance
                break  # Sortie de la boucle si la date est valide
            except ValueError:
                print("Format de date incorrect, veuillez utiliser le format YYYY-MM-DD.")

        # Liste des postes pour faciliter le choix
        postes = ["1: Gardien", "2: Défenseur", "3: Milieu", "4: Attaquant"]
        poste_dict = {1: "Gardien", 2: "Défenseur", 3: "Milieu", 4: "Attaquant"}
        poste = None
        while not poste:
            print("Choisissez un poste parmi les suivants:")
            for poste_option in postes:
                print(poste_option)
            poste_choice = input("Entrez le numéro du poste: ")
            poste = poste_dict.get(int(poste_choice), None)
            if not poste:
                print("Choix de poste invalide. Veuillez réessayer.")

        while True:
            prix_achat = input("Prix d'achat (ex: 3M ou 3000000 pour 3 millions et le prix doit être compris entre 1 million et 300 millions): ")
            try:
                if 'M' in prix_achat.upper():
                    prix = float(prix_achat.upper().replace('M', '')) * 1_000_000
                else:
                    prix = float(prix_achat)
                
                if 1_000_000 <= prix <= 300_000_000:
                    break
                else:
                    print("Le prix doit être compris entre 1 million et 300 millions.")
            except ValueError:
                print("Veuillez entrer un montant valide pour le prix d'achat.")

        read_equipes()
        equipe_id = input("ID de l'équipe: ")
        while not equipe_id.isdigit():
            read_equipes()
            print("Veuillez entrer un ID d'équipe valide.")
            equipe_id = input("ID de l'équipe: ")

        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Joueurs (nom, prenom, age, date_naissance, poste, prix_achat, equipe_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nom, prenom, int(age), date_naissance, poste,prix, int(equipe_id)))
            conn.commit()
            print("Joueur ajouté avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'ajout du joueur: {e}")
    finally:
        conn.close()


def read_joueurs():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            print("\nOptions de visualisation des joueurs :")
            print("1. Voir tous les joueurs")
            print("2. Filtrer par poste")
            print("3. Voir les performances individuelles des joueurs")
            choice = input("Choisissez une option (1-3): ")

            if choice == '1':
                sql = "SELECT joueur_id, nom, prenom, age, date_naissance, poste, prix_achat, equipe_id FROM Joueurs"
            elif choice == '2':
                postes_valides = ["Gardien", "Défenseur", "Milieu", "Attaquant"]
                while True:
                    poste = input("Entrez le poste à filtrer (ex: Gardien, Défenseur, Milieu, Attaquant): ")
                    if poste in postes_valides:
                        sql = f"SELECT joueur_id, nom, prenom, age, date_naissance, poste, prix_achat, equipe_id FROM Joueurs WHERE poste = '{poste}'"
                        break
                    else:
                        print("Le poste doit être Gardien, Défenseur, Milieu ou Attaquant. Veuillez réessayer.")
            elif choice == '3':
                cursor.execute("SELECT joueur_id, nom, prenom FROM Joueurs")
                joueurs = cursor.fetchall()
                if not joueurs:
                    print("Aucun joueur disponible pour visualiser les performances.")
                    return
                print("\nListe des joueurs disponibles:")
                for joueur in joueurs:
                    print(f"ID: {joueur['joueur_id']}, Nom: {joueur['nom']} {joueur['prenom']}")
                
                while True:
                    joueur_id = input("Entrez l'ID du joueur pour voir ses performances ou tapez 'exit' pour quitter: ")
                    if joueur_id.lower() == 'exit':
                        print("Sortie du programme de visualisation des performances.")
                        break

                    if joueur_id.isdigit() and any(int(joueur_id) == j['joueur_id'] for j in joueurs):
                        cursor.execute("SELECT nom, prenom FROM Joueurs WHERE joueur_id = %s", (joueur_id,))
                        joueur = cursor.fetchone()
                        if joueur:
                            sql = """
                            SELECT p.performances_id, p.match_id, p.buts, p.passes_decisives, m.resultat
                            FROM Performances p
                            JOIN Matches m ON p.match_id = m.match_id
                            WHERE p.joueur_id = %s
                            """
                            cursor.execute(sql, (joueur_id,))
                            results = cursor.fetchall()
                            if results:
                                print(f"Performances de {joueur['nom']} {joueur['prenom']} (ID {joueur_id}):")
                                for result in results:
                                    print(f"Performance ID: {result['performances_id']}, Match ID: {result['match_id']}, Buts: {result['buts']}, Passes: {result['passes_decisives']}, Résultat du match: {result['resultat']}")
                                break
                            else:
                                print("Aucune performance trouvée pour ce joueur.")
                                continue
                        else:
                            print("Aucun joueur trouvé avec cet ID.")
                            continue
                    else:
                        print("ID invalide ou non trouvé. Veuillez réessayer ou taper 'exit' pour quitter.")


                return

            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("Aucun joueur trouvé.")
                return

            print(f"{'ID':<5}{'Nom':<20}{'Prénom':<20}{'Âge':<5}{'Date Naissance':<15}{'Poste':<20}{'Prix Achat (€)':<15}{'Équipe ID':<10}")
            print('-' * 120)
            espace= " " * 5
            for joueur in results:
                date_naissance = joueur['date_naissance'].strftime('%Y-%m-%d') if joueur['date_naissance'] else ''
                print(f"{joueur['joueur_id']:<5}{joueur['nom']:<20}{joueur['prenom']:<20}{joueur['age']:<5}{date_naissance:<15}{joueur['poste']:<20}{joueur['prix_achat']:.2f}{espace} {joueur['equipe_id']:<10}")

    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'accès aux données des joueurs: {e}")
    finally:
        conn.close()


def update_joueur():
    conn = db_connect()
    try:
        print("\n--- Mise à jour d'un joueur ---")
        joueur_id = input("Entrez l'ID du joueur à mettre à jour: ")

        with conn.cursor() as cursor:
            # Vérifier si le joueur existe
            cursor.execute("SELECT * FROM Joueurs WHERE joueur_id = %s", (joueur_id,))
            joueur = cursor.fetchone()
            if not joueur:
                print("Aucun joueur trouvé avec cet ID.")
                return

            print("Laissez le champ vide si aucun changement n'est souhaité.")

            nom = input("Nom du joueur (sans chiffres): ")
            while nom and not nom.isalpha():
                print("Le nom ne doit contenir que des lettres.")
                nom = input("Nom du joueur (sans chiffres): ")

            prenom = input("Prénom du joueur (sans chiffres): ")
            while prenom and not prenom.isalpha():
                print("Le prénom ne doit contenir que des lettres.")
                prenom = input("Prénom du joueur (sans chiffres): ")

            age = input("Âge du joueur (18-45): ")
            while age and (not age.isdigit() or not (18 <= int(age) <= 45)):
                print("Veuillez entrer un âge valide (entre 18 et 45 ans).")
                age = input("Âge du joueur (18-45): ")

            date_naissance = input("Date de naissance (YYYY-MM-DD): ")
            while date_naissance:
                try:
                    datetime.datetime.strptime(date_naissance, '%Y-%m-%d')  # Validation de la date de naissance
                    break
                except ValueError:
                    print("Format de date incorrect, veuillez utiliser le format YYYY-MM-DD.")
                    date_naissance = input("Date de naissance (YYYY-MM-DD): ")

            postes = ["1: Gardien", "2: Défenseur", "3: Milieu", "4: Attaquant"]
            poste_dict = {1: "Gardien", 2: "Défenseur", 3: "Milieu", 4: "Attaquant"}
            poste = None
            while not poste:
                print("Choisissez un poste parmi les suivants (laissez vide pour ne pas changer):")
                for poste_option in postes:
                    print(poste_option)
                poste_choice = input(f"Entrez le numéro du poste (actuel : {joueur['poste']}): ")
                if poste_choice.isdigit() and int(poste_choice) in poste_dict:
                    poste = poste_dict[int(poste_choice)]
                elif not poste_choice:  # Permet de laisser le champ inchangé en appuyant sur Entrée
                    poste = joueur['poste']
                    break
                else:
                    print("Choix de poste invalide. Veuillez réessayer.")
            while True:
                prix_achat = input("Prix d'achat (ex: 3M ou 3000000 pour 3 millions et le prix doit être compris entre 1 million et 300 millions, laissez vide pour ne pas changer): ")
                if prix_achat == "":
                    break  # Sortir de la boucle si l'utilisateur appuie sur Entrée sans entrer de valeur
                try:
                    if 'M' in prix_achat.upper():
                        prix = float(prix_achat.upper().replace('M', '')) * 1_000_000
                    else:
                        prix = float(prix_achat)
                    
                    if 1_000_000 <= prix <= 300_000_000:
                        break  # Sortir de la boucle si le prix est dans l'intervalle valide
                    else:
                        print("Le prix doit être compris entre 1 million et 300 millions.")
                except ValueError:
                    print("Veuillez entrer un montant valide pour le prix d'achat.")
    
            equipe_id = input("ID de l'équipe: ")
            while equipe_id and not equipe_id.isdigit():
                print("Veuillez entrer un ID d'équipe valide.")
                equipe_id = input("ID de l'équipe: ")

            # Construction de la requête SQL avec les champs modifiés
            updates = []
            params = []
            if nom:
                updates.append("nom = %s")
                params.append(nom)
            if prenom:
                updates.append("prenom = %s")
                params.append(prenom)
            if age:
                updates.append("age = %s")
                params.append(int(age))
            if date_naissance:
                updates.append("date_naissance = %s")
                params.append(date_naissance)
            if poste:
                updates.append("poste = %s")
                params.append(poste)
            if prix_achat:
                updates.append("prix_achat = %s")
                params.append(prix)
            if equipe_id:
                updates.append("equipe_id = %s")
                params.append(int(equipe_id))

            if updates:
                params.append(joueur_id)
                sql = f"UPDATE Joueurs SET {', '.join(updates)} WHERE joueur_id = %s"
                cursor.execute(sql, tuple(params))
                conn.commit()
                print("Joueur mis à jour avec succès.")
            else:
                print("Aucune mise à jour effectuée.")

    except pymysql.MySQLError as e:
        print("Erreur lors de la mise à jour du joueur:", e)
    finally:
        conn.close()

def delete_joueur():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Affichage des joueurs disponibles
            cursor.execute("SELECT joueur_id, nom, prenom FROM Joueurs")
            joueurs = cursor.fetchall()
            if not joueurs:
                print("Aucun joueur disponible pour suppression.")
                return

            print("Joueurs disponibles pour suppression:")
            for joueur in joueurs:
                print(f"ID: {joueur['joueur_id']}, Nom: {joueur['nom']} {joueur['prenom']}")

            joueur_id = input("Entrez l'ID du joueur à supprimer: ")

            # Vérification de l'existence du joueur
            cursor.execute("SELECT * FROM Joueurs WHERE joueur_id = %s", (joueur_id,))
            if not cursor.fetchone():
                print("Aucun joueur trouvé avec cet ID.")
                return

            # Confirmation avant suppression
            confirmation = input("Êtes-vous sûr de vouloir supprimer ce joueur et toutes ses performances associées ? (oui/non): ")
            if confirmation.lower() == 'oui':
                # Suppression des performances associées
                cursor.execute("SELECT match_id FROM Performances WHERE joueur_id = %s", (joueur_id,))
                matches = cursor.fetchall()
                cursor.execute("DELETE FROM Performances WHERE joueur_id = %s", (joueur_id,))

                # Mise à jour des scores des matches concernés
                for match in matches:
                    update_match_score_for_performance(match['match_id'])

                # Suppression du joueur
                cursor.execute("DELETE FROM Joueurs WHERE joueur_id = %s", (joueur_id,))
                conn.commit()
                print("Joueur et toutes ses performances associées supprimés avec succès.")
            else:
                print("Suppression annulée.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la suppression du joueur: {e}")
    finally:
        conn.close()


def create_supporteur():
    conn = db_connect()
    try:
        print("Ajout d'un nouveau supporteur:")
        nom = input("Nom du supporteur: ")
        prenom = input("Prénom du supporteur: ")

        while any(char.isdigit() for char in nom) or any(char.isdigit() for char in prenom):
            print("Les noms et prénoms ne doivent pas contenir de chiffres.")
            nom = input("Nom du supporteur: ")
            prenom = input("Prénom du supporteur: ")

        with conn.cursor() as cursor:
            sql = "INSERT INTO Supporteurs (nom, prenom) VALUES (%s, %s)"
            cursor.execute(sql, (nom, prenom))
            conn.commit()
            print("Supporteur ajouté avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'ajout du supporteur: {e}")
    finally:
        conn.close()


def read_supporteurs():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT supporteur_id, nom, prenom FROM Supporteurs"
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("Aucun supporteur trouvé.")
            else:
                print(f"{'ID':<10}{'Nom':<20}{'Prénom':<20}")
                print('-' * 50)
                for supporteur in results:
                    print(f"{supporteur['supporteur_id']:<10}{supporteur['nom']:<20}{supporteur['prenom']:<20}")
    finally:
        conn.close()

def update_supporteur():
    conn = db_connect()
    try:
        supporteur_id = input("Entrez l'ID du supporteur à mettre à jour: ")
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Supporteurs WHERE supporteur_id = %s", (supporteur_id,))
            if not cursor.fetchone():
                print("Aucun supporteur trouvé avec cet ID.")
                return

            while True:
                nom = input("Nouveau nom (laissez vide pour ne pas changer): ")
                if nom and any(char.isdigit() for char in nom):
                    print("Le nom ne peut pas contenir de chiffres.")
                else:
                    break

            while True:
                prenom = input("Nouveau prénom (laissez vide pour ne pas changer): ")
                if prenom and any(char.isdigit() for char in prenom):
                    print("Le prénom ne peut pas contenir de chiffres.")
                else:
                    break

            updates = []
            params = []
            if nom:
                updates.append("nom = %s")
                params.append(nom)
            if prenom:
                updates.append("prenom = %s")
                params.append(prenom)

            if updates:
                params.append(supporteur_id)
                sql = f"UPDATE Supporteurs SET {', '.join(updates)} WHERE supporteur_id = %s"
                cursor.execute(sql, tuple(params))
                conn.commit()
                print("Supporteur mis à jour avec succès.")
            else:
                print("Aucune mise à jour effectuée.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la mise à jour du supporteur: {e}")
    finally:
        conn.close()


#Une fois l'ID du supporteur confirmé, tous les paris associés à cet ID sont supprimés.
# Cela est fait avant la suppression du supporteur pour maintenir l'intégrité des données et éviter les orphelins dans la base de données.

def delete_supporteur():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Affichage des supporteurs existants
            cursor.execute("SELECT supporteur_id, nom, prenom FROM Supporteurs")
            supporteurs = cursor.fetchall()
            if not supporteurs:
                print("Aucun supporteur trouvé.")
                return

            print("Liste des supporteurs:")
            for supporteur in supporteurs:
                print(f"ID: {supporteur['supporteur_id']}, Nom: {supporteur['nom']}, Prénom: {supporteur['prenom']}")

            supporteur_id = input("Entrez l'ID du supporteur à supprimer: ")

            # Vérification de l'existence du supporteur
            cursor.execute("SELECT * FROM Supporteurs WHERE supporteur_id = %s", (supporteur_id,))
            if not cursor.fetchone():
                print("Aucun supporteur trouvé avec cet ID.")
                return

            # Suppression de tous les paris associés au supporteur
            cursor.execute("DELETE FROM Paris WHERE supporteur_id = %s", (supporteur_id,))
            print(f"Tous les paris associés au supporteur ID {supporteur_id} ont été supprimés.")

            # Suppression du supporteur
            cursor.execute("DELETE FROM Supporteurs WHERE supporteur_id = %s", (supporteur_id,))
            conn.commit()
            print(f"Le supporteur ID {supporteur_id} a été supprimé avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la suppression du supporteur et de ses paris: {e}")
    finally:
        conn.close()


def create_pari():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Affichage des supporteurs disponibles
            cursor.execute("SELECT supporteur_id, nom, prenom FROM Supporteurs")
            supporteurs = cursor.fetchall()
            if not supporteurs:
                print("Aucun supporteur disponible.")
                return

            print("Liste des supporteurs:")
            for supporteur in supporteurs:
                print(f"ID: {supporteur['supporteur_id']}, Nom: {supporteur['nom']}, Prénom: {supporteur['prenom']}")

            # Boucle pour la validation de l'ID du supporteur
            while True:
                supporteur_id = input("Choisissez l'ID du supporteur pour le pari: ")
                if supporteur_id.isdigit() and any(s['supporteur_id'] == int(supporteur_id) for s in supporteurs):
                    break
                print("Supporteur non trouvé ou entrée invalide. Veuillez réessayer.")

            # Boucle pour sélection du match à venir
            while True:
                cursor.execute("SELECT match_id, date FROM Matches WHERE Resultat = '?'")
                matches = cursor.fetchall()
                if not matches:
                    print("Aucun match à venir disponible pour parier.")
                    return

                print("Liste des matches à venir:")
                for match in matches:
                    print(f"ID: {match['match_id']}, Date: {match['date']}")

                match_id = input("Choisissez l'ID du match pour le pari: ")
                if match_id.isdigit() and any(m['match_id'] == int(match_id) for m in matches):
                    break
                print("Match non trouvé, entrée invalide, ou le match a déjà été joué. Veuillez réessayer.")

            while True:
                mise = input("Entrez la mise pour le pari (ex: 50): ")
                if mise.isdigit() and float(mise) > 0:
                    break
                print("Veuillez entrer une mise valide.")

            while True:
                resultat_predi = input("Entrez le résultat prédit (ex: 2-1): ")
                if resultat_predi and '-' in resultat_predi and all(part.isdigit() for part in resultat_predi.split('-')):
                    break
                print("Veuillez entrer un résultat prédit valide sous la forme 'X-Y'.")

            # Insertion du pari
            sql = "INSERT INTO Paris (supporteur_id, match_id, mise, Resultat_prédit) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (supporteur_id, match_id, mise, resultat_predi))
            conn.commit()
            print(f"Le pari a été ajouté avec succès pour le supporteur ID {supporteur_id} sur le match ID {match_id}.")

    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'ajout du pari: {e}")
    finally:
        conn.close()


def read_paris():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT paris_id, supporteur_id, match_id, mise, Resultat_prédit FROM Paris"
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("Aucun pari trouvé.")
            else:
                # Définir une largeur minimale pour chaque colonne
                width_pari_id = 15
                width_supporteur_id = 20
                width_match_id = 15
                width_mise = 20  # Largeur suffisante pour la mise avec deux décimales
                width_resultat = 20

                # En-têtes
                print(f"{'ID Pari':<{width_pari_id}}{'ID Supporteur':<{width_supporteur_id}}{'ID Match':<{width_match_id}}{'Mise (€)':<{width_mise}}{'Résultat Prédit':<{width_resultat}}")
                print('-' * (width_pari_id + width_supporteur_id + width_match_id + width_mise + width_resultat))

                # Données
                for pari in results:
                    mise_formatted = f"{pari['mise']:.2f} €"  # Formatage de la mise en euros
                    print(f"{pari['paris_id']:<{width_pari_id}}{pari['supporteur_id']:<{width_supporteur_id}}{pari['match_id']:<{width_match_id}}{mise_formatted:<{width_mise}}{pari['Resultat_prédit']:<{width_resultat}}")
    finally:
        conn.close()



def delete_pari():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Rechercher tous les paris disponibles
            sql_find_all_paris = "SELECT paris_id, supporteur_id, match_id, mise, Resultat_prédit FROM Paris"
            cursor.execute(sql_find_all_paris)
            all_paris = cursor.fetchall()

            if all_paris:
                print("Voici la liste des paris disponibles :")
                read_paris()
                # Demander à l'utilisateur quel pari supprimer
                pari_id = input("Entrez l'ID du pari à mettre à jour: ")
                while not pari_id.isdigit() or not any(int(pari_id) == p['paris_id'] for p in all_paris):
                    print("ID de pari non valide ou non trouvé. Veuillez réessayer.")
                    pari_id = input("Entrez l'ID du pari à mettre à jour: ")
                
                # Suppression du pari sélectionné
                sql_delete_pari = "DELETE FROM Paris WHERE paris_id = %s"
                cursor.execute(sql_delete_pari, (pari_id,))
                conn.commit()
                print(f"Le pari ID {pari_id} a été supprimé.")
            else:
                print("Aucun pari trouvé.")

    except pymysql.MySQLError as e:
        print(f"Erreur lors de la suppression du pari: {e}")
    finally:
        conn.close()


def update_pari():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            # Afficher tous les paris pour aider l'utilisateur à choisir
            cursor.execute("SELECT paris_id, supporteur_id, match_id, mise, Resultat_prédit FROM Paris")
            paris = cursor.fetchall()

            if not paris:
                print("Aucun pari disponible pour la mise à jour.")
                return

            print("Liste des paris disponibles:")
            for pari in paris:
                print(f"ID Pari: {pari['paris_id']}, Supporteur: {pari['supporteur_id']}, Match: {pari['match_id']}, Mise: {pari['mise']}, Résultat Prédit: {pari['Resultat_prédit']}")

            pari_id = input("Entrez l'ID du pari à mettre à jour: ")
            while not pari_id.isdigit() or not any(int(pari_id) == p['paris_id'] for p in paris):
                print("ID de pari non valide ou non trouvé. Veuillez réessayer.")
                pari_id = input("Entrez l'ID du pari à mettre à jour: ")

            # Collecte des nouvelles valeurs
            nouvelle_mise = input("Entrez la nouvelle mise (laissez vide pour ne pas changer): ")
            while nouvelle_mise and not nouvelle_mise.isdigit():
                print("La mise doit être un nombre. Veuillez réessayer.")
                nouvelle_mise = input("Entrez la nouvelle mise (laissez vide pour ne pas changer): ")

            nouveau_resultat = input("Entrez le nouveau résultat prédit (laissez vide pour ne pas changer): ")
            while nouveau_resultat and not ('-' in nouveau_resultat and all(part.isdigit() for part in nouveau_resultat.split('-'))):
                print("Le format du résultat prédit est invalide. Il doit être sous la forme 'X-Y'. Veuillez réessayer.")
                nouveau_resultat = input("Entrez le nouveau résultat prédit (laissez vide pour ne pas changer): ")

            updates = []
            params = []
            if nouvelle_mise:
                updates.append("mise = %s")
                params.append(nouvelle_mise)
            if nouveau_resultat:
                updates.append("Resultat_prédit = %s")
                params.append(nouveau_resultat)

            if updates:
                params.append(pari_id)
                sql_update_pari = "UPDATE Paris SET " + ', '.join(updates) + " WHERE paris_id = %s"
                cursor.execute(sql_update_pari, tuple(params))
                conn.commit()
                print(f"Le pari ID {pari_id} a été mis à jour avec succès.")
            else:
                print("Aucune information n'a été mise à jour.")

    except pymysql.MySQLError as e:
        print(f"Erreur lors de la mise à jour du pari: {e}")
    finally:
        conn.close()


def determine_winners():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT p.supporteur_id, SUM(p.mise) * 2 AS total_gain
            FROM Paris p
            JOIN Matches m ON p.match_id = m.match_id
            WHERE p.Resultat_prédit = m.resultat
            GROUP BY p.supporteur_id;
            """
            cursor.execute(sql)
            winners = cursor.fetchall()

            if not winners:
                print("Aucun pari gagnant.")
            else:
                print("Liste des gains par supporteur:")
                for winner in winners:
                    print(f"Supporteur ID: {winner['supporteur_id']}, Total Gain: {winner['total_gain']}€")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la détermination des gagnants: {e}")
    finally:
        conn.close()



def determine_losers():
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT p.supporteur_id, SUM(p.mise) AS total_loss
            FROM Paris p
            JOIN Matches m ON p.match_id = m.match_id
            WHERE p.Resultat_prédit != m.resultat
            GROUP BY p.supporteur_id;
            """
            cursor.execute(sql)
            losers = cursor.fetchall()

            if not losers:
                print("Aucun pari perdant.")
            else:
                print("Liste des pertes par supporteur:")
                for loser in losers:
                    print(f"Supporteur ID: {loser['supporteur_id']}, Total Perte: {loser['total_loss']}€")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la détermination des perdants: {e}")
    finally:
        conn.close()



