import pdb
import unittest

import plane_builders

from abstract_node import Node
from plane import Plane, Location

class TestPlaneBuilder(unittest.TestCase):

    def setUp(self):
        self.node_a = Node(node_id="1")
        self.node_b = Node(node_id="2")
        self.node_c = Node(node_id="3")
        self.few_nodes = {}
        self.many_nodes = {}

        few_nodes_list = Node.generate_nodes(3, Node, node_parameters={}, protocol_manager=None)
        for node in few_nodes_list:
            self.few_nodes[node.id] = node

        many_nodes_list = Node.generate_nodes(300, Node, node_parameters={}, protocol_manager=None)
        for node in many_nodes_list:
            self.many_nodes[node.id] = node

        self.plane_1 = Plane(10, 20)
        self.plane_2 = Plane(30, 30)

    def test_small_plane_builder(self):
        plane_builders.degree_plane_builder(self.plane_1, 2, 4, self.few_nodes)
        self.assertEqual(len(self.plane_1.all_node_ids), 3)

    def test_bigger_plane_builder(self):
        plane_builders.degree_plane_builder(self.plane_2, 2, 2, self.many_nodes)
        self.assertEqual(len(self.plane_2.all_node_ids), 300)

    def test_square_plane_builder(self):
        plane_builders.square_builder(self.plane_2, 2, 2, self.many_nodes)
        self.assertEqual(len(self.plane_2.all_node_ids), 300)
        self.assert_(self.plane_2.get_node(Location(0,0)))
