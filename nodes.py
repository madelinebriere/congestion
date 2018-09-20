#!/usr/bin/python                                                                                                                                                         
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class NodeGenerator(Topo):
    "Connect two hosts."
    def build(self):
	host1 = self.addHost('tcp-t')
	host2 = self.addHost('tcp-r')
	self.addLink(host1, host2)

def launchNet():
    "Create and test a 2-node network"
    topo = NodeGenerator()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    launchNet()
