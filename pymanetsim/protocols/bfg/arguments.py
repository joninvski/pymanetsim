class BfgProtocolArguments(object):
    """
    This class represents the protocol parameters specific for BFG protocol
    """

    def __init__(self, arguments):
        if not arguments: arguments = {}

        self.fill_property(arguments, 'random_walk_max_hop', 40)
        self.fill_property(arguments, 'random_walk_multiply', 1)
        self.fill_property(arguments, 'random_walk_time_to_give_up', 40 + 20)


        self.fill_property(arguments, 'start_time', 1)
        self.fill_property(arguments, 'time_interval', 1)
        self.fill_property(arguments, 'number_of_routes_to_find', 1)
        self.fill_property(arguments, 'origin_ids', [])
        self.fill_property(arguments, 'destiny_ids', [])

    def fill_property(self, arguments, name, default):
        if name in arguments:
            value = arguments[name]

        else:
            value = default

        setattr(self, name, value)
