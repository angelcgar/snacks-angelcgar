#!/bin/bash

if [ "$1" == "new" ]; then
  echo "Creando nuevo proyecto..."

  if [ -z "$2" ]; then
    echo "No se ha especificado el nombre del proyecto"
    exit 1
  else
    mkdir $2
    cd $2
    git init
    touch README.md
    echo "# " >>README.md
    cp ~/Documentos/plantillas/youtube/templete.md .
    git add .
    git commit -m "Initial commit"
    echo "Proyecto creado con éxito"
  fi

else
  echo "No hay argumentos"
fi
