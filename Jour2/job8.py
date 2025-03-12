import mysql.connector
from datetime import datetime

class Zoo:
    def __init__(self):
        self.mydb = None
        self.cursor = None

    def connecter(self):
        """Établit la connexion à la base de données."""
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="zoo"
        )
        self.cursor = self.mydb.cursor()

    def creer_base_de_donnees(self):
        """Créer la base de données et les tables si elles n'existent pas déjà."""
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS zoo")
        self.mydb.commit()

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
                FOREIGN KEY (id_cage) REFERENCES cage(id)
            )
        """)
        self.mydb.commit()
        
    def verifier_cage_existe(self, id_cage):
        self.cursor.execute("SELECT COUNT(*) FROM cage WHERE id = %s", (id_cage,))
        result = self.cursor.fetchone()

        if result[0] > 0:
            return True
        else:
            return False
        

    def ajouter_animal(self, nom, race, date_naissance, pays_origine, id_cage):
        """Ajoute un animal dans la base de données après vérification de la cage."""
        if not self.verifier_cage_existe(id_cage):
            print(f"Erreur : La cage ID {id_cage} n'existe pas !")
            return
        query = """
            INSERT INTO animal (nom, race, date_naissance, pays_origine, id_cage)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (nom, race, date_naissance, pays_origine, id_cage)
        self.cursor.execute(query, values)
        self.mydb.commit()
        print(f"Animal {nom} ajouté avec succès.")


    def ajouter_cage(self, superficie, capacite_max):
        """Ajoute une cage dans la base de données."""
        query = """
            INSERT INTO cage (superficie, capacite_max)
            VALUES (%s, %s)
        """
        values = (superficie, capacite_max)
        self.cursor.execute(query, values)
        self.mydb.commit()
        print(f"Cage ajoutée avec succès.")







    def supprimer_animal(self, animal_id):
        """Supprime un animal de la base de données."""
        query = "DELETE FROM animal WHERE id = %s"
        self.cursor.execute(query, (animal_id,))
        self.mydb.commit()
        print(f"Animal ID {animal_id} supprimé avec succès.")

    def supprimer_cage(self, cage_id):
        """Supprime une cage de la base de données."""
        query = "DELETE FROM cage WHERE id = %s"
        self.cursor.execute(query, (cage_id,))
        self.mydb.commit()
        print(f"Cage ID {cage_id} supprimée avec succès.")

    def modifier_animal(self, animal_id, nom=None, race=None, date_naissance=None, pays_origine=None, id_cage=None):
        """Modifie les informations d'un animal."""
        update_str = "SET "
        values = []

        if nom:
            update_str += "nom = %s, "
            values.append(nom)
        if race:
            update_str += "race = %s, "
            values.append(race)
        if date_naissance:
            update_str += "date_naissance = %s, "
            values.append(date_naissance)
        if pays_origine:
            update_str += "pays_origine = %s, "
            values.append(pays_origine)
        if id_cage:
            update_str += "id_cage = %s, "
            values.append(id_cage)

        update_str = update_str.rstrip(", ")

        query = f"UPDATE animal {update_str} WHERE id = %s"
        values.append(animal_id)
        self.cursor.execute(query, tuple(values))
        self.mydb.commit()
        print(f"Animal ID {animal_id} modifié avec succès.")

    def afficher_animaux(self):
        """Affiche tous les animaux dans le zoo."""
        self.cursor.execute("""
            SELECT a.id, a.nom, a.race, a.date_naissance, a.pays_origine, c.id 
            FROM animal a
            LEFT JOIN cage c ON a.id_cage = c.id
        """)
        result = self.cursor.fetchall()

        if result:
            print("Liste des animaux dans le zoo :")
            for row in result:
                print(f"ID: {row[0]}, Nom: {row[1]}, Race: {row[2]}, Date de naissance: {row[3]}, Pays d'origine: {row[4]}, Cage ID: {row[5]}")
        else:
            print("Aucun animal trouvé.")

    def afficher_animaux_par_cage(self):
        """Affiche les animaux dans chaque cage."""
        self.cursor.execute("""
            SELECT c.id, c.superficie, a.nom 
            FROM cage c
            LEFT JOIN animal a ON c.id = a.id_cage
        """)
        result = self.cursor.fetchall()

        if result:
            print("Liste des animaux par cage :")
            current_cage_id = None
            for row in result:
                if row[0] != current_cage_id:
                    print(f"\nCage ID: {row[0]}, Superficie: {row[1]} m²")
                    current_cage_id = row[0]
                print(f"  - {row[2]}")
        else:
            print("Aucun animal dans les cages.")

    def superficie_totale_cages(self):
        """Calcule la superficie totale des cages."""
        self.cursor.execute("SELECT SUM(superficie) FROM cage")
        result = self.cursor.fetchone()
        if result:
            print(f"La superficie totale des cages est de {result[0]:.2f} m².")
        else:
            print("Aucune cage trouvée.")

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        if self.cursor:
            self.cursor.close()
        if self.mydb:
            self.mydb.close()


# Utilisation du programme
zoo = Zoo()
zoo.connecter()
zoo.creer_base_de_donnees()

# Exemples de gestion du zoo

# Ajouter des cages
zoo.ajouter_cage(100.5, 5)
zoo.ajouter_cage(200.0, 10)

# Ajouter des animaux
# zoo.ajouter_animal("Lion", "Panthera leo", "2015-03-21", "Afrique", 1)
# zoo.ajouter_animal("Éléphant", "Loxodonta", "2012-10-11", "Afrique", 2)

# Afficher tous les animaux
zoo.afficher_animaux()

# Afficher les animaux par cage
zoo.afficher_animaux_par_cage()

# Calculer la superficie totale des cages
zoo.superficie_totale_cages()

# Modifier un animal
zoo.modifier_animal(1, nom="Lion King")

# Afficher tous les animaux
zoo.afficher_animaux()

# Supprimer un animal
# zoo.supprimer_animal(2)

# Supprimer une cage
# zoo.supprimer_cage(2)

# Fermer la connexion
zoo.fermer_connexion()
