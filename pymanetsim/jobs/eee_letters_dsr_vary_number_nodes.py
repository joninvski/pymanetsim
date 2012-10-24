from protocols.dsr.dsr import DsrProtocolManager
from protocols.dsr.node import DsrNode
import eee_letters_dsr_vary_number_nodes

abstract = [eee_letters_dsr_vary_number_nodes]

config_parameters = {
    'type_of_nodes':DsrNode,
    'protocol_manager':DsrProtocolManager,
}

y_variables = {'total_messages':DsrProtocolManager.get_total_messages_sent,
               'routes_found':DsrProtocolManager.get_routes_found,
               'search_messages':DsrProtocolManager.get_total_search_messages,
               'go_back_messages':DsrProtocolManager.get_total_go_back_messages}
job_name = "eee_dsr_normal"
