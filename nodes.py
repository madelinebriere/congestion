#!/usr/bin/python                                                                                                                                                         
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import sys

class NodeGenerator(Topo):
    "Connect two hosts."
    def build(self):
	if len(sys.argv) - 1 <= 0:
		bw_in = 10
	else: 
		bw_in = int(sys.argv[1])

	if len(sys.argv) - 1 <= 1:
		delay_in = '5ms'
	else:
		delay_in = sys.argv[2]

	if len(sys.argv) - 1 <= 2:
		loss_in	= 2
	else:
		loss_in = int(sys.argv[3])

	if len(sys.argv) - 1 <= 3:
		qsize_in = 1000
	else:
		qsize_in = int(sys.argv[4])

	switch = self.addSwitch('s1')
	host1 = self.addHost('tcp-t')
	host2 = self.addHost('tcp-r')
	self.addLink(host1, switch, bw=bw_in, delay=delay_in,
		loss = loss_in, max_queue_size = qsize_in);
	self.addLink(host2, switch, bw=bw_in, delay=delay_in,
		loss = loss_in, max_queue_size = qsize_in);

def launchNet():
    "Create and test a 2-node network"
    topo = NodeGenerator()
    net = Mininet(topo, link=TCLink)
    net.start()
    # TODO: Measure BW using iperf.
    # TODO: Measure RTT using ping.
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    # setLogLevel('info')
    launchNet()
