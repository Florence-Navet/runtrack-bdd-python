import mysql.connector

class Employe:
    def __init__(self, id=None, nom=None, prenom=None, salaire=None, id_service=None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.salaire = salaire
        self.id_service = id_service
        self.mydb = None
        self.cursor = None

    def connecter(self):
        """Établit la connexion à la base de données."""
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="entreprise"
        )
        self.cursor = self.mydb.cursor()

    def delete_employe_par_nom_prenom(self, nom, prenom):
        """Supprime tous les employés avec le même nom et prénom."""
        if not self.mydb or not self.cursor:
            print("Erreur : connexion à la base de données non établie.")
            return

        # Supprimer tous les employés avec ce nom et prénom
        self.cursor.execute("DELETE FROM employe WHERE nom = %s AND prenom = %s", (nom, prenom))
        self.mydb.commit()

        print(f"Tous les employés {prenom} {nom} ont été supprimés avec succès.")

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        if self.cursor:
            self.cursor.close()
        if self.mydb:
            self.mydb.close()

    def reinitialiser_auto_increment(self):
        """Réinitialise l'auto-increment à la valeur suivante la plus basse."""
        if not self.mydb or not self.cursor:
            print("Erreur : connexion à la base de données non établie.")
            return

        self.cursor.execute("ALTER TABLE employe AUTO_INCREMENT = 1")
        self.mydb.commit()
        print("Auto-increment réinitialisé.")


    def ajouter_employe(self):
        """Ajoute un employé à la base de données."""
        if not self.mydb or not self.cursor:
            print("Erreur : connexion à la base de données non établie.")
            return

        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        values = (self.nom, self.prenom, self.salaire, self.id_service)
        self.cursor.execute(query, values)
        self.mydb.commit()
        print(f"Employé {self.nom} {self.prenom} ajouté avec succès.")
        
    def afficher_employes(self):
        """Affiche tous les employés avec leur service."""
        if not self.mydb or not self.cursor:
            print("Erreur : connexion à la base de données non établie.")
            return
        
        self.cursor.execute("""
            SELECT e.id, e.nom, e.prenom, e.salaire, 
                   COALESCE(s.nom, 'Aucun service') AS service 
            FROM employe e 
            LEFT JOIN service s ON e.id_service = s.id
        """)
        
        result = self.cursor.fetchall()

        if result:
            print("Liste des employés :")
            for row in result:
                print(f"ID: {row[0]}, Nom: {row[1]}, Prénom: {row[2]}, Salaire: {row[3]} €, Service: {row[4]}")
        else:
            print("Aucun employé trouvé.")

# Connexion et ajout d'un employé
employe1 = Employe(nom="Patenne", prenom="Adeline", salaire=1800, id_service=1)
employe1.connecter()

# Ajouter l'employé
# employe1.ajouter_employe()

# Suppression de tous les employés "Adeline Patenne"
employe1.delete_employe_par_nom_prenom("Patenne", "Adeline")

# Afficher tous les employés restants
employe1.afficher_employes()

# Vérifier la connexion MySQL
if employe1.mydb.is_connected():
    db_info = employe1.mydb.get_server_info()
    print(f"\nConnecté à MySQL, version : {db_info}")

# Fermer la connexion à la base de données
employe1.fermer_connexion()
