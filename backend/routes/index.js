var express = require('express');
var router = express.Router();
const { exec } = require('child_process');

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Simulador de Consola Interactiva' });
});

/* POST /execute - Ejecuta comandos en el servidor */
router.post('/execute', function (req, res) {
  const userCommand = req.body.command; // Comando enviado desde el cliente

  if (!userCommand || typeof userCommand !== 'string') {
    return res.status(400).json({ error: 'Comando inválido.' });
  }

  // Ejecutar el comando en la terminal del servidor
  exec(userCommand, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error al ejecutar el comando: ${error.message}`);
      return res.status(500).json({ error: `Error: ${error.message}` });
    }

    // Responder con la salida del comando
    res.json({ command: userCommand, output: stdout || stderr });
  });
});

module.exports = router;
