#!/bin/env bash
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y git libgpiod-dev socat
sudo nmcli con modify "Wired connection 1" ipv4.method manual ipv4.addresses 192.168.7.2/24

sudo apt install python3-pip 
pip install pi-plates --break-system-packages
pip install pyyaml --break-system-packages 
pip install sm16relind --break-system-packages 
pip install sm8mosind --break-system-packages 
pip install smtc --break-system-packages 

cd ~/ 
git clone https://github.com/SequentMicrosystems/8mosind-rpi.git 
cd ~/8mosind-rpi 
sudo make install

cd ~/ 
git clone https://github.com/SequentMicrosystems/16relind-rpi.git 
cd ~/16relind-rpi 
sudo make install 

cd ~/ 
git clone https://github.com/SequentMicrosystems/smtc-rpi.git 
cd ~/smtc-rpi 
sudo make install 

cd ~/ 
git clone https://github.com/SequentMicrosystems/SmartFan-rpi.git 
cd ~/SmartFan-rpi 
sudo make install 

cd ~/
git clone https://github.com/SequentMicrosystems/megaind-rpi.git
cd ~/megaind-rpi
sudo make install

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

cd ~/ 
cp picode/{*.py,*.sh,*.yaml} ~/

sed -i "s/USER/$(whoami)/g" picode/wd_run.service
sudo cp picode/wd_run.service /etc/systemd/system/wd_run.service
sudo systemctl daemon-reload
sudo systemctl enable wd_run.service
