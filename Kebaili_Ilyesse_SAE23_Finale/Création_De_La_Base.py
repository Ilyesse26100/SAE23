import pymysql

# Configuration des paramètres de connexion à la base de données MySQL
host = "localhost"
user = "votre_utilisateur_mysql"
password = "votre_mot_de_passe_mysql"
charset = "utf8mb4"
db_name = "RealMadridDB"

# Établissement de la connexion à MySQL
connection = pymysql.connect(host="localhost", user="root", password="", charset="utf8mb4")

# Création de la base de données si elle n'existe pas
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
connection.commit()
# Sélection de la base de données créée pour les opérations futures
cursor.execute(f"USE {db_name}")

# Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Equipes (
    equipe_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    stade VARCHAR(255),
    entraineur VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Supporteurs (
    supporteur_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Joueurs (
    joueur_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    age INT,
    date_naissance DATE,
    poste VARCHAR(255),
    prix_achat DECIMAL(10, 2),
    equipe_id INT,
    FOREIGN KEY (equipe_id) REFERENCES Equipes(equipe_id) ON DELETE CASCADE    
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    equipe_domicile_id INT ,
    equipe_exterieur_id INT,
    Resultat VARCHAR(255),
    FOREIGN KEY (equipe_domicile_id) REFERENCES Equipes(equipe_id) ON DELETE CASCADE,
    FOREIGN KEY (equipe_exterieur_id) REFERENCES Equipes(equipe_id) ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Performances (
    performances_id INT AUTO_INCREMENT PRIMARY KEY,
    joueur_id INT,
    match_id INT,
    buts INT DEFAULT 0,
    passes_decisives INT DEFAULT 0,
    FOREIGN KEY (joueur_id) REFERENCES Joueurs(joueur_id) ON DELETE CASCADE ,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id) ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Paris (
    paris_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    supporteur_id INT,
    mise DECIMAL(10, 2),
    Resultat_Prédit VARCHAR(255) , 
    FOREIGN KEY (match_id) REFERENCES Matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (supporteur_id) REFERENCES Supporteurs(supporteur_id) ON DELETE CASCADE               
)
""")

# Validation des opérations de création
connection.commit()

# Fermeture de la connexion et du curseur
cursor.close()
connection.close()
