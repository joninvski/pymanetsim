import plane_builders
import random

plane_parameters = {
    'x_size':50,
    'y_size':50,
    'min_degree':5,
    'max_degree':8,
    'number_of_nodes':1200,
    'plane_builder_method':plane_builders.degree_plane_builder,
}

origins = [str(id) for id in range(1, 500)]
random.shuffle(origins)

protocol_parameters = {
    'start_time':50,
    'time_interval':100,
    'number_of_routes_to_find':-1,
    'origin_ids':origins,
    'destiny_ids':['1000']
}

node_parameters = {
}

config_parameters = {
    'max_cycles':13000,
    'events':{},
}

x_variable_field = "protocol_p['number_of_routes_to_find']"
x_variable_name = "routes_requests"
x_variable_values = [100, 200, 300, 400, 500]
