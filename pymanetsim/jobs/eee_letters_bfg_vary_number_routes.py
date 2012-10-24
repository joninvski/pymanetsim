from protocols.bfg.node import BfgNode
from protocols.bfg.bfg import BfgProtocolManager
import eee_letters_number_routes_abstract

abstract = [eee_letters_number_routes_abstract]

config_parameters = {
    'type_of_nodes':BfgNode,
    'protocol_manager':BfgProtocolManager,
}

protocol_parameters = {
    'random_walk_max_hop':170,
    'random_walk_multiply':1
}


y_variables = {
    'total_messages':BfgProtocolManager.get_total_messages_sent,
    'routes_found':BfgProtocolManager.get_routes_found,
    'follow_heat_messages':BfgProtocolManager.get_total_follow_heat,
    'random_walk_messages':BfgProtocolManager.get_total_random_walk,
    'dsr_messages':BfgProtocolManager.get_total_random_walk,
    'go_back_messages':BfgProtocolManager.get_total_go_back,
    'hello_messages':BfgProtocolManager.get_total_hello,
    'dsr_messages':BfgProtocolManager.get_total_dsr,
    'read_collision':BfgProtocolManager.get_read_collision,
}

job_name = "eee_bfg_normal"
