import random

from plane import Location

def square_builder(plane, min_degree, max_degree, all_nodes):
    """Build planes where the nodes are place in a square

    The building algorithm for 8 nodes is this

    X

    X X
    X X

    X X
    X X X
    X X X

    """
    y_lines = plane.y_size
    x_lines = plane.x_size

    node_list = all_nodes.values()

    random.shuffle(node_list)
    plane.insert_node(node_list.pop(), Location(0, 0))

    for y in xrange(1, y_lines):
        for x in xrange(0, x_lines):
            if not node_list:
                return

            if plane.get_node(Location(x, y - 1)) != None:
                plane.insert_node(node_list.pop(), Location(x, y))

            else:
                plane.insert_node(node_list.pop(), Location(x, y))
                plane.insert_node(node_list.pop(), Location(x, y-1))

def triangle_builder(plane, min_degree, max_degree, all_nodes):
    """Build planes where the nodes are place in a triangle -- "Doesn't seem to be working"

    The building algorithm for 6 nodes is this

    X

    X
    X X

    X
    X X
    X X X
    """
    y_lines = plane.y_size
    x_lines = plane.x_size

    node_list = all_nodes.values()

    random.shuffle(node_list)
    plane.insert_node(node_list.pop(), Location(0, 0))

    for y in xrange(1, y_lines):
        for x in xrange(0, x_lines):
            if not node_list:
                return

            if plane.get_node(Location(x, y - 1)) != None:
                plane.insert_node(node_list.pop(), Location(x, y))

            else:
                plane.insert_node(node_list.pop(), Location(x, y))



def degree_plane_builder(plane, min_degree, max_degree, all_nodes=None):
    """Builds a plane which respects the min_degree and max_degree of neighbours passes (KIND OF!!!)"""
    inserted_nodes = {}
    node_list = all_nodes.values()

    for node_iterator in xrange(0, len(node_list)):
        inserted_nodes = _make_sure_node_has_degree(node=node_list[node_iterator], plane=plane,
                                  min_degree=min_degree, max_degree=max_degree,
                                  remaining_nodes=node_list[node_iterator+1:], inserted_nodes=inserted_nodes)

def _make_sure_node_has_degree(node, plane, min_degree, max_degree, remaining_nodes, inserted_nodes):
    if not node in inserted_nodes:
        empty_locations = plane.get_all_empty_locations()

        if not empty_locations:
            return inserted_nodes

        #Let's try to choose one empty location with a neighbour
        empty_location_with_neighbours = _choose_empty_location_with_neighbour(plane, empty_locations)

        plane.insert_node(node, empty_location_with_neighbours)
        inserted_nodes[node] = empty_location_with_neighbours

    number_of_neighbours = len(plane.get_neighbours_ids(inserted_nodes[node]))
    desired_degree = random.randint(min_degree, max_degree)

    while remaining_nodes and number_of_neighbours < desired_degree:
        empty_space = plane.get_empty_space_around(inserted_nodes[node])
        if not empty_space:
            break

        node_to_insert = remaining_nodes[0]
        if node_to_insert in inserted_nodes:
            break

        plane.insert_node(node_to_insert, empty_space)
        inserted_nodes[node_to_insert] = empty_space
        number_of_neighbours = len(plane.get_neighbours_ids(empty_space))

        remaining_nodes = remaining_nodes[1:]

    return inserted_nodes

def _choose_empty_location_with_neighbour(plane, empty_locations):
    location_with_smallest_number_of_neighbours = []
    n_neighbours = 1

    while True:
        for empty_location in empty_locations:
            if len(plane.get_neighbours_ids(empty_location)) == n_neighbours:
                location_with_smallest_number_of_neighbours.append(empty_location)

        if location_with_smallest_number_of_neighbours:
            break

        if n_neighbours >= 9:
            return plane.get_random_empty_location()

        else:
            n_neighbours += 1

    return random.choice(location_with_smallest_number_of_neighbours)
