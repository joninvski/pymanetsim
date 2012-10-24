import plane_builders

plane_parameters = {
    'x_size':100,
    'y_size':100,
    'min_degree':6,
    'max_degree':6,
    'number_of_nodes':300,
    'plane_builder_method':plane_builders.square_builder,
}

protocol_parameters = {
    'start_time':1,
    'time_interval':1,
    'number_of_routes_to_find':50,
    'origin_ids':[str(id) for id in range(1, 50)],
    'destiny_ids':['100'],
}

node_parameters = {
}

config_parameters = {
    'max_cycles':600,
    'events':{},
}
