

-- Insérer l'élève Martin Dupuis dans la table etudiant
INSERT INTO etudiant (nom, prenom, age, email) 
VALUES ('Dupuis', 'Martin', 18, 'martin.dupuis@laplateforme.io');

-- Récupérer les membres de la famille "Dupuis"
SELECT nom, prenom, age, email
FROM etudiant
WHERE nom = 'Dupuis';
