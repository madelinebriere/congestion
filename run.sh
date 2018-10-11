#!/bin/sh

sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo apt-get install python-numpy python-scipy python-matplotlib
sudo mn -c # clear environment
sudo python simulate.py
sudo python plot.py
