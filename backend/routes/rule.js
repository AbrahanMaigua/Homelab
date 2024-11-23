const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const db = require("../db"); // Importar la configuración de la base de datos
const app = express();
const router = express.Router();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Rutas CRUD
// Crear un nuevo item (C)
router.post("/items", async (req, res) => {
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ error: "El campo 'name' es obligatorio." });
  }

  try {
    const result = await db.query(
      `INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id`,
      [name, description]
    );
    res.status(201).json({ id: result.rows[0].id });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Leer todos los items (R)
router.get("/items", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM items");
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Leer un item por ID (R)
router.get("/items/:id", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM items WHERE id = $1", [
      req.params.id,
    ]);
    if (result.rows.length === 0)
      return res.status(404).json({ error: "Item no encontrado." });
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Actualizar un item por ID (U)
router.put("/items/:id", async (req, res) => {
  const { name, description } = req.body;
  try {
    const result = await db.query(
      "UPDATE items SET name = $1, description = $2 WHERE id = $3 RETURNING *",
      [name, description, req.params.id]
    );
    if (result.rowCount === 0)
      return res.status(404).json({ error: "Item no encontrado." });
    res.json({ message: "Item actualizado correctamente." });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Eliminar un item por ID (D)
router.delete("/items/:id", async (req, res) => {
  try {
    const result = await db.query("DELETE FROM items WHERE id = $1 RETURNING id", [
      req.params.id,
    ]);
    if (result.rowCount === 0)
      return res.status(404).json({ error: "Item no encontrado." });
    res.json({ message: "Item eliminado correctamente." });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Leer todos los rules (R)
router.get("/rule", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM rule");
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Leer un rule por ID (R)
router.get("/rule/:id", async (req, res) => {
  try {
    const result = await db.query(
      `
      SELECT rule.id, rule.name, rule.rules, items.name AS item_name
      FROM rule
      JOIN items ON rule.item_id = items.id
      WHERE rule.id = $1
      `,
      [req.params.id]
    );
    if (result.rows.length === 0)
      return res.status(404).json({ error: "Rule no encontrado." });
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Crear un nuevo rule (C)
router.post("/rule", async (req, res) => {
  const { name, rules, item_id, type } = req.body;
  if (!name || !rules || !item_id || !type) {
    return res
      .status(400)
      .json({ error: "Los campos 'name', 'rules', 'item_id' y 'type' son obligatorios." });
  }
  try {
    const result = await db.query(
      `INSERT INTO rule (name, rules, item_id, type) VALUES ($1, $2, $3, $4) RETURNING id`,
      [name, rules, item_id, type]
    );
    res.status(201).json({ id: result.rows[0].id, message: "Rule creado correctamente." });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Resto de rutas se adaptan de forma similar...

module.exports = router;
