from protocols.bfg.node import BfgNode 
from protocols.bfg.bfg import BfgProtocolManager

import main_abstract

abstract = [main_abstract]

config_parameters = {
    'type_of_nodes':BfgNode,
    'protocol_manager':BfgProtocolManager,
}

protocol_parameters = {
    'random_walk_max_hop':100,
    'random_walk_multiply':-1,
}


x_variable_field = "protocol_p.random_walk_multiply"
x_variable_name = "random_walk_multiply"
x_variable_values = range(1, 9)
y_variables = {
                'total_messages':BfgProtocolManager.get_total_messages_sent,
                'routes_found':BfgProtocolManager.get_routes_found,
                'follow_heat_messages':BfgProtocolManager.get_total_follow_heat,
                'random_walk_messages':BfgProtocolManager.get_total_random_walk,
                'go_back_messages':BfgProtocolManager.get_total_go_back,
                'hello_messages':BfgProtocolManager.get_total_hello,
                'read_collision':BfgProtocolManager.get_read_collision,
              }
job_name = "bfg_normal"
