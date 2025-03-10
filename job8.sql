-- Création de la table etudiant
CREATE TABLE etudiant (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(25) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Insérer des étudiants dans la table etudiant
INSERT INTO etudiant (nom, prenom, age, email) VALUES
('Spaghetti', 'Betty', 23, 'betty.spaghetti@laplateforme.io'),
('Steak', 'Chuck', 45, 'chuck.steak@laplateforme.io'),
('Doe', 'John', 18, 'john.doe@laplateforme.io'),
('Barnes', 'Binkie', 16, 'binkie.barnes@laplateforme.io'),
('Dupuis', 'Gertrude', 20, 'gertrude.dupuis@laplateforme.io');

-- Sélectionner la liste des étudiants de moins de 18 ans
SELECT * FROM etudiant WHERE age < 18;