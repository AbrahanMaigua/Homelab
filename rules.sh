#!/bin/bash
set +x
# CLI para manejar argumentos
if [ $# -eq 0 ]; then
  echo "Uso: $0 <comando> [opciones]"
  echo "Comandos disponibles:"
  echo "  rule add    <name>  <description>"
  echo "  rule delete <id>"
  echo "  rule update <id> <name> <description>"
  echo "  rule view   <id>"
  echo "  rule list"
  exit 1
fi

# Función para agregar un ítem
function add() {
  # Escapar correctamente las variables pasadas
  local id="$1"
  local name="$2"
  local rules="$3"
  local item_id="$4"
  local type="$5"

  # Usar el nombre y la descripción en el cuerpo de la solicitud
  response=$(curl  -s -X POST "$URL_API/api/rule" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$name\", 
         \"rules\": \"$rules\",
         \"item_id\": \"$item_id\",
         \"type\": \"$type\"}",)

  # Mostrar la respuesta
  echo "$response"
}

# Función para eliminar un ítem
function delete() {
  response=$(curl -s -X DELETE "$URL_API/api/rule/$1" \
    -H "Content-Type: application/json")
  echo "$response"
}

# Función para actualizar un ítem
function update() {
  local id="$1"
  local name="$2"
  local rules="$3"
  local item_id="$4"
  local type="$5"



  response=$(curl -s -X PUT "$URL_API/api/rule/$id" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$name\", 
         \"rules\": \"$rules\",
         \"item_id\": \"$item_id\",
         \"type\": \"$type\"}",)

  echo "$response"
}

# Función para ver todos los ítems
function view() {
  response=$(curl -s -X GET "$URL_API/api/rule" \
    -H "Content-Type: application/json")
  echo "$response"
}

# Función para obtener un ítem específico por su ID
function list() {
  response=$(curl -s -X GET "$URL_API/api/rule/$1" \
    -H "Content-Type: application/json")
  echo "$response"
}

# Ejecutar la función con parámetros pasados al script
if [ "$1" == "add" ]; then
    add $2 $3 $4 $5 
else [ "$1" == "list" ]; then
    list 
else [ "$1" == "rm" ]; then
    delete $2
else [ "$1" == "view" ]; then
    view $2
else [ "$1" == "update" ]; then
    update $2 $3 $4 $5 
else
  echo "Comando no válido"
fi