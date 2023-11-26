#!/bin/bash -v
MEDIA_DIRS=1900 1910 1920 1930 1940 1950 1960 1970 1980 1990 2000 2010 sfx
INSTALL_ROOT=$(cwd)

echo "installing pre-requisites"
sudo apt install sox libsox-fmt-all bc -y

echo "installing systemd daemons"
sudo cp systemd-files/* /lib/systemd/system/
sudo systemctl daemon-reload
#sudo systemctl enable time-machine-radio-low-power-daemon.service
#sudo systemctl enable time-machine-radio-power-switch-daemon.service
sudo systemctl enable time-machine-radio.service
sudo systemctl enable time-machine-radio-volume-daemon.service

echo "configuring sound device for soft-volume"
cp .asoundrc "$HOME"

echo "setting up media directories"
for y in $MEDIA_DIRS; do mkdir "$INSTALL_ROOT/media/$y"; done