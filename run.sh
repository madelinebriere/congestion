#!/bin/sh

sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo mn -c # clear environment
sudo python simulate.py
sudo python plot.py
