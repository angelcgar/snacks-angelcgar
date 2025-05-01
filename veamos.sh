#!/bin/bash

primera_funcion() {
  echo "Hola desde la primera función"
}

segunda_funcion() {
  echo "Hola desde la segunda función"
}

tercera_funcion() {
  echo "Hola desde la tercera función"
}

funcion_helper_1() {
  primera_funcion
}

show_help() {
  echo "Uso: $0 [opciones]"
}

case "$1" in
"--parametro")
  funcion_helper_1
  echo "Hola desde la función helper 1"
  ;;
"")
  echo "Hola desde la función por defecto"
  ;;
"" | "help" | "--help" | "-h")
  show_help
  ;;
esac
