#!/usr/bin/python

"""
Simple example of Mobility with Mininet
(aka enough rope to hang yourself.)

We move a host from s1 to s2, s2 to s3, and then back to s1.

Gotchas:

The reference controller doesn't support mobility, so we need to
manually flush the switch flow tables!

Good luck!

to-do:

- think about wifi/hub behavior
- think about clearing last hop - why doesn't that work?
"""

from mininet.log import output, warn
from mininet.net import Mininet, CLI
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.term import makeTerm
from random import randint
import time

HOST_NUMBER = 9
MOVE_SERVER = False
MOVIE_FILE_NAME = '720x480_5mb.mp4'
host_switch = {}


class MobilitySwitch(OVSSwitch):
    "Switch that can reattach and rename interfaces"

    def __init__(self, *args, **kwargs):
        OVSSwitch.__init__(self, protocols='OpenFlow13', *args, **kwargs)

    def delIntf(self, intf):
        "Remove (and detach) an interface"
        port = self.ports[intf]
        del self.ports[intf]
        del self.intfs[port]
        del self.nameToIntf[intf.name]

    def addIntf(self, intf, rename=False, **kwargs):
        "Add (and reparent) an interface"
        OVSSwitch.addIntf(self, intf, **kwargs)
        intf.node = self
        if rename:
            self.renameIntf(intf)

    def attach(self, intf):
        "Attach an interface and set its port"
        port = self.ports[intf]
        if port:
            if self.isOldOVS():
                self.cmd('ovs-vsctl add-port', self, intf)
            else:
                self.cmd('ovs-vsctl add-port', self, intf,
                         '-- set Interface', intf,
                         'ofport_request=%s' % port)
            self.validatePort(intf)

    def validatePort(self, intf):
        "Validate intf's OF port number"
        ofport = int(self.cmd('ovs-vsctl get Interface', intf,
                              'ofport'))
        if ofport != self.ports[intf]:
            warn('WARNING: ofport for', intf, 'is actually', ofport,
                 '\n')

    def renameIntf(self, intf, newname=''):
        "Rename an interface (to its canonical name)"
        intf.ifconfig('down')
        if not newname:
            newname = '%s-eth%d' % (self.name, self.ports[intf])
        intf.cmd('ip link set', intf, 'name', newname)
        del self.nameToIntf[intf.name]
        intf.name = newname
        self.nameToIntf[intf.name] = intf
        intf.ifconfig('up')

    def moveIntf(self, intf, switch, port=None, rename=True):
        "Move one of our interfaces to another switch"
        self.detach(intf)
        self.delIntf(intf)
        switch.addIntf(intf, port=port, rename=rename)
        switch.attach(intf)


class FinalTopo(Topo):
    """docstring for ClassName"""

    def build(self):
        global host_switch
        # Creating Hosts h0 to ...
        hs = [self.addHost('h%d' % i) for i in range(0, HOST_NUMBER)]
        # Creating APs (Switches)
        ap2 = self.addSwitch('ap2', dpid="0000000000001002")
        ap3 = self.addSwitch('ap3', dpid="0000000000001003")
        ap4 = self.addSwitch('ap4', dpid="0000000000001004")
        ap5 = self.addSwitch('ap5', dpid="0000000000001005")
        ap7 = self.addSwitch('ap7', dpid="0000000000001007")
        ap8 = self.addSwitch('ap8', dpid="0000000000001008")
        ap9 = self.addSwitch('ap9', dpid="0000000000001009")
        ap10 = self.addSwitch('ap10', dpid="0000000000001010")
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
        # Linking Aps
        self.addLink(ap2, topMiddleLeftSwitch)                       # ap2-s2
        self.addLink(ap3, topMiddleRightSwitch)
        self.addLink(ap4, bottomMiddleLeftSwitch)
        self.addLink(ap5, bottomMiddleRightSwitch)
        self.addLink(ap7, topLeftSwitch)
        self.addLink(ap8, topRightSwitch)
        self.addLink(ap9, bottomLeftSwitch)
        self.addLink(ap10, bottomRightSwitch)
        # Linking Hosts
        sws = [topMiddleSwitch,
               topLeftSwitch,
               topRightSwitch,
               topMiddleLeftSwitch,
               topMiddleRightSwitch,
               bottomMiddleLeftSwitch,
               bottomMiddleRightSwitch,
               bottomLeftSwitch,
               bottomMiddleSwitch,
               bottomRightSwitch]
        for h in hs:
            sw = sws[randint(0, len(sws) - 1)]
            self.addLink(h, sw)
            # Store initial ref host x switch
            host_switch[h] = sw


def printConnections(switches):
    "Compactly print connected nodes to each switch"
    for sw in switches:
        output('%s: ' % sw)
        for intf in sw.intfList():
            link = intf.link
            if link:
                intf1, intf2 = link.intf1, link.intf2
                remote = intf1 if intf1.node != sw else intf2
                output('%s(%s) ' % (remote.node, sw.ports[intf]))
        output('\n')


