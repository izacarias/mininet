from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import ethernet
from ryu.lib.packet import packet
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto.ether import ETH_TYPE_LLDP
# Used for Topology Discover
from ryu.topology import event
# from ryu.topology import switches
from ryu.topology.api import get_link
from ryu.topology.api import get_switch
# Used to process graphs
import networkx as nx
# Debug only
import pprint
import copy


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        # Internal representation of Network
        self.net = nx.DiGraph()

    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = datapath.ofproto_parser.OFPMatch(in_port=in_port, eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY, instructions=inst)
        datapath.send_msg(mod)

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

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        """ Handle data on receive switch features list """
        self.logger.info("Receiving a EventOFPSwitchFeatures...")
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath,
                                                 match=match,
                                                 cookie=0,
                                                 command=ofproto.OFPFC_ADD,
                                                 idle_timeout=0,
                                                 hard_timeout=0,
                                                 priority=0,
                                                 instructions=inst)
        datapath.send_msg(mod)
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # Getting data abou Event
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        # Getting packet and ether frame
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        # Getting source, destination and DatapathID
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # Ignoring LLDP packets
        if eth.ethertype == ETH_TYPE_LLDP:
            return

        # Loggin packet in messages
        self.logger.info("OFP -- EventOFPPacketIn")
        self.logger.info("... Packet in %s %s %s %s", dpid, src, dst, in_port)

        # Adding nodes to NetworkX Object
        # If the source is not in the Graph, add it to graph
        if src not in self.net:
            self.logger.info(src + "Nx -- Adding " + src)
            self.net.add_node(src)
            self.net.add_edge(dpid, src, {'port': in_port})
            self.net.add_edge(src, dpid)

        # If destination host is on graph, grab the next hop,

        self.logger.info("Nx -- Searching for " + dst)
        if dst in self.net.nodes():
            self.logger.info("Nx -- Found " + dst)
            pprint.pprint(self.net.edges())
            path = nx.shortest_path(self.net, src, dst)
            next_hop = path[path.index(dpid) + 1]
            out_port = self.net[dpid][next_hop]['port']
        else:
            # Destination not in graph, need FLOOD the packet
            self.logger.info(dst + " destination IS not in Net. FLOOD")
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a Flow in the switch, so it do not causes a
        # packet in Event next time
        if out_port != ofproto.OFPP_FLOOD:
            self.logger.info("OFP -- Adding flow to " + str(dpid))
            self.add_flow(datapath, in_port, dst, actions)

        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=msg.buffer_id,
                                  in_port=in_port,
                                  actions=actions)
        # learn a mac address to avoid FLOOD next time.
        # self.mac_to_port[dpid][src] = in_port
        # if dst in self.mac_to_port[dpid]:
        #     out_port = self.mac_to_port[dpid][dst]
        # else:
        #     out_port = ofproto.OFPP_FLOOD
        # install a flow to avoid packet_in next time
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
        #     self.add_flow(datapath, 1, match, actions)

        # data = None
        # if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #     data = msg.data

        # out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        #                           in_port=in_port, actions=actions,
        #                           data=data)
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        self.logger.info("Receiving a EventSwitchEnter...")
        # Getting switch list
        switch_list = copy.copy(get_switch(self, None))
        switches = [switch.dp.id for switch in switch_list]
        links_list = copy.copy(get_link(self, None))
        links = [(link.src.dpid, link.dst.dpid, {
                  'port': link.src.port_no}) for link in links_list]
        # Adding nodes and edges to NetworkX
        print switches
        print links

        self.net.add_nodes_from(switches)
        self.net.add_edges_from(links)
