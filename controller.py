# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import mac
from ryu.lib.packet import arp
from ryu.lib.packet import ethernet
from ryu.lib.packet import packet
# Used to process graphs
import networkx as nx
# Debug only
from pprint import pprint

# Constants for ARP FLOOD MANIPULATION
ARP_MSG_DROP = True
ARP_MSG_FLOOD = False


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.switches = []
        self.arp_table = {}
        self.sw_bcast = {}
        self.net = nx.DiGraph()
        # Neet for ARP request / response
        self.hw_addr = '0a:0a:0a:0a:0a:0a'
        self.ip_addr = '10.0.0.254'

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """ Add flow to datapath"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def delete_flow(self, datapath, eth_dst=None):
        """ Delete all flows in datapath """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        if eth_dst:
            match = parser.OFPMatch(eth_dst=eth_dst)
            mod = parser.OFPFlowMod(datapath=datapath,
                                    command=ofproto.OFPFC_DELETE,
                                    out_port=ofproto.OFPP_ANY,
                                    out_group=ofproto.OFPG_ANY,
                                    priority=1, match=match)
        else:
            for dst in self.mac_to_port[datapath.id].keys():
                match = parser.OFPMatch(eth_dst=dst)
                mod = parser.OFPFlowMod(
                    datapath, command=ofproto.OFPFC_DELETE,
                    out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                    priority=1, match=match)
                datapath.send_msg(mod)

    def _arp_handler(self, msg):
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        pkt_eth = pkt.get_protocols(ethernet.ethernet)[0]
        pkt_arp = pkt.get_protocol(arp.arp)

        if pkt_eth:
            dst = pkt_eth.dst
            src = pkt_eth.src

        # If packet is MAC Broadcast drop it
        if dst == mac.BROADCAST_STR and pkt_arp:
            self.logger.info('_arp_handler: Destination is Broadcast Addr')
            # Grab the IP address from ARP pkt
            arp_dst_ip = pkt_arp.dst_ip

            self.logger.info("Searching for %s, %s, %s in:", dpid, src,
                             arp_dst_ip)
            if (dpid, src, arp_dst_ip) in self.sw_bcast:
                if self.sw_bcast[(dpid, src, arp_dst_ip)] != in_port:
                    datapath.send_packet_out(in_port=in_port, actions=[])
                    return True
            else:
                self.sw_bcast[(dpid, src, arp_dst_ip)] = in_port
                self.logger.info("Adding %s, %s, %s to sw_bcast.", dpid,
                                 src, arp_dst_ip)
        if pkt_arp:
            opcode = pkt_arp.opcode
            arp_src_ip = pkt_arp.src_ip
            arp_dst_ip = pkt_arp.dst_ip

            if opcode == arp.ARP_REQUEST:
                if arp_dst_ip in self.arp_table:
                    actions = [parser.OFPActionOutput(in_port)]
                    # Create ARP Reply
                    arp_rply = packet.Packet()
                    arp_rply.add_protocol(ethernet.ethernet(
                        ethertype=pkt_eth.ethertype,
                        dst=src,
                        src=self.arp_table[arp_dst_ip]))
                    arp_rply.add_protocol(arp.arp(
                        opcode=arp.ARP_REPLY,
                        src_mac=self.arp_table[arp_dst_ip],
                        src_ip=arp_dst_ip,
                        dst_mac=src,
                        dst_ip=arp_src_ip))
                    arp_rply.serialize()
                    # Send packet via datapath
                    out = parser.OFPPacketOut(datapath=datapath,
                                              buffer_id=ofproto.OFP_NO_BUFFER,
                                              in_port=ofproto.OFPP_CONTROLLER,
                                              actions=actions,
                                              data=arp_rply.data)
                    datapath.send_msg(out)
                    return True
        return False

    def _get_mac_by_datapath_port(self, dpid, port):
        """ Return the MAC address by Datapath ID and Path """
        for mac_address in self.mac_to_port[dpid]:
            if self.mac_to_port[dpid][mac_address] == port:
                return mac_address
        return None

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # save the list of switches
        if datapath not in self.switches:
            self.switches.append(datapath)
            self.logger.info("Switch %s added to list", datapath.id)

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.info("packet truncated: only %s of %s bytes",
                             ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        pkt_eth = pkt.get_protocols(ethernet.ethernet)[0]
        pkt_arp = pkt.get_protocol(arp.arp)
        dst = pkt_eth.dst
        src = pkt_eth.src

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        if pkt_arp:
            # Larn MAC x IP to Global ARP Table
            self.arp_table[pkt_arp.src_ip] = src

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port.setdefault(dpid, {})
        if src not in self.mac_to_port[dpid]:
            self.logger.info('Mac2Port -- Adding [dpid=%s][mac=%s][port=%d]',
                             dpid, src, in_port)
            self.mac_to_port[dpid][src] = in_port

        self.logger.info("Searching for [dst=%s] in [dpid=%s]", dst, dpid)
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            self.logger.info('Dst in Mac2Port: [dpid=%s][mac=%s][Port=%d]',
                             dpid, dst, out_port)
        else:
            self.logger.info('Mac2Port -- Unknow MAC: [dpid=%s] [mac=%s]',
                             dpid, dst)
            if self._arp_handler(msg):
                self.logger.info('ARP FLOOD -- Discarding packages')
                return
            else:
                # ARP_MSG_FLOOD
                out_port = ofproto.OFPP_FLOOD
                self.logger.info('ARP FLOOD -- Flooding Network')

        actions = [parser.OFPActionOutput(out_port)]
        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    # Port Status Event
    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no
        dpid = msg.datapath.id
        ofproto = msg.datapath.ofproto
        mac = ""

        if reason == ofproto.OFPPR_DELETE:
            self.logger.info("Port deleted: [dpid=%s]:[port=%d]", dpid,
                             port_no)
            mac = self._get_mac_by_datapath_port(dpid, port_no)
            self.logger.info("Mac a ser removido das tabelas: %s", mac)

            # Remover de self.mac_to_port
            print("----------- mac_to_port ------------")
            pprint(self.mac_to_port)
            print("------------- sw_bcast -------------")
            # Remover de sw_broadcast
            pprint(self.sw_bcast)



# ----------- mac_to_port ------------
# {1: {'00:00:00:00:00:01': 1, '00:00:00:00:00:02': 6},
#  2: {'00:00:00:00:00:01': 2},
#  3: {'00:00:00:00:00:01': 1, '00:00:00:00:00:02': 5},
#  4: {'00:00:00:00:00:01': 4, '00:00:00:00:00:02': 5},
#  5: {'00:00:00:00:00:01': 2, '00:00:00:00:00:02': 5},
#  6: {'00:00:00:00:00:01': 2, '00:00:00:00:00:02': 1},
#  7: {'00:00:00:00:00:01': 1},
#  8: {'00:00:00:00:00:01': 1},
#  9: {'00:00:00:00:00:01': 2, '00:00:00:00:00:02': 3},
#  16: {'00:00:00:00:00:01': 2, '00:00:00:00:00:02': 3},
#  4098: {'00:00:00:00:00:01': 1},
#  4099: {'00:00:00:00:00:01': 1},
#  4100: {'00:00:00:00:00:01': 1},
#  4101: {'00:00:00:00:00:01': 1},
#  4103: {'00:00:00:00:00:01': 1},
#  4104: {'00:00:00:00:00:01': 1},
#  4105: {'00:00:00:00:00:01': 1},
#  4112: {'00:00:00:00:00:01': 1}}
# ------------- sw_bcast -------------
# {(1, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (2, '00:00:00:00:00:01', '10.0.0.2'): 2,
#  (3, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4, '00:00:00:00:00:01', '10.0.0.2'): 4,
#  (5, '00:00:00:00:00:01', '10.0.0.2'): 2,
#  (6, '00:00:00:00:00:01', '10.0.0.2'): 2,
#  (7, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (8, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (9, '00:00:00:00:00:01', '10.0.0.2'): 2,
#  (16, '00:00:00:00:00:01', '10.0.0.2'): 2,
#  (4098, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4099, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4100, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4101, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4103, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4104, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4105, '00:00:00:00:00:01', '10.0.0.2'): 1,
#  (4112, '00:00:00:00:00:01', '10.0.0.2'): 1}
