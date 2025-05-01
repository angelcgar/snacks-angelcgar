#!/bin/bash

NOMBRE_PROYECTO="nombre_proyecto_default"

primera_funcion() {
  echo "Iniciando instalacion limpia de un proyecto de React con vite"
  # ? Usar $1 o $2, por que se usa $1 para determinar cual eslinter usar y $2 para el nombre del proyecto
  pnpm create vite@latest "$1" --template react-ts
  cd "$1" || {
    echo "Error: No se pudo cambiar al directorio $1"
    exit 1
  }
  pnpm install
}

segunda_funcion() {
  echo "Hola desde la segunda función"
}

tercera_funcion() {
  echo "Hola desde la tercera función"
}

funcion_helper_1() {
  local nombre_proyecto=${1:-$NOMBRE_PROYECTO}
  primera_funcion "$nombre_proyecto"
  echo "donde estamos?"
  pwd
  # Supongo que aquí se puede empezar a cocinar con el proyecto, verdad?
  echo "Instalando Eslint"
  pnpm install -D eslint prettier eslint-plugin-react eslint-config-prettier eslint-plugin-prettier @typescript-eslint/eslint-plugin @typescript-eslint/parser
  echo "Configurando Eslint"
  cat >eslint.config.js <<EOF
import globals from "globals"; import react from "eslint-plugin-react"; import reactHooks from "eslint-plugin-react-hooks"; import reactRefresh from "eslint-plugin-react-refresh"; import tseslint from "typescript-eslint"; import prettier from "eslint-config-prettier"; import eslintPluginPrettier from "eslint-plugin-prettier"; export default tseslint.config({ ignores: ["dist", "node_modules"] }, { files: ["**/*.{ts,tsx}"], languageOptions: { parser: tseslint.parser, ecmaVersion: 2020, sourceType: "module", globals: globals.browser, parserOptions: { ecmaFeatures: { jsx: true } } }, plugins: { react, "@typescript-eslint": tseslint.plugin, "react-hooks": reactHooks, "react-refresh": reactRefresh, prettier: eslintPluginPrettier }, rules: { ...react.configs.recommended.rules, ...reactHooks.configs.recommended.rules, "react/jsx-uses-react": "off", "react/react-in-jsx-scope": "off", "react/jsx-uses-vars": "error", "react/display-name": "off", "react/prop-types": "off", "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }], "@typescript-eslint/explicit-module-boundary-types": "off", "react-refresh/only-export-components": ["warn", { allowConstantExport: true }], "prettier/prettier": "error" } }, { rules: {}, settings: { react: { version: "detect" } } }, { ...prettier });
EOF
  echo "Configurando prettier"
  touch .prettierrc
  cat >.prettierrc <<EOF
  { "semi": true, "singleQuote": true, "printWidth": 80, "tabWidth": 2, "trailingComma": "es5" }
EOF
  echo "Configurando prettier ignore"
  touch .prettierignore
  cat >.prettierignore <<EOF
# Ignora la carpeta de salida de Vite
dist
build

# Dependencias
node_modules

# Archivos de lock
package-lock.json
pnpm-lock.yaml
yarn.lock

# Configuraciones del entorno
.env
.env.*.local

# Salidas de prueba o cobertura
coverage
*.log

# Cache de herramientas
.vite
.eslintcache
EOF

  echo "Configurando eslint ignore"
  cat >.eslintignore <<EOF
# Ignora la carpeta de salida de Vite
dist
build
# Dependencias
node_modules
EOF

  echo "Todo listo para programar"
}

show_help() {
  echo "Uso: $0 [opciones]"
}

case "$1" in
"--use-eslint")
  if [ -z "$2" ]; then
    echo "Error: Se requiere un nombre de proyecto después de --use-eslint"
    exit 1
  fi
  usar_eslint=true
  funcion_helper_1 "$2"
  echo "Hola desde la función helper 1"
  ;;
"")
  echo "Hola desde la función por defecto"
  ;;
"" | "help" | "--help" | "-h")
  show_help
  ;;
esac
