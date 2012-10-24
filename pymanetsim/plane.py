import pdb
import random

CONST_EMPTY = None
CONST_EMPTY_STR = " -- "

class Plane(object):
    """
    This class represents a plane where nodes are located
    """

    def __init__(self, x_size=None, y_size=None):
        """
        Constructor.

        x_size -- The X lenght of the world
        y_size -- The Y lenght of the world
        """
        x_size = x_size or 10
        y_size = y_size or 10

        self.x_size = x_size
        self.y_size = y_size

        self.all_node_ids = []

        self.terrain = []
        for x in xrange(x_size):
            self.terrain.append([CONST_EMPTY]*y_size)

    def insert_node(self, node, location):
        """
        Inserts a node in the plane
        """
        if self.get_node(location):
            raise LocationOcuppied()

        self.terrain[location.x][location.y] = node.id
        node.location = location
        self.all_node_ids.append(node.id)

    def remove_node(self, node):
        """
        Removes a node from the plane
        """
        x, y = node.location.x, node.location.y
        self.terrain[x][y] = CONST_EMPTY

    def get_node(self, location):
        """
        Gets the node in the plane present in a specific location
        """
        return self.terrain[location.x][location.y]

    def __str__(self):
        """
        Gives the string representation of a plane
        """
        text = "\n\n"
        for x in xrange(self.x_size):
            for y in xrange(self.y_size):
                if self.terrain[x][y]:
                    text += " %03d " % int(self.terrain[x][y])
                else:
                    text += " --- "
            text += "\n\n"
        return text

    def random_location(self):
        """Chooses a random location of the plane"""
        x = random.randint(0, self.x_size - 1)
        y = random.randint(0, self.y_size - 1)

        return Location(x, y)

    def get_neighbours_ids_at_distance(self, location, distance):
        """Gets the neigbours ids of a location from the map which
        distance is less or equal to the distance argument"""
        x, y = location.x, location.y
        neighbours = []

        for i in xrange(distance, distance + 1):

            if x - i >= 0:
                self._append_if_node_exists(neighbours, x-i, y)
                if y + i < self.y_size:
                    self._append_if_node_exists(neighbours, x-i, y+i)
                if y - i >= 0:
                    self._append_if_node_exists(neighbours, x-i, y-i)

            if x + i < self.x_size:
                self._append_if_node_exists(neighbours, x+i, y)
                if y + i < self.y_size:
                    self._append_if_node_exists(neighbours, x+i, y+i)
                if y - i >= 0:
                    self._append_if_node_exists(neighbours, x+i, y-i)

            if y - i >= 0:
                self._append_if_node_exists(neighbours, x, y-i)
            if y + i < self.y_size:
                self._append_if_node_exists(neighbours, x, y+i)

        return neighbours

    def get_neighbours_ids(self, location):
        """Get the imediate neighbour ids (those who are at a distance of 1)"""
        return self.get_neighbours_ids_at_distance(location, distance=1)

    def _append_if_node_exists(self, node_list, x, y):
        if not (self.terrain[x][y] == CONST_EMPTY):
            node_list.append(self.terrain[x][y])

    def get_empty_space_around(self, location):
        """Returns the locations which are empty around the specified location"""
        x, y = location.x, location.y
        found = None

        if x - 1 >= 0:
            if not self.terrain[x-1][y]:
                found = Location(x-1, y)
            if y + 1 < self.y_size:
                if not self.terrain[x-1][y+1]:
                    found = Location(x-1, y+1)
            if y - 1 >= 0:
                if not self.terrain[x-1][y-1]:
                    found = Location(x-1, y-1)

        if x + 1 < self.x_size:
            if not self.terrain[x+1][y]:
                found = Location(x+1, y)
            if y + 1 < self.y_size:
                if not self.terrain[x+1][y+1]:
                    found = Location(x+1, y+1)
            if y - 1 >= 0:
                if not self.terrain[x+1][y-1]:
                    found = Location(x+1, y-1)

        if y - 1 >= 0:
            if not self.terrain[x][y-1]:
                found = Location(x, y-1)
        if y + 1 < self.y_size:
            if not self.terrain[x][y+1]:
                found = Location(x, y+1)

        return found

    def get_all_empty_locations(self):
        """Gets all empty location present on the map"""
        empty_locations = []
        for x in xrange(0, self.x_size):
            for y in xrange(0, self.y_size):
                if self.terrain[x][y] == CONST_EMPTY:
                    empty_locations.append(Location(x, y))

        return empty_locations

    def get_random_empty_location(self):
        """Chooses an empty random location from the map"""
        return random.choice(self.get_all_empty_locations())

    def get_mean_degree(self, all_nodes):
        """Calculates the mean degree of neighbours in the map"""
        sum_neighbors = 0
        for node in all_nodes:
            sum_neighbors += len(self.get_neighbours_ids(node.location))

        return float(sum_neighbors) / len(all_nodes)

    @staticmethod
    def generate_plane(all_nodes, plane_parameters):
        """Generates a pane with the specified plane parameters"""

        plane = Plane(plane_parameters['x_size'], plane_parameters['y_size'])
        plane_parameters['plane_builder_method'](plane, plane_parameters['min_degree'], plane_parameters['max_degree'], all_nodes)

        return plane

    @staticmethod
    def load_plane(plane_parameters, type_of_nodes, node_parameters, protocol_manager):
        """Loads a plane present in a file"""
        file_path = plane_parameters['scenario_file']
        f = open(file_path, "r")

        scenario = f.read()
        return Plane.load(scenario, type_of_nodes, node_parameters, protocol_manager)

    @staticmethod
    def load(scenario, type_of_nodes, node_parameters, protocol_manager):
        """
        Loads a simulation according to the given parameters
        """
        x_size, y_size = scenario.splitlines()[0].split()
        x_size, y_size = int(x_size), int(y_size)
        nodes_in_file = scenario.splitlines()[1:]

        plane = Plane(x_size=x_size, y_size=y_size)
        all_nodes = {}

        for line in nodes_in_file:
            node_id, x, y = line.split()
            location = Location(int(x), int(y))

            if(location.x >= x_size or location.y >= y_size):
                raise Exception("Trying to load  node %s outside boundaries" % (node_id))

            node = type_of_nodes(node_id=node_id, node_parameters=node_parameters, protocol_manager=protocol_manager)
            plane.insert_node(node=node, location=location)
            all_nodes[node.id] = node

        return all_nodes, plane

class Location(object):
    """
    This class represents a location in the plane
    """

    def __init__(self, x_position, y_position):
        """
        Constructor.

        x_position -- The x position of the location
        y_position -- The y position of the location
        """
        self.x = x_position
        self.y = y_position

    def __str__(self):
        return "[%d %d]" % (self.x, self.y)

    def __cmp__(self, other_location):
        if isinstance(other_location, Location):
            return cmp("%d-%d" % (other_location.x, other_location.y), "%d-%d" % (self.x, self.y))
        else:
            return cmp(other_location, "%d-%d" % (self.x, self.y))

class LocationOcuppied(Exception):
    """
    This class represents the exception when trying to
    insert a node where there is already a node
    """
    pass