def moveHost(host, oldSwitch, newSwitch, newPort=None):
    "Move a host from old switch to new switch"
    hintf, sintf = host.connectionsTo(oldSwitch)[0]
    oldSwitch.moveIntf(sintf, newSwitch, port=newPort)
    return hintf, sintf


def vlcCommand(type='', host=None, curr_time_str=None):
    "Create VLC Player commands for server abnd clients"
    baseCommand = 'vlc-wrapper '
    if (type == 'server'):
        # media_file = '/home/mininet/720x480_5mb.mp4'
        media_file = '/home/mininet/' + MOVIE_FILE_NAME
        # baseCommand += '-vvv '
        baseCommand += media_file + ' '
        baseCommand += '-I dummy '
        baseCommand += '--sout '
        # baseCommand += "'#transcode{vcodec=mp4v,acodec=none,vb=800,ab=128}"
        baseCommand += '"#http{mux=ffmpeg{mux=flv},dst=:8080}" '
        # baseCommand += '--loop '
        baseCommand += '--sout-keep '
        return baseCommand

    if (type == 'client'):
        baseCommand += ' -vvv'
        baseCommand += ' http://10.0.0.1:8080'
        baseCommand += ' --novideo'
        baseCommand += ' --noaudio'
        baseCommand += ' --play-and-exit'
        if host:
            log_file_name = ""
            if curr_time_str:
                log_file_name = curr_time_str + "_" + host.name
            baseCommand += ' --extraintf=http:logger'
            baseCommand += ' --verbose=2'
            baseCommand += ' --file-logging'
            baseCommand += ' --logfile=' + log_file_name + '.log'
        return baseCommand

    if (type == 'ping'):
        baseCommand = 'ping 10.0.0.1'
        return baseCommand


def mobilityTest():
    "Simple Random Mobility"
    global host_switch
    # list of hosts
    h = []
    ap = []
    old = []
    ap_names = ['ap2', 'ap3', 'ap4', 'ap5',
                'ap7', 'ap8', 'ap9', 'ap10']
    used_ports = {}
    # Getting Current time to save logs
    curr_time_str = time.strftime("%H%M%S")
    # Creating remote controller (on Host OS)
    c1 = RemoteController('c1', ip='192.168.56.1', port=6633)
    print '* Simple mobility test'
    # Using Custom Topology (FinalTopo)
    print "* Instanciating FinalTopo"
    topo = FinalTopo()
    print '* Preparing network'
    # Creating the Mininet Object
    net = Mininet(topo=topo, autoSetMacs=True,
                  switch=MobilitySwitch, controller=c1)
    print '* Starting network:'
    net.start()
    printConnections(net.switches)
    print '* Waiting for the controller...'
    net.waitConnected(delay=1)
    print '... ok All switches connected.'
    print '* Testing network'
    net.pingAll()
    print '* Identifying switch interface for h1'
    # Add hosts and old (actual) switches to list
    for i in range(0, HOST_NUMBER):
        h_name = 'h%d' % i
        h.append(net.get(h_name))
        old.append(net.get(host_switch[h_name]))
    # create list of AP/Switches
    for i in range(len(ap_names) - 1):
        ap.append(net.get(ap_names[i]))
        used_ports[ap_names[i]] = []
    # Running VLC Player
    # print vlcCommand('server')

    makeTerm(h[0], title='Streamer', cmd=vlcCommand('server'))
    # Wait for server starts stream
    time.sleep(3)  # waiting for streaming server (1 sec)
    # Make clients for VLC
    for i in range(1, len(h)):
        print "** Starting Clients"
        vlc_command = vlcCommand('client', h[i], curr_time_str)
        print vlc_command
        makeTerm(h[i], title='Client', cmd=vlc_command)
    # makeTerm(h2, title='Client', cmd=vlcCommand('client', h2, curr_time_str))
    print '* Starting "handovers"'
    # Should move the server (starts in h0)
    if MOVE_SERVER:
        range_start = 0
    else:
        range_start = 1
    # Loop forever to test the controller (Stop with Ctrl+C)
    print "** Entering While Loop"
    while True:
        # Moving all hosts
        for i in range(range_start, len(h)):
            # Wait 5 secs to next move
            time.sleep(8)
            # Select new AP and random port to connect
            new = ap[randint(0, len(ap) - 1)]
            port = randint(10, 20)

            used_ports[new].append(port)
            print '* Moving', h[i], 'from', old[i], 'to', new, 'port', port
            hintf, sintf = moveHost(h[i], old[i], new, newPort=port)

            print '* ', hintf, 'is now connected to', sintf
            print '* New network:'
            printConnections(net.switches)
            old[i] = new

    # Waiting for CTRL+D to finish
    CLI(net)
    net.stop()

if __name__ == '__main__':
    mobilityTest()
