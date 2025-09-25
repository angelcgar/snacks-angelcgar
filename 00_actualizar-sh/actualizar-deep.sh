#!/bin/bash

# Lista de paquetes que NO se deben actualizar
EXCLUDE_PKGS=(
    brave-bin
    firefox
    intellij-idea-community-edition
    thunderbird
    visual-studio-code-bin
    libreoffice-fresh
    libreoffice-fresh-es
    kdenlive
    okular
    vlc
    warp-terminal
    wine
    audacity
    linux
    linux-headers
    linux-firmware
    linux-firmware-marvell
    linux-firmware-whence
    virtualbox
    virtualbox-host-modules-arch
    docker
    docker-compose
    snapd
)

# Verificar si pacman está instalado
if ! command -v pacman &> /dev/null; then
    echo "Error: pacman no está instalado. Este script es solo para sistemas basados en Arch Linux."
    exit 1
fi

# Convertir la lista de exclusiones en un formato que pacman entienda
EXCLUDE_STRING=$(printf " --ignore %s" "${EXCLUDE_PKGS[@]}")

# Mostrar los paquetes que se excluirán
echo "==================================================="
echo "Excluyendo los siguientes paquetes de la actualización:"
for pkg in "${EXCLUDE_PKGS[@]}"; do
    echo " - $pkg"
done
echo "==================================================="

# Actualizar el sistema, excluyendo los paquetes especificados
echo "Iniciando la actualización del sistema..."
sudo pacman -Syu $EXCLUDE_STRING

# Verificar si la actualización fue exitosa
if [ $? -eq 0 ]; then
    echo "==================================================="
    echo "¡Actualización completada con éxito!"
    echo "==================================================="
else
    echo "==================================================="
    echo "Hubo un error durante la actualización. Por favor, revisa los mensajes anteriores."
    echo "==================================================="
    exit 1
fi
