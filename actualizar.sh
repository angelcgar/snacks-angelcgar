#!/bin/bash

# Lista de paquetes que NO se deben actualizar
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
    gcc-libs
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
    linux
    linux-headers 
    cloudflared
    cmake
    containerd
    archlinux-tweak-tool-git
    arcolinux-sddm-simplicity-git
    arcolinux-system-config-git 
    audacity
    ffmpeg
    gettext
    glib2 
    glib2-devel
    grub
    libmupdf
    man-pages
    networkmanager
    noto-fonts
    nss        
    nwg-look    
    oh-my-zsh-git
    opencv
    papirus-icon-theme
    snapd
    linux-firmware
    linux-firmware-marvell
    linux-firmware-whence
)

# Convertir la lista de exclusiones en un formato que pacman entienda
EXCLUDE_STRING=$(printf " --ignore %s" "${EXCLUDE_PKGS[@]}")

# Actualizar el sistema, excluyendo los paquetes especificados
echo "Actualizando el sistema, excluyendo paquetes específicos..."
sudo pacman -Syu $EXCLUDE_STRING #--noconfirm

echo "¡Proceso completado!"
