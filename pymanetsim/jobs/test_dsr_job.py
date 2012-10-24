from protocols.dsr.node import DsrNode
from protocols.dsr.dsr import DsrProtocolManager

import jobs.test_abstract_job

abstract = [jobs.test_abstract_job]

config_parameters = {
    'type_of_nodes':DsrNode,
    'protocol_manager':DsrProtocolManager,
}

y_variables = {'total_messages':DsrProtocolManager.get_total_messages_sent,
               'routes_found':DsrProtocolManager.get_routes_found,
               'search_messages':DsrProtocolManager.get_total_search_messages,
               'go_back_messages':DsrProtocolManager.get_total_go_back_messages}
job_name = "test_unit_dsr_job_manager"
