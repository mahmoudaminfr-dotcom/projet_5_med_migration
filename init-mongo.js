// 1. On bascule sur la base de données médicale de l'hôpital
db = db.getSiblingDB('healthcare_db');

// 2. Récupération dynamique et nettoyage des retours chariots (\r) invisibles sous Windows
const username = (process.env.MONGO_USER || '').trim();
const password = (process.env.MONGO_PASS || '').trim();

// 3. Création de l'utilisateur applicatif avec son niveau de sécurité restreint (readWrite uniquement)
db.createUser({
  user: username,
  pwd: password,
  roles: [
    {
      role: 'readWrite',       // Niveau de sécurité : Lecture et Écriture uniquement
      db: 'healthcare_db'      // Périmètre : Uniquement cette base de données
    }
  ]
});