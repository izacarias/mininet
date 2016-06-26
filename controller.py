from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
# Used for topology discover
from ryu.topology import event
from ryu.topology.api import get_host
from ryu.topology.api import get_link
from ryu.topology.api import get_switch
# NetworkX for Graphs
import networkx as nx
# Python Standard Library (Python STL)
# import copy
from pprint import pprint
import logging


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.switches = []
        # Stores the network Graph
        self.net = nx.DiGraph()
        self.stp = nx.Graph()
        # Set Log Level
        self.logger.setLevel(logging.DEBUG)

    # Utility function: lists all attributes in in object
    def ls(self, obj):
        print("\n".join([x for x in dir(obj) if x[0] != "_"]))

    # -------------------- Flow Manipulation --------------------

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        # Flow will expire in 5 seconds without traffic (unused)
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst, idle_timeout=5)
        datapath.send_msg(mod)
        # self.logger.debug('[ADD_FLOW] dpid=')

    def delete_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        for dst in self.mac_to_port[datapath.id].keys():
            match = parser.OFPMatch(eth_dst=dst)
            mod = parser.OFPFlowMod(
                datapath, command=ofproto.OFPFC_DELETE,
                out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                priority=1, match=match)
            datapath.send_msg(mod)

    # def get_network_topology(self, ev):
    #     self.net.clear()
    #     # Getting Switches Info (Nodes)
    #     switch_list = get_switch(self, None)
    #     for switch in switch_list:
    #         self.net.add_node(switch.dp.id)
    #     # Getting Links Info
    #     links_list = get_link(self, None)
    #     for link in links_list:
    #         src_dpid = link.src.dpid
    #         dst_dpid = link.dst.dpid
    #         src_port_no = link.src.port_no
    #         dst_port_no = link.dst.port_no
    #         # Adding links do Directions Graph
    #         self.net.add_edge(src_dpid, dst_dpid, {'port': src_port_no})
    #         self.net.add_edge(dst_dpid, src_dpid, {'port': dst_port_no})
    #     # self.logger.debug("[NetworkX] -- Topology Complete")

    # ------------------ Topology Functions -------------------
    def add_switch(self, ev):
        switch = ev.switch
        self.switches.append(switch.dp)
        dpid = switch.dp.id
        # Adding switch node
        if dpid == 0:
            self.net.add_node('0', n_type='switch', has_host='false')
        else:
            self.net.add_node(dpid, n_type='switch', has_host='false')

    def search_host(self, dpid):
        hosts = get_host(self, dpid)
        print '###############################'
        pprint(hosts)

    def discover_by_arp(self, datapath, msg):
        # Convert DiGraph to undirected Graph
        # ud_net = self.net.to_undirected()
        # stp_graph = nx.minimum_spanning_tree(ud_net)
        # target_ports = []
        # excluded_ports = []
        # for edge in stp_graph.edges():
        #     opose_sw = None
        #     if datapath.id == edge[0]:
        #         opose_sw = edge[1]
        #     if datapath.id == edge[1]:
        #         opose_sw = edge[0]
        #     if opose_sw:
        pass

    # -------------------- Topology events --------------------
    @set_ev_cls(event.EventSwitchEnter, MAIN_DISPATCHER)
    def switch_enter_handler(self, ev):
        # self.logger.debug("[Event] -- SwitchEnter")
        # self.get_network_topology(ev)
        self.add_switch(ev)

    @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
    def link_add_handler(self, ev):
        link = ev.link
        src_dpid = link.src.dpid
        dst_dpid = link.dst.dpid
        src_port_no = link.src.port_no
        dst_port_no = link.dst.port_no
        # Adding a edge from source datapath to destination datapath
        # UpLink
        self.net.add_edge(src_dpid, dst_dpid, {'port': src_port_no})
        # DownLink
        self.net.add_edge(dst_dpid, src_dpid, {'port': dst_port_no})

    @set_ev_cls(event.EventHostAdd, MAIN_DISPATCHER)
    def host_add_handler(self, ev):
        # host = ev.host
        # pprint(host.to_dict())
        # {'ipv4': ['10.0.0.1'],
        #  'ipv6': [],
        #  'mac': '00:00:00:00:00:01',
        #  'port': {'dpid': '0000000000000001',
        #           'hw_addr': '12:54:79:4c:14:83',
        #           'name': u's1-eth1',
        #           'port_no': '00000001'}}
        pass

    # -------------------- OpenFlow events --------------------
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        ofpport = msg.desc
        dpid_str = dpid_lib.dpid_to_str(datapath.id)
        # Detecting a host down (Possibly moving?)
        if msg.reason == ofproto.OFPPR_MODIFY \
                and ofpport.state == ofproto.OFPPS_LINK_DOWN:
            port_no = ofpport.port_no
            hw_addr = ofpport.hw_addr
            # -------------------------------
            # TODO: Remove from Network GRAPH
            # TODO: Remove flow from switches (all dpids)
            # self.logger.debug('Host Down: [dpid=%s] [port=%d] [hw_addr=%s]',
            #                   dpid_str, port_no, hw_addr)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

        # Discards truncated packets
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("Packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)

        # event data
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Extract data from packets
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        # Ignoring LLDP packet
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        # self.mac_to_port.setdefault(dpid, {})
        # Logging Packet in event
        self.logger.info("Packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        # self.mac_to_port[dpid][src] = in_port
        if src not in self.net:
            # make sure it's a host address
            if "00:00:00" in src:
                self.net.add_node(src, n_type='host')
                self.net.add_edge(src, dpid, {'port': in_port})
                self.net.add_edge(dpid, src, {'port': in_port})
                self.net.node[dpid]['has_host'] = 'true'

            self.logger.debug('Host added: [%s]->[dpid:%s][port=%d]',
                              src, dpid, in_port)
            # TODO: Test without return
            # return
        # Try to get the destination from Network Graph
        # if dst in self.mac_to_port[dpid]:
        #     out_port = self.mac_to_port[dpid][dst]
        # else:
        #     out_port = ofproto.OFPP_FLOOD
        # pprint(self.net.nodes())
        if dst in self.net.nodes() and src in self.net.nodes():
            self.log.debug('Host in graph: %s', dst)
            try:
                path = nx.shortest_path(self.net, src, dst)
                # TODO: Add to cache paths?
            except Exception as e:
                self.logger.info(e)
                # there isn't a path, nothing to do
                return
            # make a path flow to packet
            next_switch = path[path.index(dpid) + 1]
            # get the port for next hop in path
            out_port = self.net[dpid][next_switch]['port']

            # Install a flow in switch to avoid pkt_in next time
            actions = [parser.OFPActionOutput(out_port)]
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

            # Forward packet to the next switch
            data = None
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                data = msg.data
            out = parser.OFPPacketOut(datapath=datapath,
                                      buffer_id=msg.buffer_id, in_port=in_port,
                                      actions=actions, data=data)
            datapath.send_msg(out)
        else:
            # Unknow destination. Nothing to do
            ports_to_send = []
            mst = nx.minimum_spanning_tree(self.net.to_undirected())
            edges_st = [(s, d, port)
                        for s, d, port in self.net.edges(data=True)
                        if ((s, d) in mst.edges() or
                            (d, s) in mst.edges())]
            for s, d, attrib in edges_st:
                if s == dpid:
                    ports_to_send.append(attrib['port'])
            # Forward ARP request
            actions = []
            # If there are ports to send (without loop)
            if ports_to_send:
                for p_flood in ports_to_send:
                    actions.append(parser.OFPActionOutput(p_flood))
                data = None

                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data
                out = parser.OFPPacketOut(datapath=datapath,
                                          buffer_id=msg.buffer_id,
                                          in_port=in_port, actions=actions,
                                          data=data)
                datapath.send_msg(out)
