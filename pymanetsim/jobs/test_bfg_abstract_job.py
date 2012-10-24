import plane_builders
import random

plane_parameters = {
    'x_size':300,
    'y_size':300,
    'min_degree':1,
    'max_degree':8,
    'number_of_nodes':0,
    'plane_builder_method':plane_builders.square_builder,
}

protocol_parameters = {
    'start_time':1,
    'time_interval':1,
    'number_of_routes_to_find':5,
    'origin_ids':['1','2','3'],
    'destiny_ids':['50']
}

node_parameters = {
}

config_parameters = {
    'max_cycles':3000,
    'events':{},
}

x_variable_field = "plane_p.number_of_nodes"
x_variable_name = "number_of_nodes"
x_variable_values = range(100, 200, 20)
