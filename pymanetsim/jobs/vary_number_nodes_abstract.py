import plane_builders

plane_parameters = {
    'x_size':100,
    'y_size':100,
    'min_degree':6,
    'max_degree':6,
    'plane_builder_method':plane_builders.square_builder
}

protocol_parameters = {
    'start_time':1,
    'time_interval':10,
    'number_of_routes_to_find':49,
    'origin_ids':[str(id) for id in range(1, 400)],
    'destiny_ids':['500']
}

node_parameters = {
}

config_parameters = {
    'max_cycles':2000,
    'events':{},
}

x_variable_field = "plane_p.number_of_nodes"
x_variable_name = "number_of_nodes"
x_variable_values = xrange(500, 3000, 300)
