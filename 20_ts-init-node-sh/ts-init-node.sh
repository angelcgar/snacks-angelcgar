#!/bin/bash

# Configuración
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración de rutas para plantillas
CONFIG_DIR="$HOME/.config/ts-init-node"
GITIGNORE_TEMPLATE="$CONFIG_DIR/gitignore.bash"
LICENSE_TEMPLATE="$CONFIG_DIR/LICENSE"

# Verificar dependencias
check_dependencies() {
  echo -e "${BLUE}🔍 Checking dependencies...${NC}"
  for cmd in jq pnpm git; do
    if ! command -v $cmd &>/dev/null; then
      echo -e "❌ Error: '$cmd' no está instalado" >&2
      exit 1
    fi
  done
  echo -e "${GREEN}✅ Dependencias verificadas${NC}"
}

# Cargar plantillas
load_templates() {
  source $GITIGNORE_TEMPLATE
  LICENSE_TEXT=$(<"$LICENSE_TEMPLATE")
}

# Inicializar proyecto
init_project() {
  [ -f "package.json" ] && {
    echo -e "❌ Error: package.json ya existe"
    exit 0
  }

  echo -e "${BLUE}🚀 Starting Node.js with TypeScript project setup...${NC}"
  pnpm init

  # Instalar dependencias
  echo -e "${GREEN}✅ Installing dependencies for development ${NC}"
  pnpm install -D typescript @types/node ts-node-dev rimraf

  # Configuración TypeScript
  npx tsc --init --outDir dist/ --rootDir src

  # Llamar a un Eslint
  init_biome

  # Instalar primeras dependencias
  init_dependencies
}

# TODO: Añadir reglas favoritas
init_biome() {
  echo -e "${GREEN}✅ Installing biome${NC}"
  pnpm add --save-dev --save-exact @biomejs/biome
  pnpm biome init
}

init_dependencies() {
  echo -e "${GREEN}✅ Installing dependencies for programming${NC}"
  pnpm i dotenv env-var
}

# Configuración Git
setup_git() {
  [ -d ".git" ] || git init

  if [ ! -f ".gitignore" ]; then
    echo -e "${GREEN}✅ Creating .gitignore${NC}"
    echo "$GITIGNORE" >.gitignore
  fi
}

# Configurar licencia
setup_license() {
  local year=$(date +%Y)
  local author=${GIT_NAME:-$(git config user.name || echo "Joe Doe")}

  echo -e "${GREEN}✅ Creating LICENSE${NC}"
  echo "${LICENSE_TEXT}" |
    sed "s/{{YEAR}}/$year/g" |
    sed "s/{{AUTHOR}}/$author/g" >LICENSE
}

# Estructura del proyecto
create_structure() {
  echo -e "${GREEN}✅ Creating project structure${NC}"
  mkdir -p src/
  cat >src/app.ts <<EOF
import 'dotenv/config';

console.log('Hello Node');
console.log('Environment:', process.env.NODE_ENV);
EOF

  echo "NODE_ENV=development" >.env
  echo "# $(basename "$PWD")" >README.md
}

# Main
check_dependencies
load_templates
init_project
setup_git
setup_license
create_structure

# TODO: añadir scripts para los tests
# Configurar scripts
jq 'del(.scripts.test) | .scripts += {
  "dev": "tsnd --respawn --clear src/app.ts",
  "build": "rimraf ./dist && tsc",
  "start": "npm run build && node dist/app.js"
}' package.json >temp.json && mv temp.json package.json

echo -e "${BLUE}🎉 Project setup completed successfully!${NC}"
echo -e "${BLUE}📝 Start developing with:${NC} ${GREEN}pnpm run dev${NC}"
