#!/usr/bin/python                                                                                                                                                         
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

from argparse import ArgumentParser
from subprocess import Popen
from time import sleep, time

import sys

# Authors: Maddie Briere and Jesse Yue

# References:
# - Bufferbloat by huangty (2018).
# - Introduction to Mininet by Lantz et. al (2017).

# Parse arguments.
parse = ArgumentParser(description = "Congestion variables")
parse.add_argument('--bw', '-b',
	dest="bw_in",
	type = float,
	action = "store",
	help="Bandwidth of host links",
	default = 10)

parse.add_argument('--delay', '-d',
	dest = "delay_in",
	action="store",
	help="Delay in ms of host links",
	default = '5ms')

parse.add_argument('--qsize', '-q',
	dest="qsize_in",
	type = float,
	action="store",
	help="Max buffer size",
	default = 1000)

parse.add_argument('--loss', '-l',
	dest="loss_in",
	type = float,
	help = "Percentage of packets lost",
	action= "store",
	default=2)

args=parse.parse_args()

class NodeGenerator(Topo):
    "Connect two hosts."
    def build(self):
	switch = self.addSwitch('s1')
	host1 = self.addHost('tcp-t', ip='10.0.0.1')
	host2 = self.addHost('tcp-r', ip='10.0.0.2')
	self.addLink(host1, switch, bw=args.bw_in, delay=args.delay_in,
		loss = args.loss_in, max_queue_size = args.qsize_in);
	self.addLink(host2, switch, bw=args.bw_in, delay=args.delay_in,
		loss = args.loss_in, max_queue_size = args.qsize_in);

def launchNet():
	"Create and test a 2-node network"
	print "Starting network"
	seconds = 3600
	start = time()

	topo = NodeGenerator()
	net = Mininet(topo, link=TCLink)
	net.start();

    	# Retrieve nodes.
	h1 = net.getNodeByName('tcp-t')
	h2 = net.getNodeByName('tcp-r')

    	# Launch basic traffic ... measure bandwidth.
    	# Reference: How to generate traffic in a network topology.
    	# Shivakumar 2013
	print "Launching iperf: Measuring BW"
	h2.cmd('iperf -s -w 16m -p 5001 -i 1 > iperf-recv.txt &')

	print "Launching ping: Measuring RTTM"
	h1.cmd('ping -c 7200 -i .5 -w 3 10.0.0.2 > ping-recv.txt &')

	print "Streaming large file"
	h2.cmd('nc -l 5001 > /dev/null/')
	h1.cmd('nc 10.0.0.2 5001 < big_file.txt')

	net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    # setLogLevel('info')
    launchNet()
