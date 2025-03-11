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
    cursor.execute("SELECT nom, capacite FROM salle")

    # Récupérer tous les résultats
    results = cursor.fetchall()

    # Afficher le résultat dans la console
    print("Liste des salles et leurs capacités:")
    for row in results:
        print(f"Nom: {row[0]}, Capacité: {row[1]}")

    # Fermer le curseur
    cursor.close()

# Fermer la connexion
mydb.close()
