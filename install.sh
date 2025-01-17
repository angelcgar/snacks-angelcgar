nombre_programa="ts-init-node"

if [ -e "~/.local/bin/$nombre_programa" ]; then
  rm ~/.local/bin/$nombre_programa
fi

cp $nombre_programa.sh ~/.local/bin/$nombre_programa

echo "$nombre_programa instalado correctamente"
