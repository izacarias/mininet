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

from mininet.net import Mininet, CLI
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import LinearTopo
from mininet.log import output, warn
from mininet.term import makeTerm, runX11

from random import randint
import time


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


def vlcCommand(type=''):
    baseCommand = 'vlc-wrapper '
    if (type == 'server'):
        # media_file = '/home/mininet/720x480_5mb.mp4'
        media_file = '/home/mininet/360x240_2mb.mp4'
        # baseCommand += '-vvv '
        baseCommand += media_file + ' '
        baseCommand += '-I dummy '
        baseCommand += '--sout '
        baseCommand += "'#transcode{vcodec=mp4v,acodec=none,vb=800,ab=128}"
        baseCommand += ":standard{access=http,mux=ogg,dst=:8080}' "
        baseCommand += '--loop '
        baseCommand += '--sout-keep '
        return baseCommand

    if (type == 'client'):
        baseCommand += 'http://10.0.0.1:8080 '
        baseCommand += '--no-audio'
        return baseCommand


def mobilityTest():
    "A simple test of mobility"

    # Creating remote controller
    c1 = RemoteController('c1', ip='192.168.56.1', port=6633)

    # Creating MobilitySwitch with compatible version
    print '* Simple mobility test'
    net = Mininet(topo=LinearTopo(3), switch=MobilitySwitch, controller=c1)
    print '* Starting network:'
    net.start()
    printConnections(net.switches)
    print '* Testing network'
    # net.pingAll()
    print '* Identifying switch interface for h1'
    h1, h2, old = net.get('h1', 'h2', 's1')
    # Running VLC Player
    print vlcCommand('server')
    makeTerm(h1, title='Streamer', cmd=vlcCommand('server'))
    time.sleep(1)  # waiting for streaming server (1 sec)
    makeTerm(h2, title='Client', cmd=vlcCommand('client'))
    print "After H1 Terminal"

    CLI(net)

    # Loop forever to test the controller (Stop with Ctrl+C)
#    while True:
#        pass
#        for s in 2, 3, 1:
#            new = net['s%d' % s]
#            port = randint(10, 20)
#            print '* Moving', h1, 'from', old, 'to', new, 'port', port
#            hintf, sintf = moveHost(h1, old, new, newPort=port)
#            print '*', hintf, 'is now connected to', sintf
#            print '* Clearing out old flows'
#            for sw in net.switches:
#                sw.dpctl('del-flows')
#            print '* New network:'
#            printConnections(net.switches)
#            print '* Testing connectivity:'
#            net.pingAll()
#            old = new
    net.stop()

if __name__ == '__main__':
    mobilityTest()
