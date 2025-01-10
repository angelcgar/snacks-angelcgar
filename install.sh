if [ -e "~/.local/bin/today" ]; then
  rm ~/.local/bin/today
fi

cp today.sh ~/.local/bin/today
