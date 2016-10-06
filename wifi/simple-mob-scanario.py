#!/usr/bin/python
import os
import sys
import time
import datetime

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, UserSwitch

from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.term import makeTerm


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
OF_CONTROLLER_IP = '143.54.12.179'
OF_CONTROLLER_PORT = 6633

# FFMpeg Binaries
FFSERVER_BIN = '/home/mininet/bin/ffserver'
FFPLAY_BIN = '/home/mininet/bin/ffplay'

# Number of UAVs
CONF_UAV_NUMBER = 9
CONF_GUARANI_NUMBER = 9

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
EXP_START_FROM = 0
EXP_TIMES_TO_RUN = 30
# EXP_STREAMS_LIST = ['h264400', 'h2641000', 'h2642250']
EXP_STREAMS_LIST = ['h2641000']

EXP_LOG_NAME = {1: 'ONE', 2: 'TWO', 3: 'THREE',
                4: 'FOUR', 5: 'FIVE', 6: 'SIX',
                7: 'SEVEN', 8: 'EIGHT', 9: 'NINE'}


class OVSKernelSwitch13(OVSKernelSwitch):
    """
    Class for use of OpenFlow 1.3 (Inheritance)
    """
    def __init__(self, *args, **kwargs):
        OVSKernelSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)


class UserSwitch13(UserSwitch):
    """
    Class using OpenFlow 1.3 (Inheritance)
    """
    def __init__(self, *args, **kwargs):
        UserSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)


def uav_get_ybase():
    posy = POS_GUARANI_Y_START + \
        (CONF_GUARANI_NUMBER - 1) * POS_GUARANI_DISTANCE + \
        POS_UAV_FROM_GUARANI
    return int(round(posy))


def uav_get_xbase(uav_index):
    formula = (uav_index - (CONF_UAV_NUMBER + 1) / 2) * POS_UAV_DISTANCE
    posx = POS_GUARANI_X + formula
    return int(round(posx))


def runFFServer(server_host):
    termTitle = 'FFServer on {0:s}'.format(server_host.name)
    conf_path = '/home/mininet/ffserver/'
    ffserver_cmd = '{0:s} -f {1:s}ffserver-{2:s}.conf'.format(
        FFSERVER_BIN, conf_path, server_host.name)
    # print '*** Starting server: ' + ffserver_cmd
    po_tunnel, po_terminal = makeTerm(
        server_host, title=termTitle, cmd=ffserver_cmd)
    return po_tunnel, po_terminal


def runFFPlay(player_host, server_host, stream_name, exp_name, exp_timestr=''):
    """ List of ffservers """
    servers = {'sta1': {'ip': '10.0.0.1', 'port': '8001'},
               'sta2': {'ip': '10.0.0.2', 'port': '8002'},
               'sta3': {'ip': '10.0.0.3', 'port': '8003'},
               'sta4': {'ip': '10.0.0.4', 'port': '8004'},
               'sta5': {'ip': '10.0.0.5', 'port': '8005'},
               'sta6': {'ip': '10.0.0.6', 'port': '8006'},
               'sta7': {'ip': '10.0.0.7', 'port': '8007'},
               'sta8': {'ip': '10.0.0.8', 'port': '8008'},
               'sta9': {'ip': '10.0.0.9', 'port': '8009'}}
    if exp_timestr == '':
        exp_timestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    stream_url = 'http://{0:s}:{1:s}/{2:s}'.format(
        servers[server_host.name]['ip'], servers[server_host.name]['port'],
        stream_name)
    logfile_name = 'log_{0:s}_{1:s}_rep{2:s}_{3:s}.log'.format(
        server_host.name, stream_name, exp_timestr, exp_name)
    ffplayer_cmd = '{0:s} -autoexit -an -x 160 -y 90 {1:s} 2>&1 | tee {2:s}'.format(
        FFPLAY_BIN, stream_url, logfile_name)
    termTitle = 'FFPlayer from {0:s}'.format(server_host.name)
    # print '*** Starting client: ' + ffplayer_cmd
    po_tunnel, po_terminal = makeTerm(
        player_host, title=termTitle, cmd=ffplayer_cmd)
    return po_tunnel, po_terminal


