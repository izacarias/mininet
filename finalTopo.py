#!/usr/bin/python

# Executar com o comando:
# sudo mn --custom finalTopo.py --topo finaltopo [...]

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class FinalTopo (Topo):
    "My Topo for multipath"

    def __init__(self):

        Topo.__init__(self)

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        ap2 = self.addSwitch('ap2', dpid="0000000000001002")
        ap3 = self.addSwitch('ap3', dpid="0000000000001003")
        ap4 = self.addSwitch('ap4', dpid="0000000000001004")
        ap5 = self.addSwitch('ap5', dpid="0000000000001005")
        ap7 = self.addSwitch('ap7', dpid="0000000000001007")
        ap8 = self.addSwitch('ap8', dpid="0000000000001008")
        ap9 = self.addSwitch('ap9', dpid="0000000000001009")
        ap10 = self.addSwitch('ap10', dpid="0000000000001010")

        topMiddleSwitch = self.addSwitch('s1', dpid="0000000000000001")
        topLeftSwitch = self.addSwitch('s7', dpid="0000000000000007")
        topRightSwitch = self.addSwitch('s8', dpid="0000000000000008")

        topMiddleLeftSwitch = self.addSwitch('s2', dpid="0000000000000002")
        topMiddleRightSwitch = self.addSwitch('s3', dpid="0000000000000003")

        bottomMiddleLeftSwitch = self.addSwitch('s4', dpid="0000000000000004")
        bottomMiddleRightSwitch = self.addSwitch('s5', dpid="0000000000000005")

        bottomLeftSwitch = self.addSwitch('s9', dpid="0000000000000009")
        bottomMiddleSwitch = self.addSwitch('s6', dpid="0000000000000006")
        bottomRightSwitch = self.addSwitch('s10', dpid="0000000000000010")

        self.addLink(h1, topMiddleSwitch)
        self.addLink(h2, bottomMiddleSwitch)

        self.addLink(topLeftSwitch, topMiddleSwitch)  # s7-s1
        self.addLink(topLeftSwitch, topMiddleLeftSwitch)  # s7-s2
        self.addLink(topMiddleSwitch, topMiddleLeftSwitch)  # s1-s2
        self.addLink(topMiddleSwitch, topRightSwitch)  # s1-s8
        self.addLink(topMiddleSwitch, topMiddleRightSwitch)  # s1-s3
        self.addLink(topMiddleSwitch, bottomMiddleSwitch)  # s1-s6
        self.addLink(topRightSwitch, topMiddleRightSwitch)  # s8-s3
        self.addLink(topMiddleLeftSwitch, bottomMiddleRightSwitch)  # s2-s5
        self.addLink(topMiddleLeftSwitch, bottomMiddleLeftSwitch)  # s2-s4
        self.addLink(topMiddleRightSwitch, bottomMiddleRightSwitch)  # s3-s5
        self.addLink(topMiddleRightSwitch, bottomMiddleLeftSwitch)  # s3-s4
        self.addLink(bottomMiddleLeftSwitch, bottomLeftSwitch)  # s4-s9
        self.addLink(bottomMiddleLeftSwitch, bottomMiddleSwitch)  # s4-s6
        self.addLink(bottomMiddleRightSwitch, bottomMiddleSwitch)  # s5-s6
        self.addLink(bottomMiddleRightSwitch, bottomRightSwitch)  # s5-s10
        self.addLink(bottomLeftSwitch, bottomMiddleSwitch)  # s9-s6
        self.addLink(bottomRightSwitch, bottomMiddleSwitch)  # s10-s6

        self.addLink(ap2, topMiddleLeftSwitch)
        self.addLink(ap3, topMiddleRightSwitch)
        self.addLink(ap4, bottomMiddleLeftSwitch)
        self.addLink(ap5, bottomMiddleRightSwitch)
        self.addLink(ap7, topLeftSwitch)
        self.addLink(ap8, topRightSwitch)
        self.addLink(ap9, bottomLeftSwitch)
        self.addLink(ap10, bottomRightSwitch)


topos = {'finaltopo': (lambda: FinalTopo())}
