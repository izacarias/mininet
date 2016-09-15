#!/usr/bin/python


from mininet.net import Mininet
from mininet.node import RemoteController, UserSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import os

# Configurations
OF_CONTROLLER_IP = '143.54.12.179'
OF_CONTROLLER_PORT = 6633


def topology():
    "Create a network."
    c1 = RemoteController('c1', ip=OF_CONTROLLER_IP, port=OF_CONTROLLER_PORT)
    net = Mininet(controller=c1, link=TCLink, switch=UserSwitch)
    #    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
    sta = []

    print "*** Creating nodes"
    for n in range(10):
        sta.append(n)
        sta[n] = net.addStation('sta%s' % (
            n + 1), wlans=2, mac='00:00:00:00:00:%s' % (n + 1), ip='10.0.0.%s/8' % (n + 1))
    ap1 = net.addBaseStation('ap1', ssid='ap-ssid1',
                             mode='g', channel='1', position='50,115,0')
    ap2 = net.addBaseStation('ap2', ssid='ap-ssid2',
                             mode='g', channel='6', position='100,55,0')
    ap3 = net.addBaseStation('ap3', ssid='ap-ssid3',
                             mode='g', channel='11', position='100,175,0')
    ap4 = net.addBaseStation('ap4', ssid='ap-ssid4',
                             mode='g', channel='6', position='150,115,0')
#    phyap = net.addPhysicalBaseStation( 'phyap5', ssid= 'new-ssid5', mode= 'g', channel= '6', position='170,185,0', wlan='wlan1' )
    c1 = net.addController('c1', controller=RemoteController)

    print "*** Creating links"
    for station in sta:
        net.addMesh(station, ssid='meshNet')

    """uncomment to plot graph"""
    net.plotGraph(max_x=240, max_y=240)

    """Routing"""
    net.meshRouting('custom')

    """Seed"""
    net.seed(20)

    print "*** Associating and Creating links"
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)
    net.addLink(ap3, ap4)
    net.addLink(ap4, ap1)
 #   net.addLink(phyap, ap1)

    net.addOfDataPath('ap4', 'wlan0')

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
  #  phyap.start( [c1] )

    os.system('ovs-vsctl add-port ap1 wlan0')

    for station in sta:
        station.cmd('ifconfig %s-wlan1 192.168.0.%s' %
                    (station, (sta.index(station) + 1)))

#        station.cmd('iptables -A FORWARD -d 10.0.0.0/8 -i %s-wlan1 -o %s-mp0 -j ACCEPT' % (station,station))
        station.cmd(
            'iptables -A FORWARD -i %s-wlan1 -o %s-mp0 -j ACCEPT' % (station, station))
        station.cmd(
            'iptables -A FORWARD -i %s-mp0 -o %s-wlan1 -j ACCEPT' % (station, station))
        station.cmd(
            'iptables -A FORWARD -i %s-mp0 -o %s-wlan1 -m state --state ESTABLISHED,RELATED -j ACCEPT' % (station, station))
#        station.cmd('iptables -A FORWARD -i %s-wlan1 -o %s-mp0 -m state --state ESTABLISHED,RELATED -j ACCEPT' % (station, station))
        station.cmd(
            'iptables -t nat -A POSTROUTING -o %s-mp0 -j MASQUERADE' % station)
 #       station.cmd('iptables -t nat -A POSTROUTING -o %s-wlan1 -j MASQUERADE' % station)
#        station.cmdPrint('iptables -t nat -A POSTROUTING -s 10.0.0.0/8 -o %s-wlan1 -j ACCEPT' % station)
        station.cmd('sysctl -w net.ipv4.ip_forward=1')

    "*** Available models: RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWayPoint, GaussMarkov, ReferencePoint, TimeVariantCommunity ***"
    net.startMobility(startTime=0, model='RandomWalk',
                      max_x=200, max_y=220, min_v=0.1, max_v=0.2)

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
