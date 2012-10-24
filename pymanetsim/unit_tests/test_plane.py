import pdb
import unittest

import plane

from plane import Plane, Location, LocationOcuppied
from abstract_node import Node

class TestPlane(unittest.TestCase):

    def setUp(self):
        self.test_plane_5_10 = Plane(x_size=5, y_size=10)

    def test_boundaries(self):
        self.assert_(self.test_plane_5_10.get_node(Location(4, 9)) is plane.CONST_EMPTY)
        self.assertRaises(IndexError, self.test_plane_5_10.get_node, **{'location':Location(5, 9)})
        self.assertRaises(IndexError, self.test_plane_5_10.get_node, **{'location':Location(1, 10)})
        self.assert_(self.test_plane_5_10.get_node(Location(1, 9)) is plane.CONST_EMPTY)
        self.assert_(self.test_plane_5_10.get_node(Location(0, 0)) is plane.CONST_EMPTY)

    def test_node_insertion_normal(self):
        self.test_plane_5_10.insert_node(Node(node_id=1), Location(0,  0))
        self.assert_(self.test_plane_5_10.get_node(Location(0, 0)))
        self.assertFalse(self.test_plane_5_10.get_node(Location(0, 1)))
        self.test_plane_5_10.insert_node(Node(node_id=1), Location(0, 1))
        self.assert_(self.test_plane_5_10.get_node(Location(0, 1)))

    def test_node_insertion_already_ocupied(self):
        self.test_plane_5_10.insert_node(Node(node_id=1), Location(0, 0))
        self.assert_(self.test_plane_5_10.get_node(Location(0, 0)))

        self.assertRaises(LocationOcuppied, self.test_plane_5_10.insert_node, Node(2), Location(0, 0))

    def test_remove_node_existing(self):
        """
        Tests the removal of an existing node
        """
        node = Node(node_id=1)
        self.test_plane_5_10.insert_node(node, Location(0, 0))
        self.assert_(self.test_plane_5_10.get_node(Location(0, 0)))
        self.test_plane_5_10.remove_node(node)
        self.assertFalse(self.test_plane_5_10.get_node(Location(0, 0)))

    def test_plane_insertion(self):
        """
        Tests the insertion of ids in plane
        """
        my_plane = Plane(x_size=10, y_size=10)
        my_plane.insert_node(Node(node_id=1), Location(3, 4))
        my_plane.insert_node(Node(node_id=2), Location(3, 5))
        my_plane.insert_node(Node(node_id=3), Location(1, 2))

        self.assert_("1" in my_plane.all_node_ids)
        self.assert_("2" in my_plane.all_node_ids)
        self.assert_("3" in my_plane.all_node_ids)

if __name__ == '__main__':
    unittest.main()
