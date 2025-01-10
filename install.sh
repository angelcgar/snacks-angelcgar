if [ -e "~/.local/bin/ts-init-node" ]; then
  rm ~/.local/bin/ts-init-node
fi

cp ts-init-node.sh ~/.local/bin/ts-init-node
