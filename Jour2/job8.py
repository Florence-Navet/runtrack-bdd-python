import mysql.connector

class Zoo:
    def __init__(self):
        self.mydb = None
        self.cursor = None

    def connecter(self):
        """Établit la connexion à la base de données."""
        # Se connecter à MySQL sans spécifier de base de données
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456"
        )
        self.cursor = self.mydb.cursor()

    def creer_base_de_donnees(self):
        """Création de la base de données et des tables si elles n'existent pas déjà."""
        # Créer la base de données si elle n'existe pas
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS zoo")
        self.mydb.commit()

        # Maintenant que la base de données est créée, se connecter à la base "zoo"
        self.cursor.execute("USE zoo")
        
        # Créer les tables "cage" et "animal"
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                superficie FLOAT,
                capacite_max INT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS animal (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100),
                race VARCHAR(100),
                date_naissance DATE,
                pays_origine VARCHAR(100),
                id_cage INT,
                FOREIGN KEY(id_cage) REFERENCES cage(id)
            )
        """)
        self.mydb.commit()

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        if self.cursor:
            self.cursor.close()
        if self.mydb:
            self.mydb.close()

    def ajouter_cage(self, superficie, capacite_max):
        """Ajoute une cage à la base de données."""
        query = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
        values = (superficie, capacite_max)
        self.cursor.execute(query, values)
        self.mydb.commit()
        print("Cage ajoutée avec succès.")

# Utilisation de la base de données
zoo = Zoo()
zoo.connecter()
zoo.creer_base_de_donnees()

# Gestion du zoo
zoo.ajouter_cage(100.5, 5)
zoo.ajouter_cage(200.5, 10)
