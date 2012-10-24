import pdb
import unittest

from events import RouteFoundEvent

import plane_builders

from abstract_node import Node
from simulator import Simulation, NodeParameters, ConfigurationParameters, ProtocolParameters, PlaneParameters, SimulationParameters
from protocols.dsr.node import DsrNode, SearchTargetMessage
from protocols.bfg.node import BfgNode

from protocols.dsr.node import LookForDestination as Look_For_Destination_DSR
from protocols.dsr.dsr import DsrProtocolManager
from protocols.bfg.node import LookForDestination as Look_For_Destination_BFG
from protocols.bfg.bfg import BfgProtocolManager

MAP_DIR = "../maps/"

class TestSim(unittest.TestCase):
    def setUp(self):
        Node.node_counter = 0

        self.node_a = DsrNode()
        self.node_b = DsrNode()
        self.event_a = Look_For_Destination_DSR(self.node_a.id, self.node_b.id)

    def test_sim_creation_generated(self):
        plane_p = PlaneParameters(x_size = 100, y_size = 100, min_degree=100, max_degree=100, number_of_nodes=5, plane_builder_method=plane_builders.degree_plane_builder)
        protocol_p = ProtocolParameters(arguments={})
        node_p = NodeParameters(arguments={})
        config_p = ConfigurationParameters(max_cycles=10, events=[self.event_a], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)

        simulation_parameters = SimulationParameters(plane_parameters=plane_p, protocol_parameters=protocol_p, node_parameters=node_p, config_parameters=config_p)

        sim1 = Simulation(simulation_parameters)

        self.assertEqual(len(sim1.all_nodes),  5)
        self.assertEqual(sim1._max_cycles, 10)

    def test_sim_creation_loaded(self):
        config_p = ConfigurationParameters(max_cycles=2, events=[], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)
        plane_p = PlaneParameters(scenario_file= MAP_DIR + "map2.txt")

        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)

        sim1 = Simulation(simulation_parameters)

        self.assertEqual(len(sim1.all_nodes),  28)
        self.assertEqual(sim1._max_cycles, 2)

    def test_sim_dsr_route_find(self):
        event = Look_For_Destination_DSR("1", "3")
        config_p = ConfigurationParameters(max_cycles=6, events=[event], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)
        plane_p = PlaneParameters(scenario_file = MAP_DIR + "map1.txt")

        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)

        sim1 = Simulation(simulation_parameters)

        sim1.run(cycles_to_run=1)

        new_sim_event = sim1.event_broker.get_simulator_event()
        new_message = sim1.message_broker.get_message_to_be_transmitted()
        sim1.message_broker.add_to_be_transmitted(new_message)

        self.assertFalse(new_sim_event)
        self.assertTrue(isinstance(new_message, SearchTargetMessage))
        self.assertFalse(sim1.event_broker.get_asynchronous_event())

        sim1.run()
        new_sim_event = sim1.event_broker.get_simulator_event()
        new_message = sim1.message_broker.get_message_to_be_transmitted()

        self.assertTrue(isinstance(new_sim_event, RouteFoundEvent))
        self.assertFalse(new_message)
        self.assertFalse(sim1.event_broker.get_asynchronous_event())

    def test_sim_bfg_route_find_easy(self):
        config_p = ConfigurationParameters(max_cycles=40, events=[], type_of_nodes=BfgNode, protocol_manager=BfgProtocolManager)
        plane_p = PlaneParameters(scenario_file = MAP_DIR + "map1.txt")
        protocol_p = ProtocolParameters(arguments={'random_walk_max_hop':100, 'random_walk_multiply':1})

        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p, protocol_parameters=protocol_p)

        sim1 = Simulation(simulation_parameters)

        sim1.run(cycles_to_run=10)
        event = Look_For_Destination_BFG("1", "3", random_walk_multiply=1, random_walk_max_hop=100)
        new_event = sim1.event_broker.add_asynchronous_event(event)

        sim1.run()
        new_event = sim1.event_broker.get_simulator_event()
        self.assertTrue(isinstance(new_event, RouteFoundEvent))

        self.assertTrue(new_event.arguments['route'])

    def test_sim_bfg_route_find_hard(self):
        config_p = ConfigurationParameters(max_cycles=100, events=[], type_of_nodes=BfgNode, protocol_manager=BfgProtocolManager)
        plane_p = PlaneParameters(scenario_file = MAP_DIR + "map2.txt")
        protocol_p = ProtocolParameters(arguments={'random_walk_max_hop':100, 'random_walk_multiply':1})

        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p, protocol_parameters=protocol_p)

        sim1 = Simulation(simulation_parameters)

        sim1.run(cycles_to_run=3)
        event = Look_For_Destination_BFG(origin_id="1", destiny_id="16", random_walk_multiply=1, random_walk_max_hop=100)
        new_event = sim1.event_broker.add_asynchronous_event(event)

        sim1.run()
        new_event = sim1.event_broker.get_simulator_event()
        self.assertTrue(isinstance(new_event, RouteFoundEvent))

    def test_simulator_node_parameters(self):
        node_parameters = NodeParameters({'NODE_arg_1':'something'})
        self.assertEqual(node_parameters['NODE_arg_1'], 'something')

    def test_simulator_simulation_parameters(self):
        sim_parameters = ConfigurationParameters(max_cycles=10, events=[self.event_a], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)

        self.assertEqual(sim_parameters['max_cycles'], 10)
        self.assertEqual(sim_parameters['events'], [self.event_a])
        self.assertEqual(sim_parameters['type_of_nodes'], DsrNode)

    def test_simulator_plane_parameters_b(self):
        plane_parameters = PlaneParameters({'x_size':10, 'y_size':30, 'min_degree':3, 'max_degree':8})

        self.assertEqual(plane_parameters['x_size'], 10)
        self.assertEqual(plane_parameters['y_size'], 30)

if __name__ == '__main__':
    unittest.main()
