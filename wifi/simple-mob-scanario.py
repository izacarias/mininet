#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.term import makeTerm
from mininet.log import setLogLevel


"""
Handorver example (based on proposed scenario)
"""

# Configurations
OF_CONTROLLER_IP = '192.168.56.1'
OF_CONTROLLER_PORT = 6633

# Nodes placement
POS_SCALE = 20
POS_CENTER = 50

# Number of UAVs
CONF_UAV_NUMBER = 9


class OVSKernelSwitch13(OVSKernelSwitch):
    """
    Class for use of OpenFlow 1.3 (Inheritance)
    """
    def __init__(self, *args, **kwargs):
        OVSKernelSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)


def topology():
    """
      Creates the network elements in Mininet
    """

    # List o UAVs (stations)
    uav_list = []
    # List of Switches and APs (Guaranis)
    sw_list = []
    ap_list = []
    print "*** Creates a remote controller"
    c1 = RemoteController('c1', ip=OF_CONTROLLER_IP, port=OF_CONTROLLER_PORT)

    print "*** Creating a network."
    net = Mininet(controller=c1,
                  link=TCLink,
                  switch=OVSKernelSwitch13)

    # Creating N UAV (configured by CONF_UAV_NUMBER)
    print '*** Creating UAVs (Stations)'
    for i in range(CONF_UAV_NUMBER):
        print '*** Creating UAV {0:2d} of {1:2d}...'.format(i, CONF_UAV_NUMBER)
        sta_mac = '00:00:00:00:00:{0:02d}'.format(i)
        sta_name = 'sta{0:d}'.format(i)
        sta_ip = '10.0.0.{0:d}'.format(i)
        uav_list.append(net.addStation(sta_name, mac=sta_mac, ip=sta_ip))

    print "*** Creating static Guaranis (Switch + AP)"
    for i in xrange(1, 10):
        print '*** Creating Guarani (Switch + AP) {0:d} of {1:d}'.format(i, 9)
        sw_name = 's{0:d}'.format(i)
        ap_name = 'ap{0:d}'.format(i)
        sw_dpid = '000000000000000{0:d}'.format(i)
        ap_dpid = '000000000000100{0:d}'.format(i)
        sw_list.append(net.addSwitch(sw_name, dpid=sw_dpid))
        ap_list.append(net.addBaseStation(ap_name, dpid=ap_dpid, ssid='ssid_ex', ))

    print "*** Linking static switches"
    net.addLink(topLeftSwitch, topMiddleSwitch)                 # s7-s1
    net.addLink(topLeftSwitch, topMiddleLeftSwitch)             # s7-s2
    net.addLink(topMiddleSwitch, topMiddleLeftSwitch)           # s1-s2
    net.addLink(topMiddleSwitch, topRightSwitch)                # s1-s8
    net.addLink(topMiddleSwitch, topMiddleRightSwitch)          # s1-s3
    net.addLink(topMiddleSwitch, bottomMiddleSwitch)            # s1-s6
    net.addLink(topRightSwitch, topMiddleRightSwitch)           # s8-s3
    net.addLink(topMiddleLeftSwitch, bottomMiddleRightSwitch)   # s2-s5
    net.addLink(topMiddleLeftSwitch, bottomMiddleLeftSwitch)    # s2-s4
    net.addLink(topMiddleRightSwitch, bottomMiddleRightSwitch)  # s3-s5
    net.addLink(topMiddleRightSwitch, bottomMiddleLeftSwitch)   # s3-s4
    net.addLink(bottomMiddleLeftSwitch, bottomLeftSwitch)       # s4-s9
    net.addLink(bottomMiddleLeftSwitch, bottomMiddleSwitch)     # s4-s6
    net.addLink(bottomMiddleRightSwitch, bottomMiddleSwitch)    # s5-s6
    net.addLink(bottomMiddleRightSwitch, bottomRightSwitch)     # s5-s10
    net.addLink(bottomLeftSwitch, bottomMiddleSwitch)           # s9-s6
    net.addLink(bottomRightSwitch, bottomMiddleSwitch)          # s10-s6

    print "*** Creating access points"
    # Creating Access Points
    ap2 = net.addBaseStation('ap2', dpid='0000000000001002', ssid='ssid_ap',
                             mode='g', channel='1', position='37,10,0')
    ap3 = net.addBaseStation('ap3', dpid='0000000000001003', ssid='ssid_ap',
                             mode='g', channel='6', position='37,90,0')
    ap4 = net.addBaseStation('ap4', dpid='0000000000001004', ssid='ssid_ap',
                             mode='g', channel='11', position='62,10,0')
    ap5 = net.addBaseStation('ap5', dpid='0000000000001005', ssid='ssid_ap',
                             mode='g', channel='1', position='62,90,0')
    ap7 = net.addBaseStation('ap7', dpid='0000000000001007', ssid='ssid_ap',
                             mode='g', channel='1', position='0,0,0')
    ap8 = net.addBaseStation('ap8', dpid='0000000000001008', ssid='ssid_ap',
                             mode='g', channel='11', position='12,90,0')
    ap9 = net.addBaseStation('ap9', dpid='0000000000001009', ssid='ssid_ap',
                             mode='g', channel='6', position='87,10,0')
    ap10 = net.addBaseStation('ap10', dpid='0000000000001010',
                              ssid='ssid_ap', mode='g', channel='11',
                              position='87,90,0')

    print "*** Linking access points to switches"
    net.addLink(ap2, topMiddleLeftSwitch)
    net.addLink(ap3, topMiddleRightSwitch)
    net.addLink(ap4, bottomMiddleLeftSwitch)
    net.addLink(ap5, bottomMiddleRightSwitch)
    net.addLink(ap7, topLeftSwitch)
    net.addLink(ap8, topRightSwitch)
    net.addLink(ap9, bottomLeftSwitch)
    net.addLink(ap10, bottomRightSwitch)

    print "*** Creating links"
    net.addLink(ap7, sta1)
    net.addLink(ap8, sta2)

    print "*** Starting network"
    net.build()
    c1.start()
    # Starting Switches
    topMiddleSwitch.start([c1])
    topLeftSwitch.start([c1])
    topRightSwitch.start([c1])
    topMiddleLeftSwitch.start([c1])
    topMiddleRightSwitch.start([c1])
    bottomMiddleLeftSwitch.start([c1])
    bottomMiddleRightSwitch.start([c1])
    bottomLeftSwitch.start([c1])
    bottomMiddleSwitch.start([c1])
    bottomRightSwitch.start([c1])
    # Starting APs
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])
    ap7.start([c1])
    ap8.start([c1])
    ap9.start([c1])
    ap10.start([c1])

    # Running IPERF in stations
    makeTerm(sta1, title='Server', cmd='iperf -s')
    makeTerm(sta2, title='Client', cmd='iperf -c 10.0.0.2 -t 45')

    """uncomment to plot graph"""
    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(startTime=0)
    # Sta1 mobility
    net.mobility('sta1', 'start', time=1, position='10,22,0')
    net.mobility('sta1', 'stop', time=40, position='90,22,0')
    # sta2 mobility
    net.mobility('sta2', 'start', time=2, position='10,82,0')
    net.mobility('sta2', 'stop', time=40, position='90,82,0')
    # Stop all mobility
    net.stopMobility(stopTime=40)

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
