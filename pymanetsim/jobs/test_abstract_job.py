import plane_builders
import random

plane_parameters = {
    'x_size':40,
    'y_size':40,
    'min_degree':2,
    'max_degree':7,
    'number_of_nodes':0,
    'plane_builder_method':plane_builders.degree_plane_builder,
}

protocol_parameters = {
    'start_time':50,
    'time_interval':1,
    'number_of_routes_to_find':100,
    'origin_ids':[str(id) for id in range(1,101)],
    'destiny_ids':['360']
}

node_parameters = {
}

config_parameters = {
    'max_cycles':500,
    'events':{},
}

x_variable_field = "plane_p.number_of_nodes"
x_variable_name = "number_of_nodes"
x_variable_values = range(800, 1000, 100)
