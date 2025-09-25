nombre_programa="actualizar_arch_personal"

if [ -e "~/.local/bin/$nombre_programa" ]; then
  rm ~/.local/bin/$nombre_programa
fi

cp actualizar.sh ~/.local/bin/$nombre_programa

