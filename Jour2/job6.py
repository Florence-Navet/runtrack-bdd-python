import mysql.connector

# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",  # Remplace par ton mot de passe
    database="laplateforme"  
)

if mydb.is_connected():
   
    db_info = mydb.get_server_info()
    print(f"Connecté à MySQL, version : {db_info}")

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = mydb.cursor()

    # Exécuter la requête SQL pour récupérer les noms et capacités des salles
    cursor.execute("SELECT SUM(capacite) FROM salle")

    # Récupérer tous les résultats
    result = cursor.fetchone()

    # Afficher la capacité totale
    if result:
        total_capacite = result[0]
        print(f"La capacité totale des salles est de {total_capacite}.")


    # Fermer le curseur
    cursor.close()

# Fermer la connexion
mydb.close()
