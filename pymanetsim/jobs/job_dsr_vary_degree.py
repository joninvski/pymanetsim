from protocols.dsr.node import DsrNode
from protocols.dsr.dsr import DsrProtocolManager

import vary_degree_abstract

abstract = [vary_degree_abstract]

config_parameters = {
    'type_of_nodes':DsrNode,
    'protocol_manager':DsrProtocolManager,
}

y_variables = {'total_messages':DsrProtocolManager.get_total_messages_sent,
               'routes_found':DsrProtocolManager.get_routes_found,
               'search_messages':DsrProtocolManager.get_total_search_messages,
               'go_back_messages':DsrProtocolManager.get_total_go_back_messages}
job_name = "dsr_normal"
