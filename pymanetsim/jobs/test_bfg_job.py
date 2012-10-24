from protocols.bfg.bfg import BfgProtocolManager
from protocols.bfg.node import BfgNode

import jobs.test_abstract_job

abstract = [jobs.test_abstract_job]

config_parameters = {
    'type_of_nodes':BfgNode,
    'protocol_manager':BfgProtocolManager,
}

y_variables = {
    'total_messages':BfgProtocolManager.get_total_messages_sent,
    'routes_found':BfgProtocolManager.get_routes_found,
    'follow_heat_messages':BfgProtocolManager.get_total_follow_heat,
    'random_walk_messages':BfgProtocolManager.get_total_random_walk,
    'go_back_messages':BfgProtocolManager.get_total_go_back,
    'hello_messages':BfgProtocolManager.get_total_hello,
    'read_collision':BfgProtocolManager.get_read_collision,
}

job_name = "test_unit_bfg_job_manager"