def topology(run_number, stream_name, nr_of_clients):
    """
      Creates the network elements in Mininet
    """

    # List o UAVs (stations)
    uav_list = []
    # List of Switches and APs (Guaranis)
    sw_list = []
    ap_list = []

    # list of running servers (Process ID -- POpen)
    p_servers = []
    p_players = []

    print "*** Creating a remote controller"
    c1 = RemoteController('c1', ip=OF_CONTROLLER_IP, port=OF_CONTROLLER_PORT)

    print "*** Creating a network."
    net = Mininet(controller=c1,
                  link=TCLink,
                  switch=OVSKernelSwitch13)

    """ Creating N UAV (configured by CONF_UAV_NUMBER)"""
    print '*** Creating UAVs (Stations)'
    for i in range(CONF_UAV_NUMBER):
        print '    - Creating UAV {0:2d} of {1:2d}...'.format(i + 1,
                                                              CONF_UAV_NUMBER)
        sta_mac = '00:00:00:00:00:{0:02d}'.format(i + 1)
        sta_name = 'sta{0:d}'.format(i + 1)
        sta_ip = '10.0.0.{0:d}/24'.format(i + 1)
        # node position
        # uav_position = '{0:d},{1:d},0'.format(
        #     uav_get_xbase(i + 1), uav_get_ybase() - 10)
        uav_min_x = uav_get_xbase(i + 1) - POS_UAV_MOTION
        uav_max_x = uav_get_xbase(i + 1) + POS_UAV_MOTION
        uav_min_y = uav_get_ybase() - POS_UAV_MOTION
        uav_max_y = uav_get_ybase() + POS_UAV_MOTION
        uav_list.append(net.addStation(sta_name, mac=sta_mac, ip=sta_ip,
                                       min_x=uav_min_x, max_x=uav_max_x,
                                       min_y=uav_min_y, max_y=uav_max_y,
                                       wlans=2))

    print "*** Creating static Guaranis (Switch + AP)"
    for i in xrange(1, CONF_GUARANI_NUMBER + 1):
        print '    - Creating Guarani (Switch + AP) {0:d} of {1:d}' \
            .format(i, CONF_GUARANI_NUMBER)
        sw_name = 's{0:d}'.format(i)
        sw_dpid = '00000000000000{0:02d}'.format(i)
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

    print "*** Creating Hosts and adding links..."
    h1 = net.addHost('h1', mac='00:00:00:00:01:91', ip='10.0.1.91/24')
    net.addLink(h1, sw_list[0])
    # h2 = net.addHost('h2', mac='00:00:00:00:01:92', ip='10.0.1.92/24')
    # net.addLink(h2, sw_list[-1])

    print '*** Adding Mesh network among Stations'
    for uav in uav_list:
        print '    - Adding UAV {0:s} to mesh network'.format(uav.name)
        net.addMesh(uav, ssid='meshNet')

    print '*** Adding custom routing model to mesh...'
    net.meshRouting('custom')

    # """uncomment to plot graph"""
    # net.plotGraph(max_x=200, max_y=200)

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
    uav_list[4].cmd('iwconfig sta5-wlan1 essid ssid_ap9')
    print '**** Configuring the IP address for UAV Wireless interface'

    for uav in uav_list:
        print '**** Configuring {0:s}-wlan1: 10.0.1.{1:d}/24' \
            .format(uav.name, uav_list.index(uav) + 1)
        uav.cmd(
            'ifconfig {0:s}-wlan1 10.0.1.{1:d}/24'
            .format(uav.name, uav_list.index(uav) + 1))
        uav.cmd(
            'iptables -A FORWARD -i {0:s}-wlan1 -o {0:s}-mp0 -j ACCEPT'
            .format(uav.name))
        uav.cmd(
            'iptables -A FORWARD -i {0:s}-mp0 -o {0:s}-wlan1 -j ACCEPT'
            .format(uav.name))
        uav.cmd(
            'iptables -A FORWARD -i {0:s}-mp0 -o {0:s}-wlan1 -m state ' +
            '--state ESTABLISHED,RELATED -j ACCEPT'
            .format(uav.name))
        uav.cmd(
            'iptables -t nat -A POSTROUTING -o {0:s}-mp0 -j MASQUERADE'
            .format(uav.name))
        uav.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    # Adding routes to hosts
    h1.cmd('route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.1.5')

    # Enabling the routing by node sta5
    uav_list[4].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 dev sta5-wlan1')

    # Configuring staX routes
    uav_list[0].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[1].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[2].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[3].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    # --- uav_list[4] is the GATEWAY ---
    # uav_list[4].cmd(
    #     'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[5].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[6].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[7].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')
    uav_list[8].cmd(
        'route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.0.5')

    net.seed(20)
    # Starting Mobility
    net.startMobility(startTime=0, model='RandomWalk',
                      max_x=200, max_y=200, min_v=0.1, max_v=0.2)

    # Run FFServer on Stations
    # Running all servers to select a random source
    for n in range(CONF_UAV_NUMBER):
        p_tun, p_srv = runFFServer(uav_list[n])     # p_tun not used
        p_servers.append(n)
        p_servers[n] = p_srv

    # Wait for ffservers to initialize
    # and stations to go to initial position
    time.sleep(8)

    print '**** Running Exp {0:d} of stream {1:s} scenario {2:s}'. \
        format(run_number, stream_name, EXP_LOG_NAME[nr_of_clients])

    print '**** Running {0:d} clients...'.format(nr_of_clients)

    # p1, p2 = runFFPlay(h1, uav_list[0], stream_name,
    #                   EXP_LOG_NAME[nr_of_clients])
    # get updated timestamp to name all logs
    exp_timestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for n in range(nr_of_clients):
        p1, p2 = runFFPlay(h1, uav_list[n], stream_name,
                           EXP_LOG_NAME[nr_of_clients], exp_timestr)
        p_players.append(n)
        p_players[n] = p2

    print '**** Waiting for FFPlay...'
    # print p2.wait()
    for p2 in p_players:
        p2.wait()

    # Wait for clients to exit
    time.sleep(3)

    # Stop all servers
    # p_srv.terminate()
    for p_srv in p_servers:
        p_srv.terminate()

    print '*** Stopping network'
    net.stop()


def get_args(args, arg_key=''):
    return args[args.index(arg_key) + 1]


if __name__ == '__main__':
    setLogLevel('info')
    stream = get_args(sys.argv, '-m')
    run_number = int(get_args(sys.argv, '-n'))
    nr_of_clients = int(get_args(sys.argv, '-c'))
    topology(run_number, stream, nr_of_clients)
