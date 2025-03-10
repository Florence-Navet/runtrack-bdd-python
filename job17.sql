-- Modifier l'âge de Betty Spaghetti de 23 ans à 20 ans
UPDATE etudiant
SET age = 20
WHERE nom = 'Spaghetti' AND prenom = 'Betty';


-- Vérifier les informations de Betty Spaghetti après la modification
SELECT nom, prenom, age, email
FROM etudiant
WHERE nom = 'Spaghetti' AND prenom = 'Betty';