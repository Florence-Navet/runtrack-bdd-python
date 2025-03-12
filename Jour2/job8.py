import mysql.connector
import re
from datetime import datetime

class Zoo:
    def __init__(self):
        self.mydb = None
        self.cursor = None

    def connecter(self):
        """Établit la connexion à MySQL et crée la base de données si nécessaire."""
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456"  
        )
        self.cursor = self.mydb.cursor()

        # Créer la base de données si elle n'existe pas
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS zoo")
        self.cursor.execute("USE zoo")  # On change de base de données

        # Maintenant, on peut créer les tables si elles n'existent pas
        self.creer_base_de_donnees()

    def creer_base_de_donnees(self):
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
        return self.cursor.fetchone()[0] > 0
    
    def ajouter_animal(self, nom, race, date_naissance, pays_origine, id_cage):
        if not self.verifier_cage_existe(id_cage):
            print(f"Erreur : La cage ID {id_cage} n'existe pas !")
            return

        # Vérifier la capacité de la cage
        self.cursor.execute("SELECT capacite_max FROM cage WHERE id = %s", (id_cage,))
        capacite_max = self.cursor.fetchone()[0]

        # Vérifier combien d'animaux sont déjà présents dans la cage
        self.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (id_cage,))
        animaux_present = self.cursor.fetchone()[0]

        # Comparer le nombre d'animaux présents à la capacité maximale
        if animaux_present >= capacite_max:
            print(f"Erreur : La cage ID {id_cage} est pleine. Capacité max : {capacite_max}, Animaux présents : {animaux_present}.")
            return

        # Ajouter l'animal si la cage n'est pas pleine
        query = """
            INSERT INTO animal (nom, race, date_naissance, pays_origine, id_cage)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (nom, race, date_naissance, pays_origine, id_cage)
        self.cursor.execute(query, values)
        self.mydb.commit()
        print(f"Animal {nom} ajouté avec succès à la cage ID {id_cage}.")




    def ajouter_cage(self, superficie, capacite_max):
        query = """
            INSERT INTO cage (superficie, capacite_max)
            VALUES (%s, %s)
        """
        self.cursor.execute(query, (superficie, capacite_max))
        self.mydb.commit()
        print("Cage ajoutée avec succès.")

    def afficher_animaux(self):
        self.cursor.execute("SELECT id, nom, race, date_naissance, pays_origine, id_cage FROM animal")
        result = self.cursor.fetchall()
        if result:
            print("\nListe des animaux :")
            for row in result:
                print(f"ID: {row[0]}, Nom: {row[1]}, Race: {row[2]}, Date: {row[3]}, Pays: {row[4]}, Cage ID: {row[5]}")
        else:
            print("Aucun animal trouvé.")

    def afficher_animaux_par_cage(self):
        self.cursor.execute("""
            SELECT cage.id, animal.nom, animal.race
            FROM cage
            LEFT JOIN animal ON cage.id = animal.id_cage
        """)
        result = self.cursor.fetchall()
        if result:
            print("\nAnimaux par cage :")
            for row in result:
                print(f"Cage ID: {row[0]}, Animal: {row[1]}, Race: {row[2]}")
        else:
            print("Aucun animal dans les cages.")

    def deplacer_animal(self, animal_id, nouvelle_cage_id):
        # Vérifier si la cage de destination existe
        if not self.verifier_cage_existe(nouvelle_cage_id):
            print(f"Erreur : La cage ID {nouvelle_cage_id} n'existe pas !")
            return
        
        # Vérifier si l'animal existe dans la base de données
        self.cursor.execute("SELECT COUNT(*) FROM animal WHERE id = %s", (animal_id,))
        if self.cursor.fetchone()[0] == 0:
            print(f"Erreur : L'animal ID {animal_id} n'existe pas !")
            return
        
        # Mettre à jour la cage de l'animal
        query = "UPDATE animal SET id_cage = %s WHERE id = %s"
        self.cursor.execute(query, (nouvelle_cage_id, animal_id))
        self.mydb.commit()
        print(f"Animal ID {animal_id} déplacé vers la cage ID {nouvelle_cage_id}.")

    def capacite_totale_cages(self):
        self.cursor.execute("SELECT SUM(capacite_max) FROM cage")
        capacite_totale = self.cursor.fetchone()[0]
        print(f"La capacité totale des cages est de {capacite_totale} animaux.")

    

    def supprimer_cage(self, cage_id):
        # Avant de supprimer une cage, on vérifie si elle contient des animaux
        self.cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (cage_id,))
        if self.cursor.fetchone()[0] > 0:
            print(f"Erreur : La cage ID {cage_id} contient des animaux et ne peut pas être supprimée.")
        else:
            self.cursor.execute("DELETE FROM cage WHERE id = %s", (cage_id,))
            self.mydb.commit()
            print(f"Cage ID {cage_id} supprimée avec succès.")

    def superficie_totale_cages(self):
        self.cursor.execute("SELECT SUM(superficie) FROM cage")
        total_superficie = self.cursor.fetchone()[0]
        print(f"Superficie totale des cages : {total_superficie} m²")

    def fermer_connexion(self):
        if self.cursor:
            self.cursor.close()
        if self.mydb:
            self.mydb.close()

def demander_texte(prompt):
    while True:
        valeur = input(prompt).strip()
        if re.fullmatch(r"[A-Za-zÀ-ÿ -]+", valeur):
            return valeur
        print("Entrée invalide ! Veuillez entrer uniquement des lettres.")

def demander_date(prompt):
    while True:
        valeur = input(prompt).strip()
        try:
            return datetime.strptime(valeur, "%Y-%m-%d").date()
        except ValueError:
            print("Format invalide ! Veuillez entrer une date au format YYYY-MM-DD.")

def demander_entier(prompt):
    while True:
        valeur = input(prompt).strip()
        if valeur.isdigit():
            return int(valeur)
        print("Veuillez entrer un nombre valide.")

def menu():
    zoo = Zoo()
    zoo.connecter()
    zoo.creer_base_de_donnees()

    while True:
        print("\nMENU PRINCIPAL")
        print("1. Ajouter une cage")
        print("2. Ajouter un animal")
        print("3. Afficher les animaux")
        print("4. Afficher les animaux par cage")
        print("5. Deplacer un animal")
        print("6. Supprimer une cage")
        print("7. Calculer la superficie totale des cages")
        print("8. Quitter")
        choix = input("Choisissez une option (1-8) : ")

        match choix:
            case "1":
                superficie = demander_entier("Superficie de la cage : ")
                capacite_max = demander_entier("Capacité max de la cage : ")
                zoo.ajouter_cage(superficie, capacite_max)
            case "2":
                nom = demander_texte("Nom de l'animal : ")
                race = demander_texte("Race de l'animal : ")
                date_naissance = demander_date("Date de naissance (YYYY-MM-DD) : ")
                pays_origine = demander_texte("Pays d'origine : ")
                id_cage = demander_entier("ID de la cage : ")
                zoo.ajouter_animal(nom, race, date_naissance, pays_origine, id_cage)
            case "3":
                zoo.afficher_animaux()
            case "4":
                zoo.afficher_animaux_par_cage()
            case "5":
                animal_id = demander_entier("ID de l'animal à déplacer : ")
                nouvelle_cage_id = demander_entier("ID de la nouvelle cage : ")
                zoo.deplacer_animal(animal_id, nouvelle_cage_id)
            case "6":
                cage_id = demander_entier("ID de la cage à supprimer : ")
                zoo.supprimer_cage(cage_id)
            case "7":
                zoo.superficie_totale_cages()
            case "8":
                print("Fermeture du programme...")
                zoo.fermer_connexion()
                break
            case _:
                print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    menu()