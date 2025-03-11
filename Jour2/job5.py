import mysql.connector

# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="laplateforme"  
)

if mydb.is_connected():
   
    db_info = mydb.get_server_info()
    print(f"Connecté à MySQL, version : {db_info}")

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = mydb.cursor()

    # Exécuter la requête SQL pour récupérer les noms et capacités des salles
    cursor.execute("SELECT SUM(superficie) FROM etage")

    # Récupérer tous les résultats
    result = cursor.fetchone()

    # Afficher la superficie totale
    if result:
        total_superficie = result [0]
        print(f"La superficie de la Plateforme est de {total_superficie} m2.")



    # Fermer le curseur
    cursor.close()

# Fermer la connexion
mydb.close()
