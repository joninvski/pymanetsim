import plane_builders
import random

plane_parameters = {
    'x_size':50,
    'y_size':50,
    'min_degree':5,
    'max_degree':8,
    'number_of_nodes':1000,
    'plane_builder_method':plane_builders.degree_plane_builder,
}

a = [str(id) for id in range(1,50)]
random.shuffle(a)

protocol_parameters = {
    'start_time':50,
    'time_interval':100,
    'number_of_routes_to_find':50,
    'origin_ids':a,
    'destiny_ids':['80']
}

node_parameters = {
}

config_parameters = {
    'max_cycles':13000,
    'events':{},
}

x_variable_field = "plane_p['number_of_nodes']"
x_variable_name = "number_of_nodes"
x_variable_values = range(200, 2501, 500)
