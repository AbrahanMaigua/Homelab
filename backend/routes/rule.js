const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const sqlite3 = require("sqlite3").verbose();

const app = express();
var router = express.Router();


// Middleware
app.use(cors());
app.use(bodyParser.json());

// Base de datos SQLite
const db = new sqlite3.Database(":memory:");

// Crear tabla en la base de datos
db.serialize(() => {
  db.run(`
    CREATE TABLE items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      description TEXT
    );

    CREATE TABLE rule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rules TEXT,
        item_id INTEGER,
        type TEXT,
        FOREIGN KEY (item_id) REFERENCES items (id)
    );
  `);
  console.log("Tabla 'items' creada.");
});

// Rutas CRUD
// Crear un nuevo item (C)
app.post("/items", (req, res) => {
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ error: "El campo 'name' es obligatorio." });
  }
  const query = `INSERT INTO items (name, description) VALUES (?, ?)`;
  db.run(query, [name, description], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.status(201).json({ id: this.lastID });
  });
});

// Leer todos los items (R)
app.get("/items", (req, res) => {
  const query = `SELECT * FROM items`;
  db.all(query, [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Leer un item por ID (R)
app.get("/items/:id", (req, res) => {
  const query = `SELECT * FROM items WHERE id = ?`;
  db.get(query, [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: "Item no encontrado." });
    res.json(row);
  });
});

// Actualizar un item por ID (U)
app.put("/items/:id", (req, res) => {
  const { name, description } = req.body;
  const query = `UPDATE items SET name = ?, description = ? WHERE id = ?`;
  db.run(query, [name, description, req.params.id], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    if (this.changes === 0)
      return res.status(404).json({ error: "Item no encontrado." });
    res.json({ message: "Item actualizado correctamente." });
  });
});

// Eliminar un item por ID (D)
app.delete("/items/:id", (req, res) => {
  const query = `DELETE FROM items WHERE id = ?`;
  db.run(query, [req.params.id], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    if (this.changes === 0)
      return res.status(404).json({ error: "Item no encontrado." });
    res.json({ message: "Item eliminado correctamente." });
  });
});

app.post("/items", (req, res) => {
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ error: "El campo 'name' es obligatorio." });
  }
  const query = `INSERT INTO items (name, description) VALUES (?, ?)`;
  db.run(query, [name, description], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.status(201).json({ id: this.lastID });
  });
});

// Leer todos los rules (R)
app.get("/rule", (req, res) => {
  const query = `SELECT * FROM rule`;
  db.all(query, [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Leer un rule por ID (R)
app.get("/rule/:id", (req, res) => {
  const query = `
    SELECT rule.id, rule.name, rule.rules, items.name AS item_name
    FROM rule
    JOIN items ON rule.item_id = items.id
    WHERE rule.id = ?;
  `;
  db.get(query, [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: "Rule no encontrado." });
    res.json(row);
  });
});

// Crear un nuevo rule (C)
app.post("/rule", (req, res) => {
  const { name, rules, item_id, type } = req.body;
  if (!name || !rules || !item_id || !type) {
    return res
      .status(400)
      .json({ error: "Los campos 'name', 'rules', 'item_id' y 'type' son obligatorios." });
  }
  const query = `INSERT INTO rule (name, rules, item_id, type) VALUES (?, ?, ?, ?)`;
  db.run(query, [name, rules, item_id, type], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.status(201).json({ id: this.lastID, message: "Rule creado correctamente." });
  });
});

// Actualizar un rule por ID (U)
app.put("/rule/:id", (req, res) => {
  const { name, rules, type, item_id } = req.body;
  const query = `
    UPDATE rule 
    SET name = ?, rules = ?, type = ?, item_id = ? 
    WHERE id = ?`;
  db.run(query, [name, rules, type, item_id, req.params.id], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    if (this.changes === 0)
      return res.status(404).json({ error: "Rule no encontrado." });
    res.json({ message: "Rule actualizado correctamente." });
  });
});

// Eliminar un rule por ID (D)
app.delete("/rule/:id", (req, res) => {
  const query = `DELETE FROM rule WHERE id = ?`;
  db.run(query, [req.params.id], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    if (this.changes === 0)
      return res.status(404).json({ error: "Rule no encontrado." });
    res.json({ message: "Rule eliminado correctamente." });
  });
});


module.exports = router;
