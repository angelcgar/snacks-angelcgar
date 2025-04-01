#!/bin/bash

if [ "$1" == "new" ]; then
  echo "Creando nuevo proyecto..."

  if [ -z "$2" ]; then
    echo "No se ha especificado el nombre del proyecto"
    echo "Intente yv new nombre-proyecto"
    exit 1
  else
    mkdir $2
    cd $2
    #Primera carpeta
    mkdir 01_Grabacion/
    cd 01_Grabacion/
    mkdir "[Archivos de Audio Raw]"/
    mkdir "[Archivos de Video Raw]"/
    cd ..
    #Segunda carpeta
    mkdir 02_Edicion/
    cd 02_Edicion/
    mkdir Proyecto_[$2].kdenlive/
    mkdir Exportaciones/
    cd Exportaciones/
    mkdir [$2]_V1.mp4/
    mkdir [$2]_Miniatura.jpg/
    cd ..
    cd ..
    #Tercera carpeta
    mkdir 03_Recursos/
    cd 03_Recursos/
    mkdir Musica/
    mkdir Imagenes/
    mkdir Graficos/
    cd ..
    #Cuarta carpeta
    mkdir 04_Guion/
    cd 04_Guion/
    mkdir Guion_[$2].docx/
    mkdir Notas_[$2].txt/
    cd ..
    git init
    touch README.md
    echo "# " >>README.md
    cp ~/Documentos/plantillas/youtube/templete.md .
    git add .
    git commit -m "Initial commit"
    echo "Proyecto creado con éxito"
  fi

elif [ "$1" == "help" ]; then
  echo "intenta yv new nuevo-proyecto"
  exit 1
else
  echo "No hay argumentos"
fi
