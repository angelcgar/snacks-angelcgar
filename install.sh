nombre_programa="ts-init-node"
nombre_helpers="gitignore"

if [ -e "~/.local/bin/$nombre_programa" ]; then
  rm ~/.local/bin/$nombre_programa
fi

if [ -e "~/.local/bin/$nombre_helpers" ]; then
  rm ~/.local/bin/$nombre_helpers
fi

cp $nombre_programa.sh ~/.local/bin/$nombre_programa
cp $nombre_helpers.bash ~/.local/bin/$nombre_helpers.bash

echo "$nombre_programa instalado correctamente"
