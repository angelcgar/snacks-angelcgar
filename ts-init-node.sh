#! /bin/bash

# Verificar si ya existe un package.json
if [ -f "package.json" ]; then
  echo "El archivo package.json ya existe. No se realizarán cambios."
  exit 0
fi

pnpm init

pnpm i -D typescript @types/node ts-node-dev rimraf

npx tsc --init --outDir dist/ --rootDir src

source gitignore.bash

# todo: testear este bloque de codigo
# Verificar si jq está instalado
if ! command -v jq &> /dev/null; then
  echo "Error: 'jq' no está instalado. Por favor, instálalo antes de continuar." >&2
  exit 1
fi

echo "'jq' está instalado. Continuando..."

# jp: dependencia externa, para prosesar archivos json
jq '.scripts += {
  "dev": "tsnd --respawn --clear src/app.ts",
  "build": "rimraf ./dist && tsc",
  "start": "npm run build && node dist/app.js"
}' package.json > temp.json && mv temp.json package.json

if [ ! -d ".git" ]; then
  echo "Inicializando repositorio Git..."

  git init
fi

if [ ! -f ".gitignore" ]; then
  touch .gitignore

  echo "$GITIGNORE" >> .gitignore
fi

echo "Repositorio Git ya está inicializado."

mkdir src/
touch src/app.ts

echo "console.log(\"A programar\")" > src/app.ts

echo ""

echo "A programar 🚀"
