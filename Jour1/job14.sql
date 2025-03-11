
-- Récupérer les élèves dont l'âge est compris entre 18 et 25 ans, triés par âge croissant
SELECT nom, prenom, age, email
FROM etudiant
WHERE age BETWEEN 18 AND 25
ORDER BY age ASC;
