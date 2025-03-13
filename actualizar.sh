#!/bin/bash

# Lista de paquetes que NO se deben actualizar (IDEs, navegadores, herramientas pesadas, etc.)
EXCLUDE_PKGS=(
    brave-bin
    firefox
    intellij-idea-community-edition
    thunderbird
    visual-studio-code-bin
    libreoffice
    docker
    docker-compose
    gcc
    git
    github-cli
    go
    jdk21-openjdk
    jdk-openjdk
    kdenlive 
    kdeconnect
    libreoffice-fresh
    libreoffice-fresh-es
    okular
    virtualbox
    virtualbox-host-modules-arch
    vlc
    warp-terminal 
    wine
    cloudflared
    containerd
    snapd
)

# Generar la cadena de exclusión para pacman
EXCLUDE_STRING=$(printf " --ignore %s" "${EXCLUDE_PKGS[@]}")

# Ejecutar actualización con exclusión de paquetes pesados
echo "Actualizando el sistema, excluyendo paquetes no esenciales..."
sudo pacman -Syu $EXCLUDE_STRING #--noconfirm

echo "¡Actualización completada!"
