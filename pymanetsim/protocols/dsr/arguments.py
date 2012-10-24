class DsrProtocolArguments(object):
    """
    This class represents the protocol parameters specific for DSR protocol
    """

    def __init__(self, arguments):
        if not arguments: arguments = {}
        self.fill_property(arguments, 'start_time', 1)
        self.fill_property(arguments, 'time_interval', 1)
        self.fill_property(arguments, 'number_of_routes_to_find', 1)
        self.fill_property(arguments, 'origin_ids', [])
        self.fill_property(arguments, 'destiny_ids', [])

    def fill_property(self, arguments, name, default):
        if arguments.has_key(name):
            value = arguments[name]

        else:
            value = default

        setattr(self, name, value)
