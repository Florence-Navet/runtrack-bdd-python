
-- Récupérer les informations de l'étudiant le plus âgé
SELECT nom, prenom, age, email
FROM etudiant
ORDER BY age DESC
LIMIT 1;
