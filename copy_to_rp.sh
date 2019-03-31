#!/bin/sh

sudo tar -czf rcv.tar.gz --exclude=".git" --exclude="*.mp4" --exclude="*.avi" --exclude="__pycache__" --exclude="*.pyc" -C /mnt/c/Projects/Robotics/Open-CV/src/ rcv
scp rcv.tar.gz pi@192.168.2.102:~
sudo rm -f rcv.tar.gz
ssh pi@192.168.2.102 'sudo systemctl stop rcv.service'
ssh pi@192.168.2.102 'sudo rm -rf rcv'
ssh pi@192.168.2.102 'sudo tar -xzf rcv.tar.gz'
ssh pi@192.168.2.102 'sudo rm -f rcv.tar.gz'
ssh pi@192.168.2.102 'sudo systemctl daemon-reload'
ssh pi@192.168.2.102 'sudo systemctl start rcv.service'
