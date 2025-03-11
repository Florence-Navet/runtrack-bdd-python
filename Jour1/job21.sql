
-- Compter le nombre d'étudiants dont l'âge est compris entre 18 et 25 ans
SELECT COUNT(*) AS nombre_etudiants_18_25
FROM etudiant
WHERE age BETWEEN 18 AND 25;
