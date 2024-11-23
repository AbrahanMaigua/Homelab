require('dotenv').config(); // Carga variables de entorno
const { Pool } = require('pg');

// Configurar conexión a PostgreSQL
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_DATABASE,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

(async () => {
  try {
    // Conexión a la base de datos
    const client = await pool.connect();

    // Crear las tablas
    await client.query(`
      CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
      );
    `);

    console.log("Tabla 'items' creada.");

    await client.query(`
      CREATE TABLE IF NOT EXISTS rule (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        rules TEXT,
        item_id INTEGER,
        type TEXT,
        FOREIGN KEY (item_id) REFERENCES items (id)
      );
    `);

    console.log("Tabla 'rule' creada.");

    // Cerrar conexión
    client.release();
  } catch (err) {
    console.error("Error al crear tablas:", err);
  } 
})();

module.exports = {
  query: (text, params) => pool.query(text, params),
};
