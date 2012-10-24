import pdb
import unittest

from simulator import Simulation, SimulationParameters, ConfigurationParameters, PlaneParameters
from protocols.dsr.node import DsrNode
from protocols.bfg.node import BfgNode
from events import RouteFoundEvent
from abstract_node import Node

from protocols.dsr.node import LookForDestination as LookForDestinationDsr
from protocols.bfg.node import LookForDestination as LookForDestinationBfg

from protocols.bfg.bfg import BfgProtocolManager
from protocols.dsr.dsr import DsrProtocolManager

import plane_builders

class TestBigSim(unittest.TestCase):
    def setUp(self):
        Node.node_counter = 0
        self.event_a = LookForDestinationDsr("1", "30")

    def test_dsr_with_generated_plane(self):
        config_p = ConfigurationParameters(max_cycles=80, events=[], type_of_nodes=DsrNode, protocol_manager=DsrProtocolManager)
        plane_p = PlaneParameters(x_size=30, y_size=30, min_degree=2, max_degree=2, number_of_nodes=300, plane_builder_method=plane_builders.degree_plane_builder)
        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)

        sim1 = Simulation(simulation_parameters)
        print sim1.plane

        sim1.run(cycles_to_run=4)
        event = LookForDestinationDsr(origin_id="1", destiny_id="17")
        sim1.event_broker.add_asynchronous_event(event)
        sim1.run()

        new_event = sim1.event_broker.get_simulator_event()
        self.assertTrue(isinstance(new_event, RouteFoundEvent))

    def test_bfg_with_low_degree_generated_plane(self):
        config_p = ConfigurationParameters(max_cycles=80, events=[], type_of_nodes=BfgNode, protocol_manager=BfgProtocolManager)
        plane_p = PlaneParameters(x_size=20, y_size=20, min_degree=2, max_degree=2, number_of_nodes=300, plane_builder_method=plane_builders.degree_plane_builder)
        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)

        sim1 = Simulation(simulation_parameters)
        print sim1.plane

        sim1.run(cycles_to_run=4)
        event = LookForDestinationBfg("1", "16")
        sim1.event_broker.add_asynchronous_event(event)
        sim1.run()

        new_event = sim1.event_broker.get_simulator_event()
        self.assertTrue(isinstance(new_event, RouteFoundEvent))

    def test_bfg_with_high_degree_generated_plane(self):
        config_p = ConfigurationParameters(max_cycles=80, events=[], type_of_nodes=BfgNode, protocol_manager=BfgProtocolManager)
        plane_p = PlaneParameters(x_size=20, y_size=20, min_degree=5, max_degree=8, number_of_nodes=300, plane_builder_method=plane_builders.degree_plane_builder)
        simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)

        sim1 = Simulation(simulation_parameters)
        print sim1.plane

        sim1.run(cycles_to_run=4)
        event = LookForDestinationBfg("1", "16")
        sim1.event_broker.add_asynchronous_event(event)
        sim1.run()

        new_event = sim1.event_broker.get_simulator_event()
        self.assertTrue(isinstance(new_event, RouteFoundEvent))

if __name__ == '__main__':
    unittest.main()

def test_single_test(test_name):
    TestBigSim(methodName=test_name).debug()
