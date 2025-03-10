
-- Compter le nombre d'étudiants mineurs (âge < 18)
SELECT COUNT(*) AS nombre_etudiants_mineurs
FROM etudiant
WHERE age < 18;
