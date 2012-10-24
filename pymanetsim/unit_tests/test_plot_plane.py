import unittest

import plot_plane

from plane import Plane, Location, LocationOcuppied
from abstract_node import Node

class TestPlotPlane(unittest.TestCase):

    def setUp(self):
        self.test_plane = Plane(x_size=5, y_size=10)
        node_a = Node(node_id=1)
        node_b = Node(node_id=2)
        node_c = Node(node_id=3)

        self.all_nodes = {1:node_a, 2:node_b, 3:node_c}

        self.test_plane.insert_node(node_a, Location(0, 0))
        self.test_plane.insert_node(node_b, Location(2, 1))
        self.test_plane.insert_node(node_c, Location(1, 2))


    def test_plot(self):
        """
        Tests the removal of an existing node
        """
        plot_plane.plot_plane(self.test_plane, self.all_nodes, 'unit_test_plot_plane')

if __name__ == '__main__':
    unittest.main()
