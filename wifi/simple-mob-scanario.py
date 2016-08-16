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

# Number of UAVs
CONF_UAV_NUMBER = 9
CONF_GUARANI_NUMBER = 9

# Nodes placement
POS_SCALE = 35
# Distance between elements (UAV, vehicles...)
POS_GUARANI_DISTANCE = POS_SCALE / 3
POS_GUARANI_X = 100
POS_GUARANI_Y_START = POS_SCALE / 2

POS_UAV_FROM_GUARANI = POS_SCALE
POS_UAV_DISTANCE = 4.0 / (CONF_UAV_NUMBER - 1) * POS_SCALE
POS_


class OVSKernelSwitch13(OVSKernelSwitch):
    """
    Class for use of OpenFlow 1.3 (Inheritance)
    """

    def __init__(self, *args, **kwargs):
        OVSKernelSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)


def uav_get_ybase():
    y_position = POS_GUARANI_Y_START + \
        (CONF_GUARANI_NUMBER - 1) * POS_GUARANI_DISTANCE + \
        POS_UAV_FROM_GUARANI
    return y_position


def uav_get_xbase(uav_index):
    formula = (uav_index - (CONF_UAV_NUMBER + 1) / 2) * POS_UAV_DISTANCE
    posx = POS_GUARANI_X + formula
    return posx


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
        print '    - Creating UAV {0:2d} of {1:2d}...'.format(i + 1,
                                                              CONF_UAV_NUMBER)
        sta_mac = '00:00:00:00:00:{0:02d}'.format(i + 1)
        sta_name = 'sta{0:d}'.format(i + 1)
        sta_ip = '10.0.0.{0:d}/8'.format(i + 1)
        uav_list.append(net.addStation(sta_name, mac=sta_mac, ip=sta_ip))

    print "*** Creating static Guaranis (Switch + AP)"
    for i in xrange(1, CONF_GUARANI_NUMBER + 1):
        print '    - Creating Guarani (Switch + AP) {0:d} of {1:d}' \
            .format(i, 9)
        sw_name = 's{0:d}'.format(i)
        ap_name = 'ap{0:d}'.format(i)
        sw_dpid = '000000000000000{0:d}'.format(i)
        ap_dpid = '000000000000100{0:d}'.format(i)
        ap_channel = i % 3
        ap_position = '{0:d},{1:d},0'.format(
            POS_GUARANI_X,
            POS_GUARANI_Y_START + ((i - 1) * POS_GUARANI_DISTANCE))
        sw_list.append(net.addSwitch(sw_name, dpid=sw_dpid))
        ap_list.append(net.addBaseStation(ap_name, dpid=ap_dpid,
                                          ssid='ssid_ex', mode='g',
                                          channel=ap_channel,
                                          position=ap_position))
        # Link last created AP with last created Switch
        net.addLink(sw_list[-1], ap_list[-1])

    print "*** Creating links between Guaranis"
    for i in xrange(1, CONF_GUARANI_NUMBER - 1):
        print "    - sw{0:d} <=======> sw{1:d}".format(i, i + 1)
        net.addLink(sw_list[i], sw_list[i + 1])

    print "*** Starting network"
    net.build()
    c1.start()
    # Starting Switches
    for sw in sw_list:
        print '    - Starting {0:s}'.format(sw.name)
        sw.start([c1])
    # Starting APs
    for ap in ap_list:
        print '    - Starting {0:s}'.format(ap.name)
        ap.start([c1])

    # Running IPERF in stations
    # makeTerm(sta1, title='Server', cmd='iperf -s')
    # makeTerm(sta2, title='Client', cmd='iperf -c 10.0.0.2 -t 45')

    """uncomment to plot graph"""
    net.plotGraph(max_x=200, max_y=200)

    # net.startMobility(startTime=0)
    # # Sta1 mobility
    # net.mobility('sta1', 'start', time=1, position='10,22,0')
    # net.mobility('sta1', 'stop', time=40, position='90,22,0')
    # # sta2 mobility
    # net.mobility('sta2', 'start', time=2, position='10,82,0')
    # net.mobility('sta2', 'stop', time=40, position='90,82,0')
    # # Stop all mobility
    # net.stopMobility(stopTime=40)

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
