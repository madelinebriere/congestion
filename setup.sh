#!/bin/sh

git clone git@github.com:madelinebriere/congestion
sudo apt-get -y screen
sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo apt-get install python-numpy python-scipy python-matplotlib
