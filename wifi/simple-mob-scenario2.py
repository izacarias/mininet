#!/usr/bin/python
import os
import sys
import time
import datetime
import random

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
OF_CONTROLLER_IP = '127.0.0.1'
OF_CONTROLLER_PORT = 6633

# FFMpeg Binaries
FFSERVER_BIN = '/home/iulisloi/bin/ffserver'
FFPLAY_BIN = '/home/iulisloi/bin/ffplay'

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
    conf_path = '/home/iulisloi/ffserver'
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
    ffplayer_cmd = '{0:s} -autoexit -an -x 160 -y 90 {1:s} 2>&1 | tee {2:s}' \
        .format(FFPLAY_BIN, stream_url, logfile_name)
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
    uav_list.append(net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/24', min_x=40, max_x=66, min_y=20, max_y=66, wlans=1))
    uav_list.append(net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/24', min_x=67, max_x=133, min_y=20, max_y=66, wlans=1))
    uav_list.append(net.addStation('sta3', mac='00:00:00:00:00:03', ip='10.0.0.3/24', min_x=134, max_x=180, min_y=20, max_y=66, wlans=1))
    uav_list.append(net.addStation('sta4', mac='00:00:00:00:00:04', ip='10.0.0.4/24', min_x=40, max_x=66, min_y=67, max_y=133, wlans=1))
    uav_list.append(net.addStation('sta5', mac='00:00:00:00:00:05', ip='10.0.0.5/24', min_x=67, max_x=133, min_y=67, max_y=133, wlans=1))
    uav_list.append(net.addStation('sta6', mac='00:00:00:00:00:06', ip='10.0.0.6/24', min_x=134, max_x=180, min_y=67, max_y=133, wlans=1))
    uav_list.append(net.addStation('sta7', mac='00:00:00:00:00:07', ip='10.0.0.7/24', min_x=40, max_x=66, min_y=134, max_y=160, wlans=1))
    uav_list.append(net.addStation('sta8', mac='00:00:00:00:00:08', ip='10.0.0.8/24', min_x=67, max_x=133, min_y=134, max_y=160, wlans=1))
    uav_list.append(net.addStation('sta9', mac='00:00:00:00:00:09', ip='10.0.0.9/24', min_x=134, max_x=180, min_y=134, max_y=160, wlans=1))

    print "*** Creating static Guaranis (Switch + AP)"
    ap_ssid = 'ssid_dtn'
    ap_list.append(net.addBaseStation('ap1', dpid='0000000000001001', ssid=ap_ssid, mode='g', channel=1, position='50,50,0'))
    ap_list.append(net.addBaseStation('ap2', dpid='0000000000001002', ssid=ap_ssid, mode='g', channel=6, position='100,50,0'))
    ap_list.append(net.addBaseStation('ap3', dpid='0000000000001003', ssid=ap_ssid, mode='g', channel=11, position='145,45,0'))
    ap_list.append(net.addBaseStation('ap4', dpid='0000000000001004', ssid=ap_ssid, mode='g', channel=6, position='45,100,0'))
    ap_list.append(net.addBaseStation('ap5', dpid='0000000000001005', ssid=ap_ssid, mode='g', channel=11, position='110,112,0'))
    ap_list.append(net.addBaseStation('ap6', dpid='0000000000001006', ssid=ap_ssid, mode='g', channel=1, position='150,95,0'))
    ap_list.append(net.addBaseStation('ap7', dpid='0000000000001007', ssid=ap_ssid, mode='g', channel=11, position='50,150,0'))
    ap_list.append(net.addBaseStation('ap8', dpid='0000000000001008', ssid=ap_ssid, mode='g', channel=1, position='110,165,0'))
    ap_list.append(net.addBaseStation('ap9', dpid='0000000000001009', ssid=ap_ssid, mode='g', channel=6, position='156,157,0'))

    print "*** Creating links between Guaranis"
    net.addLink(ap_list[0], ap_list[3])
    net.addLink(ap_list[0], ap_list[1])
    net.addLink(ap_list[1], ap_list[4])
    net.addLink(ap_list[1], ap_list[2])
    net.addLink(ap_list[2], ap_list[5])
    net.addLink(ap_list[3], ap_list[6])
    net.addLink(ap_list[3], ap_list[4])
    net.addLink(ap_list[4], ap_list[7])
    net.addLink(ap_list[4], ap_list[5])
    net.addLink(ap_list[5], ap_list[8])
    net.addLink(ap_list[6], ap_list[7])
    net.addLink(ap_list[7], ap_list[8])


    h2_apid = random.randint(0, 8)
    print "*** Creating Hosts and adding links..."
    h1 = net.addHost('h1', mac='00:00:00:00:01:91', ip='10.0.0.91/24')
    net.addLink(h1, ap_list[1])
    h2 = net.addHost('h2', mac='00:00:00:00:01:92', ip='10.0.0.92/24')
    net.addLink(h2, ap_list[h2_apid])

    # print '*** Adding Mesh network among Stations'
    # for uav in uav_list:
    #     print '    - Adding UAV {0:s} to mesh network'.format(uav.name)
    #     net.addMesh(uav, ssid='meshNet')

    # print '*** Adding custom routing model to mesh...'
    # net.meshRouting('custom')

    # """uncomment to plot graph"""
    # net.plotGraph(max_x=200, max_y=200)

    print '*** Starting network'
    net.build()
    c1.start()
    # Starting APs
    for ap in ap_list:
        print '    - Starting {0:s}'.format(ap.name)
        ap.start([c1])

    for uav in uav_list:
        print '**** Associating {0:s} to Access Point'.format(uav.name)
        uav.cmd('iwconfig {0:s}-wlan0 essid {1:s}'.format(uav.name, ap_ssid))

    net.seed(20)
    # Starting Mobility
    net.startMobility(startTime=0, model='RandomWayPoint',
                      min_x=40, max_x=160, min_y=40, max_y=200, min_v=1, max_v=2)

    # Run FFServer on Stations
    # Running all servers to select a random source
    for n in range(CONF_UAV_NUMBER):
        p_tun, p_srv = runFFServer(uav_list[n])     # p_tun not used
        p_servers.append(n)
        p_servers[n] = p_srv

    # Wait for ffservers to initialize
    # and stations to go to initial position
    time.sleep(5)

    print '**** Running Exp {0:d} of stream {1:s} scenario {2:s}'. \
        format(run_number, stream_name, EXP_LOG_NAME[nr_of_clients])

    # print '**** Running {0:d} clients...'.format(nr_of_clients)

    # get updated timestamp to name all logs
    exp_timestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # create a random list of UAVs
    selected_uavs_list = random.sample(xrange(CONF_UAV_NUMBER), nr_of_clients)

    for n in range(nr_of_clients):
        selected_uav = selected_uavs_list[n]
        p1, p2 = runFFPlay(h1, uav_list[selected_uav], stream_name,
                           EXP_LOG_NAME[nr_of_clients], exp_timestr)
        p_players.append(n)
        p_players[n] = p2

    # additional host
    p1, p2 = runFFPlay(h1, uav_list[selected_uav], stream_name,
                       EXP_LOG_NAME[nr_of_clients], exp_timestr + '_h2_')
    p_players.append(9)
    p_players[9] = p2

    print '**** Waiting for FFPlay...'
    # print p2.wait()
    for p2 in p_players:
        p2.wait()

    # # Wait for clients to exit
    time.sleep(3)

    # # Stop all servers
    # # p_srv.terminate()
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
