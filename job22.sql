
-- Récupérer les informations de l'étudiant le plus jeune
SELECT nom, prenom, age, email
FROM etudiant
ORDER BY age ASC
LIMIT 1;
