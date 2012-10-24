from protocols.dsr.dsr import DsrProtocolManager
from protocols.dsr.node import DsrNode

import vary_number_nodes_abstract

abstract = [vary_number_nodes_abstract]

config_parameters = {
    'type_of_nodes':DsrNode,
    'protocol_manager':DsrProtocolManager,
}

y_variables = {'total_messages':DsrProtocolManager.get_total_messages_sent,
               'routes_found':DsrProtocolManager.get_routes_found}
job_name = "dsr_normal"
