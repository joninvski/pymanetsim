import pdb

class Node(object):
    """
    This class represents a node
    """

    def __init__(self, node_id, location=None, power=None, node_parameters=None, protocol_manager=None):
        """
        Constructor.

        node_id - The node unique identifier
        location - The location of the node
        power - The transmission power
        node_parameters - Extra parameters passed to the node (Just a placeholder)
        protocol_manager - Just a placeholder for the concrete protocol nodes don't forget to include
        """
        self.location = location
        self.id = str(node_id)
        self.power = power or 1

    def __str__(self):
        """
        Returns the string representation of the node
        """
        return self.id

    def __cmp__(self, other_node):
        """
        Compares two nodes by their id
        """
        if isinstance(other_node, Node):
            return cmp(other_node.id, self.id)
        else:
            return cmp(other_node, self.id)

    def pass_time(self):
        """
        Tells the node that time has passed.

        This is a placeholder for classes that derive from Node to remeber to implement this function
        """
        return {'messages': [], 'asynchronous': [], 'simulator': []}

    @staticmethod
    def generate_nodes(number_to_generate, type_of_nodes, protocol_manager, node_parameters=None):
        """
        Generates nodes accourding to the parameters

        number_to_generate -- The number of nodes to generate
        type_of_nodes -- The type of nodes to generate
        protocol_manager -- The protocol manager responsible to manage this node
        node_parameters -- Specific paramaters to pass when creating the new node instances
        """
        node_parameters = node_parameters or {}

        nodes = []
        for i in xrange(1, number_to_generate + 1):
            new_node = type_of_nodes(node_id=i, node_parameters=node_parameters, protocol_manager=protocol_manager)
            nodes.append(new_node)

        return nodes
