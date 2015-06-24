#!/bin/bash

if [[ "$1" == "stack" && "$2" == "install" ]]; then
    cd /home/ubuntu
    git clone https://github.com/Nexenta/cinder.git
    cp -r cinder/cinder/volume/drivers/nexenta /opt/stack/cinder/cinder/volume/drivers
fi