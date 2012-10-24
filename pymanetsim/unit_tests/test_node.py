import pdb
import unittest

from abstract_node import Node
from plane import Location

class TestNode(unittest.TestCase):
    def setUp(self):
        self.loc_a = Location(0, 0)
        self.loc_b = Location(3, 2)
        self.loc_c = Location(3, 2)

        self.node_a = Node(node_id='1', location=self.loc_a)
        self.node_b = Node(node_id='1', location=self.loc_b)
        self.node_c = Node(node_id='2', location=self.loc_b)

    def test_node_comparition(self):
        self.assertEqual(self.node_a, self.node_b)
        self.assertNotEqual(self.node_a, self.node_c)
        self.assertNotEqual(self.node_a, "DIFFERENT_OBJECT")

    def test_node_print(self):
        self.assertEqual(str(self.node_a), '1')
        self.assertEqual(str(self.node_b), '1')
        self.assertEqual(str(self.node_c), '2')

    def test_node_generation(self):
        generated_nodes = Node.generate_nodes(20, Node, protocol_manager=None)
        self.assertEqual(len(generated_nodes), 20)

        for n in generated_nodes:
            self.assert_(isinstance(n, Node))

if __name__ == '__main__':
    unittest.main()
