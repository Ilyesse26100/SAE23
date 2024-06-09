import csv
import pymysql
import datetime

# Configuration de la connexion à la base de données
connection = pymysql.connect(host="localhost",
                             user="root",
                             password="",
                             db='RealMadridDB',
                             charset='utf8mb4',)

try:
    # Création d'un curseur pour exécuter des requêtes SQL
    with connection.cursor() as cursor:
        # Lecture des données depuis le fichier CSV
        with open(r'JeuDessai.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Ignorer l'en-tête du fichier CSV
            for row in reader:
                 if len(row) == 4:
                    # Essayer de parser la date pour vérifier si c'est un match
                    try:
                        datetime.datetime.strptime(row[0], "%Y-%m-%d")
                        is_date = True
                    except ValueError:
                        is_date = False

                    if is_date:
                        # Vérifier si le match existe déjà
                        cursor.execute("SELECT * FROM Matches WHERE date = %s AND equipe_domicile_id = %s AND equipe_exterieur_id = %s", (row[0], row[1], row[2]))
                        if cursor.fetchone() is None:
                            sql = "INSERT INTO Matches (date, equipe_domicile_id, equipe_exterieur_id, Resultat) VALUES (%s, %s, %s, %s)"
                            cursor.execute(sql, (row[0], row[1], row[2], row[3]))
                    else:
                        # Vérifier si c'est un pari
                        if "-" in row[3] and any(char.isdigit() for char in row[3]):
                            # Vérifier si le pari existe déjà
                            cursor.execute("SELECT * FROM Paris WHERE match_id = %s AND supporteur_id = %s", (row[0], row[1]))
                            if cursor.fetchone() is None:
                                sql = "INSERT INTO Paris (match_id, supporteur_id, mise, Resultat_Prédit) VALUES (%s, %s, %s, %s)"
                                cursor.execute(sql, (row[0], row[1], row[2], row[3]))
                        else:
                            # Vérifier si la performance existe déjà
                            cursor.execute("SELECT * FROM Performances WHERE joueur_id = %s AND match_id = %s", (row[0], row[1]))
                            if cursor.fetchone() is None:
                                sql = "INSERT INTO Performances (joueur_id, match_id, buts, passes_decisives) VALUES (%s, %s, %s, %s)"
                                cursor.execute(sql, (row[0], row[1], row[2], row[3]))

                 elif len(row) == 7:
                    # Vérifier si le joueur existe déjà
                    cursor.execute("SELECT * FROM Joueurs WHERE nom = %s AND prenom = %s", (row[0], row[1]))
                    if cursor.fetchone() is None:
                        sql = "INSERT INTO Joueurs (nom, prenom, age, date_naissance, poste, prix_achat, equipe_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

                 elif len(row) == 2:
                    # Vérifier si le supporteur existe déjà
                    cursor.execute("SELECT * FROM Supporteurs WHERE nom = %s AND prenom = %s", (row[0], row[1]))
                    if cursor.fetchone() is None:
                        sql = "INSERT INTO Supporteurs (nom, prenom) VALUES (%s, %s)"
                        cursor.execute(sql, (row[0], row[1]))

                 elif len(row) == 3:
                    # Vérifier si l'équipe existe déjà
                    cursor.execute("SELECT * FROM Equipes WHERE nom = %s", (row[0],))
                    if cursor.fetchone() is None:
                        sql = "INSERT INTO Equipes (nom, stade, entraineur) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (row[0], row[1], row[2]))
 
    # Sauvegarde des modifications dans la base de données
    connection.commit()

finally:
    # Fermeture de la connexion à la base de données
    connection.close()
