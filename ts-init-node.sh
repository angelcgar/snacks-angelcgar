#! /bin/bash

# Colors for messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# todo: testear este bloque de codigo
# Verificar si jq está instalado
echo -e "${BLUE}🔍 Checking dependencies...${NC}"
if ! command -v jq &>/dev/null; then
  echo "❌Error: 'jq' no está instalado. Por favor, instálalo antes de continuar." >&2
  exit 1
fi

echo "'jq' está instalado. Continuando..."

# Verificar si pnpm está instalado
if ! command -v pnpm &>/dev/null; then
  echo "❌Error: 'pnpm' no está instalado. Por favor, instálalo antes de continuar." >&2
  exit 1
fi

# Verificar si git está configurado
if [ -z "$GIT_NAME" ] || [ -z "$GIT_EMAIL" ]; then
  echo "❌ Error: Git user.name or user.email are not configured"
  exit 1
fi

# Verificar si ya existe un package.json
if [ -f "package.json" ]; then
  echo "El archivo package.json ya existe. No se realizarán cambios."
  exit 0
fi

# Inicializamos el proyecto
echo -e "${BLUE}🚀 Starting Node.js with TypeScript project setup...${NC}"
pnpm init

echo -e "${GREEN}✅ Installing TypeScript dependencies${NC}"
pnpm i -D typescript @types/node ts-node-dev rimraf

echo -e "${GREEN}✅ Installing and configuring biome${NC}"
pnpm add --save-dev --save-exact @biomejs/biome
# TODO: Agregar configuración de biome

# Iniciamos el proyecto TypeScript
npx tsc --init --outDir dist/ --rootDir src

# Recursos para gitignore
source gitignore.bash

# TODO: Agregar configuración para jest
echo -e "${GREEN}✅ Configuring package.json${NC}"

# Eliminamos el primer script de test
jq "del(.scripts.test)" package.json >tempackage.json && mv tempackage.json package.json

# Agregamos los scripts de desarrollo, construcción y ejecución
jq '.scripts += {
  "dev": "tsnd --respawn --clear src/app.ts",
  "build": "rimraf ./dist && tsc",
  "start": "npm run build && node dist/app.js"
}' package.json >temp.json && mv temp.json package.json

# Inicializar repositorio Git
if [ ! -d ".git" ]; then
  echo "Inicializando repositorio Git..."

  git init
fi

# Inicializar configuración de Git
if [ ! -f ".gitignore" ]; then
  touch .gitignore

  echo "$GITIGNORE" >>.gitignore
fi

echo "Repositorio Git ya está inicializado."

# crear Readme
echo -e "${GREEN}✅ Creating README.md${NC}"
echo "# $(basename "$PWD")" >README.md

# Crear LICENSE

echo -e "${GREEN}✅ Creating LICENSE${NC}"

# TODO: Sacar este texto a un archivo
cat >LICENSE <<EOF
MIT License

Copyright (c) $(date +%Y) $GIT_NAME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

echo -e "${GREEN}✅ Creating project structure${NC}"

mkdir src/
touch src/app.ts

cat >src/index.ts <<EOF
import 'dotenv/config';

console.log('Hello Node');
console.log('Environment:', process.env.NODE_ENV);
EOF

echo -e "${GREEN}✅ Setting up environment variables${NC}"
echo "NODE_ENV=development" >.env

# TODO: Agregar Github Actions

echo -e "${GREEN}✅ Installing dotenv${NC}"
pnpm install dotenv env-var

echo "${BLUE}🎉 Project setup completed successfully!${NC}"
echo "${BLUE}📝 You can start developing with:${NC}"
echo "${GREEN}   pnpm run dev${NC}"
