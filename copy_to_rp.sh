#!/bin/sh

sudo tar -czf rcv.tar.gz --exclude=".git" --exclude="*.mp4" --exclude="*.avi" --exclude="__pycache__" --exclude="*.pyc" -C /mnt/c/Projects/Robotics/OpenCV rcv
scp rcv.tar.gz pi@10.0.0.2:~
sudo rm -f rcv.tar.gz
ssh pi@10.0.0.2 'sudo rm -rf rcv'
ssh pi@10.0.0.2 'sudo tar -xzf rcv.tar.gz'
ssh pi@10.0.0.2 'sudo rm -f rcv.tar.gz'