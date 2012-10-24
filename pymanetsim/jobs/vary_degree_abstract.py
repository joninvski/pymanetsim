import plane_builders

plane_parameters = {
    'x_size':300,
    'y_size':300,
    'min_degree':-1,
    'max_degree':8,
    'number_of_nodes':300,
    'plane_builder_method':plane_builders.square_builder,
}

protocol_parameters = {
    'start_time':1,
    'time_interval':1,
    'number_of_routes_to_find':50,
    'origin_ids':[str(id) for id in range(1,51)],
    'destiny_ids':['80']
}

node_parameters = {
}

config_parameters = {
    'max_cycles':900,
    'events':{},
}

x_variable_field = "plane_p.min_degree"
x_variable_name = "min_degree"
x_variable_values = range(7, 9)
