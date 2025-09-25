#!/bin/bash

if [ -z "$1" ]; then
  echo "Uso: ./gh-helper <patrón> [límite]"
  exit 1
fi

PATRON="$1"
LIMITE="${2:-150}"  # por defecto 150

gh repo list --limit "$LIMITE" --json name,url \
  -q ".[] | select(.name | test(\"$PATRON\"; \"i\")) | \"\(.name): \(.url)\""
