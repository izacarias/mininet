#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.term import makeTerm

import time


"""
Handorver example (based on proposed scenario)
    Used addresses:
    UAVs Mesh:  10.0.0.XXX/24
    Hosts: 10.0.1.XXX/24
        - 10.0.1.[1-9] - UAVs
        - 10.0.1.[91-99] - Hosts

FFServer conf files:

FFServer conf file name: ffserver-<host>.conf
                         ffserver-sta1.conf -- HttpPort: 8001
                         ffserver-sta2.conf -- HttpPort: 8002
                         ...
                         ...
                         ffserver-sta9.conf -- HttpPort: 8009

"""

# Configurations
OF_CONTROLLER_IP = '192.168.56.1'
OF_CONTROLLER_PORT = 6633

# Number of UAVs
CONF_UAV_NUMBER = 9
CONF_GUARANI_NUMBER = 4

# Nodes placement
POS_SCALE = 35

# Distance between elements (UAV, vehicles...)
POS_GUARANI_DISTANCE = POS_SCALE / 3
POS_GUARANI_X = 100
POS_GUARANI_Y_START = POS_SCALE / 2

POS_UAV_FROM_GUARANI = POS_SCALE / 2
POS_UAV_DISTANCE = int(4.0 / (CONF_UAV_NUMBER - 1) * POS_SCALE)
POS_UAV_MOTION = 5

# Experiments params
EXP_TIMES_TO_RUN = 10


class OVSKernelSwitch13(OVSKernelSwitch):
    """
    Class for use of OpenFlow 1.3 (Inheritance)
    """

    def __init__(self, *args, **kwargs):
        OVSKernelSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)


def uav_get_ybase():
    posy = POS_GUARANI_Y_START + \
        (CONF_GUARANI_NUMBER - 1) * POS_GUARANI_DISTANCE + \
        POS_UAV_FROM_GUARANI
    return int(round(posy))


def uav_get_xbase(uav_index):
    formula = (uav_index - (CONF_UAV_NUMBER + 1) / 2) * POS_UAV_DISTANCE
    posx = POS_GUARANI_X + formula
    return int(round(posx))


