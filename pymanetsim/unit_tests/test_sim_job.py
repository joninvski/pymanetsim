import pdb
import unittest
import os

from simulator import NodeParameters, ConfigurationParameters, ProtocolParameters, PlaneParameters, SimulationParameters

from protocols.dsr.node import DsrNode

from protocols.dsr.node import LookForDestination as LookForDestinationDsr
from protocols.dsr.dsr import DsrProtocolManager

from sim_job import Job
from configuration import DATA_RAW_PATH

import plane_builders


import sim_job

class TestSimJob(unittest.TestCase):
    def setUp(self):
        self.event_a = LookForDestinationDsr("1", "50")

    def test_job_simple_execution(self):
        #Now let's check the output
        path = DATA_RAW_PATH + "test_dsr_degree_messages.txt"

        #Lets be clean and remove for the others
        if os.path.isfile(path):
            os.remove(path)

        plane_p = PlaneParameters(x_size = 20, y_size = 20, min_degree=-1, max_degree=7, number_of_nodes=30, plane_builder_method=plane_builders.degree_plane_builder)
        protocol_p = ProtocolParameters(arguments={})
        node_p = NodeParameters(arguments={})
        config_p = ConfigurationParameters(max_cycles=100, events=[self.event_a], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)

        simulation_parameters = SimulationParameters(plane_parameters=plane_p, protocol_parameters=protocol_p, node_parameters=node_p, config_parameters=config_p)

        job = Job(job_name="test_dsr", simulation_parameters=simulation_parameters, x_variable_field="plane_p.min_degree", \
                  x_variable_name="degree", x_variable_values=[2, 3, 4, 5, 6, 7], y_variables={'messages':DsrProtocolManager.get_total_messages_sent})

        self.assertTrue(job)

        #Now let's check the output
        path = DATA_RAW_PATH + "test_dsr_degree_messages.txt"

        file_obj = open(path)
        self.assertTrue(file_obj)

        all_lines = file_obj.readlines()
        self.assertEqual(['2.000000 30\n', '3.000000 30\n', '4.000000 30\n', '5.000000 30\n', '6.000000 30\n', '7.000000 30\n'], all_lines)

    def test_job_values_that_vary(self):
        plane_p = PlaneParameters(x_size= 20, y_size = 20, min_degree=3, max_degree=3, number_of_nodes=1, plane_builder_method=plane_builders.degree_plane_builder)
        protocol_p = ProtocolParameters()
        node_p = NodeParameters()
        config_p = ConfigurationParameters(max_cycles=100, events=[self.event_a], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)

        simulation_parameters = SimulationParameters(plane_parameters=plane_p, protocol_parameters=protocol_p, node_parameters=node_p, config_parameters=config_p)

        job = Job(job_name="test_dsr", simulation_parameters=simulation_parameters, x_variable_field="plane_p['number_of_nodes']", \
                  x_variable_name="number_of_nodes", x_variable_values=range(10, 200, 30), y_variables={'messages':DsrProtocolManager.get_total_messages_sent})

        self.assertTrue(job)

        self.assertEqual(len(job.sim.all_nodes), 190)

        #Now let's check the output
        path = DATA_RAW_PATH + "test_dsr_number_of_nodes_messages.txt"

        file_obj = open(path)
        self.assertTrue(file_obj)

        all_lines = file_obj.readlines()
        self.assertEqual('10.000000 10\n', all_lines[0]) #If this fails it is probably form the file which wansn't \q

        # Lets be clean and remove for the others
        os.remove(path)

    def test_job_set_attribute_recursively(self):
        plane_p = PlaneParameters(x_size= 20, y_size = 20, min_degree=3, max_degree=3, number_of_nodes=1)
        protocol_p = ProtocolParameters(arguments={})
        node_p = NodeParameters(arguments={})
        config_p = ConfigurationParameters(max_cycles=100, events=[self.event_a], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)

        simulation_parameters = SimulationParameters(plane_parameters=plane_p, protocol_parameters=protocol_p, node_parameters=node_p, config_parameters=config_p)

        self.assertEqual(simulation_parameters.plane_p['number_of_nodes'], 1)
        sim_job._set_attribute_recursively(simulation_parameters, "plane_p['number_of_nodes']", 10)
        self.assertNotEqual(simulation_parameters.plane_p['number_of_nodes'], 1)
        self.assertEqual(simulation_parameters.plane_p['number_of_nodes'], 10)
        sim_job._set_attribute_recursively(simulation_parameters, "plane_p['number_of_nodes']", 30)
        self.assertEqual(simulation_parameters.plane_p['number_of_nodes'], 30)

if __name__ == '__main__':
    unittest.main()
