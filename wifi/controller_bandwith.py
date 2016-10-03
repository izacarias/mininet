"""
    Controlador para suportar mobilidade de hosts utilizando
    SDN.
    Adiciona funcoes de monitoramento ao controlador "controller.py"
    Controlador desenvolvido utilizando o framework Ryu

    Disciplima: CMP 182 - Redes de Computadores I
    Professor: Dr. Luciano Paschoal Gaspary
    Autor: Iulisloi Zacarias
    E-mail: izacarias at inf dot ufrgs dot br
    Data: 27/06/2016

"""
from controller import SimpleSwitch13
from operator import attrgetter
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib import dpid as dpid_lib

import matplotlib.pyplot as plt
import time
import random

class SimpleMonitor13(SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        # local vars to calculate the bandwith
        self.time_old = 0.0
        self.time_new = 0.0
        self.bandwith_old = 0.0
        self.bandwith_new = 0.0
        self.bandwith_avg = 0.0
        # graph options
        self.ysample = random.sample(xrange(0, 100), 100)
        self.xdata = []
        self.ydata = []
        plt.show()
        self.axes = plt.gca()
        self.axes.set_xlim(0, 100)
        self.axes.set_ylim(0, 100)
        self.line, = self.axes.plot(self.xdata, self.ydata, 'r-')
        self.graph_time_step = 0

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('Register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('Unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)
            

    def _request_stats(self, datapath):
        self.logger.debug('Send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # Requesting Flow Stats
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)
        # Requesting Port Stats
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        """ Handler for Flow Stats request """
        body = ev.msg.body
        self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        """ Handler for Port Stats request """
        body = ev.msg.body
        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)
            if ev.msg.datapath.id == dpid_lib.str_to_dpid('0000000000001009') \
                    and stat.port_no == hex(1):

                if self.time_old == 0.0:
                    self.time_old = time.time()
                    self.bandwith_old = stat.tx_bytes
                    self.update_graph(self.graph_time_step, 0)

                else:
                    self.time_new = time.time()
                    self.bandwith_new = stat.tx_bytes
                    delta_bandwith = self.bandwith_new - self.bandwith_old
                    delta_time = self.time_new - self.time_old
                    bandwith_avg = (delta_bandwith * 8) / delta_time
                    self.update_graph(self.graph_time_step, bandwith_avg)

                self.graph_time_step = self.graph_time_step + 5

    def update_graph(self, time, bps):
        mbps = bps / (1024 * 1024)
        self.xdata.append(time)
        self.ydata.append(mbps)
        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        plt.draw()
        plt.pause(1e-17)
