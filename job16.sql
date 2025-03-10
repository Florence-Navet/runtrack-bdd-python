
-- Récupérer tous les élèves dont le prénom commence par 'B'
SELECT nom, prenom, age, email
FROM etudiant
WHERE prenom LIKE 'B%';
