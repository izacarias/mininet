#!/usr/bin/python

"""
Handover example.

"""

from mininet.net import Mininet
from mininet.node import RemoteController, Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.term import makeTerm

OF_CONTROLLER_IP = '143.54.12.179'
OF_CONTROLLER_PORT = 6633

FFSERVER_BIN = '/home/mininet/bin/ffserver'
FFPLAY_BIN = '/home/mininet/bin/ffplay'

# Experiments params
EXP_START_FROM = 0
EXP_TIMES_TO_RUN = 30
# EXP_STREAMS_LIST = ['h264400', 'h2641000', 'h2642250']
EXP_STREAMS_LIST = ['h2641000']


class OVSKernelSwitch13(OVSKernelSwitch):
    """
    Class for use of OpenFlow 1.3 (Inheritance)
    """
    def __init__(self, *args, **kwargs):
        OVSKernelSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)


def runFFServer(server_host):
    termTitle = 'FFServer on {0:s}'.format(server_host.name)
    conf_path = '/home/mininet/ffserver/'
    ffserver_cmd = '{0:s} -f {1:s}ffserver-{2:s}.conf'.format(
        FFSERVER_BIN, conf_path, server_host.name)
    # print '*** Starting server: ' + ffserver_cmd
    po_tunnel, po_terminal = makeTerm(
        server_host, title=termTitle, cmd=ffserver_cmd)
    return po_tunnel, po_terminal


def runFFPlay(player_host, server_host, stream_name, rep, exp_name):
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
    stream_url = 'http://{0:s}:{1:s}/{2:s}'.format(
        servers[server_host.name]['ip'], servers[server_host.name]['port'],
        stream_name)
    logfile_name = 'log_{0:s}_{1:s}_rep{2:02d}_{3:s}.log'.format(
        server_host.name, stream_name, rep, exp_name)
    ffplayer_cmd = '{0:s} -autoexit {1:s} 2>&1 | tee {2:s}'.format(
        FFPLAY_BIN, stream_url, logfile_name)
    termTitle = 'FFPlayer from {0:s}'.format(server_host.name)
    # print '*** Starting client: ' + ffplayer_cmd
    po_tunnel, po_terminal = makeTerm(
        player_host, title=termTitle, cmd=ffplayer_cmd)
    return po_tunnel, po_terminal


def topology():
    "Create a network."
    c1 = RemoteController('c1', ip=OF_CONTROLLER_IP, port=OF_CONTROLLER_PORT)
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch13)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    ap1 = net.addBaseStation('ap1', ssid='new-ssid1',
                             mode='g', channel='1', position='15,30,0')
    ap2 = net.addBaseStation('ap2', ssid='new-ssid2',
                             mode='g', channel='6', position='55,30,0')
    h1 = net.addHost('h1', mac='00:00:00:00:01:91', ip='10.0.1.91/8')

    print "*** Creating links"
    net.addLink(ap1, ap2)
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    """uncomment to plot graph"""
    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(startTime=0)
    net.mobility('sta1', 'start', time=1, position='10,30,0')
    net.mobility('sta2', 'start', time=2, position='10,40,0')
    net.mobility('sta1', 'stop', time=40, position='60,30,0')
    net.mobility('sta2', 'stop', time=40, position='25,40,0')
    net.stopMobility(stopTime=40)

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
