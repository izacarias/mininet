#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel


"""
Handorver example (based on proposed scenario)
"""

# Configurations
OF_CONTROLLER_IP = '192.168.56.1'
OF_CONTROLLER_PORT = 6633


"""
  The topology class
"""


class FinalTopo(Topo):
    """
    Topology class for used scenario
    """

    def build(self):

        # Creating switches
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
        # Linking Switches
        self.addLink(topLeftSwitch, topMiddleSwitch)                 # s7-s1
        self.addLink(topLeftSwitch, topMiddleLeftSwitch)             # s7-s2
        self.addLink(topMiddleSwitch, topMiddleLeftSwitch)           # s1-s2
        self.addLink(topMiddleSwitch, topRightSwitch)                # s1-s8
        self.addLink(topMiddleSwitch, topMiddleRightSwitch)          # s1-s3
        self.addLink(topMiddleSwitch, bottomMiddleSwitch)            # s1-s6
        self.addLink(topRightSwitch, topMiddleRightSwitch)           # s8-s3
        self.addLink(topMiddleLeftSwitch, bottomMiddleRightSwitch)   # s2-s5
        self.addLink(topMiddleLeftSwitch, bottomMiddleLeftSwitch)    # s2-s4
        self.addLink(topMiddleRightSwitch, bottomMiddleRightSwitch)  # s3-s5
        self.addLink(topMiddleRightSwitch, bottomMiddleLeftSwitch)   # s3-s4
        self.addLink(bottomMiddleLeftSwitch, bottomLeftSwitch)       # s4-s9
        self.addLink(bottomMiddleLeftSwitch, bottomMiddleSwitch)     # s4-s6
        self.addLink(bottomMiddleRightSwitch, bottomMiddleSwitch)    # s5-s6
        self.addLink(bottomMiddleRightSwitch, bottomRightSwitch)     # s5-s10
        self.addLink(bottomLeftSwitch, bottomMiddleSwitch)           # s9-s6
        self.addLink(bottomRightSwitch, bottomMiddleSwitch)          # s10-s6

        # Creating Access Points
        ap2 = self.addSwitch('ap2', dpid='0000000000001002', ssid='ssid_ap2',
                             mode='g', channel='1', position='37,10,0')
        ap3 = self.addSwitch('ap3', dpid='0000000000001003', ssid='ssid_ap3',
                             mode='g', channel='6', position='37,90,0')
        ap4 = self.addSwitch('ap4', dpid='0000000000001004', ssid='ssid_ap4',
                             mode='g', channel='11', position='62,10,0')
        ap5 = self.addSwitch('ap5', dpid='0000000000001005', ssid='ssid_ap5',
                             mode='g', channel='1', position='62,90,0')
        ap7 = self.addSwitch('ap7', dpid='0000000000001007', ssid='ssid_ap7',
                             mode='g', channel='1', position='12,10,0')
        ap8 = self.addSwitch('ap8', dpid='0000000000001008', ssid='ssid_ap8',
                             mode='g', channel='11', position='12,90,0')
        ap9 = self.addSwitch('ap9', dpid='0000000000001009', ssid='ssid_ap9',
                             mode='g', channel='6', position='87,10,0')
        ap10 = self.addSwitch('ap10', dpid='0000000000001010',
                              ssid='ssid_ap10', mode='g', channel='11',
                              position='87,90,0')
        # Linking Aps
        self.addLink(ap2, topMiddleLeftSwitch)                       # ap2-s2
        self.addLink(ap3, topMiddleRightSwitch)
        self.addLink(ap4, bottomMiddleLeftSwitch)
        self.addLink(ap5, bottomMiddleRightSwitch)
        self.addLink(ap7, topLeftSwitch)
        self.addLink(ap8, topRightSwitch)
        self.addLink(ap9, bottomLeftSwitch)
        self.addLink(ap10, bottomRightSwitch)

        # Creating Stations
        print "*** Creating station nodes"
        sta1 = self.addStation('sta1', mac='00:00:00:00:00:02')
        sta2 = self.addStation('sta2', mac='00:00:00:00:00:03')
        print "*** Creating links for nodes (Satations)"
        self.addLink(ap7, sta1, cls=TCLink)
        self.addLink(ap8, sta2, cls=TCLink)


def mobilityTest():
    """
    Main test function
    """

    # Adding access points (APs - Static nodes?)

    # Adding Stations (Mobile nodes)

    c1 = RemoteController('c1', ip=OF_CONTROLLER_IP, port=OF_CONTROLLER_PORT)
    # Instanciating the topology class
    print "* Instanciating the topology"
    topo = FinalTopo()
    # Creating the mininet object
    print '* Creating Mininet network'
    net = Mininet(controller=c1, switch=OVSKernelSwitch,
                  topo=topo, autoSetMacs=True)
    # Starting the Mininet Network
    print '* Starting network:'
    net.build()
    net.start()
    # # Waiting for OpenFlow Controller
    # print '* Waiting for the controller...'
    # net.waitConnected(delay=1)
    # # Testing the network

    # """uncomment to plot graph"""
    # net.plotGraph(max_x=120, max_y=100)

    # net.startMobility(startTime=0)
    # net.mobility('sta1', 'start', time=1, position='10,30,0')
    # net.mobility('sta2', 'start', time=2, position='10,70,0')
    # net.mobility('sta1', 'stop', time=40, position='90,30,0')
    # net.mobility('sta2', 'stop', time=40, position='90,70,0')
    # net.stopMobility(stopTime=40)

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    """
    Bootstrap function
    """
    setLogLevel('info')
    mobilityTest()