def runFFServer(net, host):
    termTitle = 'FFServer on {0:s}'.format(host.name())
    ffserverCmd = 'ffserver-{0:s}.conf'.format(host.name)
    makeTerm(host, title=termTitle, cmd=ffserverCmd)
    pass


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

    # # Creating N UAV (configured by CONF_UAV_NUMBER)
    print '*** Creating UAVs (Stations)'
    for i in range(CONF_UAV_NUMBER):
        print '    - Creating UAV {0:2d} of {1:2d}...'.format(i + 1,
                                                              CONF_UAV_NUMBER)
        sta_mac = '00:00:00:00:00:{0:02d}'.format(i + 1)
        sta_name = 'sta{0:d}'.format(i + 1)
        sta_ip = '10.0.0.{0:d}/24'.format(i + 1)
        # node position
        uav_position = '{0:d},{1:d},0'.format(
            uav_get_xbase(i + 1), uav_get_ybase() - 10)
        uav_min_x = uav_get_xbase(i + 1) - POS_UAV_MOTION
        uav_max_x = uav_get_xbase(i + 1) + POS_UAV_MOTION
        uav_min_y = uav_get_ybase() - POS_UAV_MOTION
        uav_max_y = uav_get_ybase() + POS_UAV_MOTION
        uav_list.append(net.addStation(sta_name, mac=sta_mac, ip=sta_ip,
                                       min_x=uav_min_x, max_x=uav_max_x,
                                       min_y=uav_min_y, max_y=uav_max_y,
                                       wlans=2, position=uav_position))

    # print '*** Creating UAVs (Stations)'
    # for uav in uav_list:
    #     print '    - Adding UAV {0:s} to WifiDirect'.format(uav.name)
    #     net.wifiDirect(uav)

    print "*** Creating static Guaranis (Switch + AP)"
    for i in xrange(1, CONF_GUARANI_NUMBER + 1):
        print '    - Creating Guarani (Switch + AP) {0:d} of {1:d}' \
            .format(i, CONF_GUARANI_NUMBER)
        sw_name = 's{0:d}'.format(i)
        sw_dpid = '000000000000000{0:d}'.format(i)
        sw_list.append(net.addSwitch(sw_name, dpid=sw_dpid))

        if i == CONF_GUARANI_NUMBER:
            ap_name = 'ap{0:d}'.format(i)
            ap_dpid = '000000000000100{0:d}'.format(i)
            ap_ssid = 'ssid_ap{0:d}'.format(i)
            print '      - {0:s} -> SSID: {1:s}'.format(ap_name, ap_ssid)
            ap_position = '{0:d},{1:d},0'.format(
                POS_GUARANI_X,
                POS_GUARANI_Y_START + ((i - 1) * POS_GUARANI_DISTANCE))
            ap_channel = [1, 6, 11][i % 3]

            ap_list.append(net.addBaseStation(ap_name, dpid=ap_dpid,
                                              ssid=ap_ssid, mode='g',
                                              channel=ap_channel,
                                              position=ap_position))
            # Link last created AP with last created Switch
            net.addLink(sw_list[-1], ap_list[-1])

    print "*** Creating links between Guaranis"
    for i in xrange(0, CONF_GUARANI_NUMBER - 1):
        print "    - sw{0:s} <=======> sw{1:s}".format(sw_list[i].name,
                                                       sw_list[i + 1].name)
        net.addLink(sw_list[i], sw_list[i + 1])

    h1 = net.addHost('h1', mac='00:00:00:00:01:91', ip='10.0.1.91/24')
    h2 = net.addHost('h2', mac='00:00:00:00:01:91', ip='10.0.1.92/24')
    """ Creating routes on hosts """
    net.addLink(h1, sw_list[0])
    net.addLink(h2, sw_list[-1])

    print '*** Adding Mesh network among Stations'
    for uav in uav_list:
        print '    - Adding UAV {0:s} to mesh network'.format(uav.name)
        net.addMesh(uav, ssid='meshNet')

    print '*** Starting network'
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

    print '**** Associating UAV5 to Access Point'
    uav_list[4].cmd('iwconfig sta5-wlan1 essid ssid_ap4')
    print '**** Configuring the IP address for UAV Wireless interface'
    uav_list[4].cmd('ifconfig sta5-wlan1 10.0.1.5/24')

    # Adding routes to hosts
    h1.cmd('route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.1.5')
    h2.cmd('route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.1.5')
    # Enabling the routing by node sta5
    uav_list[4].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 dev sta5-wlan1')
    uav_list[4].cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    # Configuring staX routes
    uav_list[0].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[1].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[2].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[3].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    # uav_list[4] is the GATEWAY!!!
    uav_list[5].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[6].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[7].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[8].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')

    # """uncomment to plot graph"""
    # net.plotGraph(max_x=200, max_y=200)

    # Starting Mobility
    # net.seed(20)
    # net.startMobility(startTime=0, model='GaussMarkov', min_v=0.5, max_v=0.8)

    # Run FFServer on Stations
    runFFServer(net, uav_list[0])   # sta1
    runFFServer(net, uav_list[4])   # sta5
    runFFServer(net, uav_list[8])   # sta9

    makeTerm(uav_list[7], title='FFServer', cmd='ffserver -d')
    # Wait for ffserver to initialize
    time.sleep(1)

    # Running ffplay clients with loglevel trace (REPEAT)
    for i in range(EXP_TIMES_TO_RUN):
        h1.cmd

    # makeTerm(h1, title='FFPlay running the video', 
    #    cmd='ffplay -loglevel trace http://10.0.0.8:8090/movie480.ogg > log_h1.log 2>&1')
    # makeTerm(h2, title='Iperf client', cmd='')

    print '*** Running CLI'
    CLI(net)

    print '*** Stopping network'
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
