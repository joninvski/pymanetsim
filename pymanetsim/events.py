class EventBroker(object):
    """
    This class represents the object which handles
    the events that happen in a simulation
    """

    def __init__(self, asynchronous_events=None, simulator_events=None):
        """
        Constructor.
        """
        self.asynchronous_events = asynchronous_events or []
        self.simulator_events = simulator_events or []

    def add_asynchronous_event(self, event):
        """Adds an asynchronous event to the event broker"""
        self.asynchronous_events.append(event)

    def add_simulator_event(self, event):
        """Adds an simulator event to the event broker"""
        self.simulator_events.append(event)

    def get_asynchronous_event(self):
        """Gets an asynchronous event from the event broker"""
        if not self.asynchronous_events:
            return None
        return self.asynchronous_events.pop()

    def get_simulator_event(self):
        """ Gets a simulator event from the event broker"""
        if not self.simulator_events:
            return None
        return self.simulator_events.pop()

    def is_asynchronous_events_empty(self):
        """ Ask if the event broker has more asynchronous events"""
        return not self.asynchronous_events

    def is_simulator_events_empty(self):
        """ Ask if the event broker has more simulator events"""
        return not self.simulator_events

    def reset_asynchronous_events(self):
        """
        Resets the asynchronous event list
        """
        self.asynchronous_events = []

    def reset_simulator_events(self):
        """
        Resets the simulator event list
        """
        self.simulator_events = []


class AsynchronousEvent(object):
    """Events launched by nodes that control the protocol status"""

    def __init__(self, node_id, function_to_call, arguments):
        """Constructor"""
        self.node_id = node_id
        self.function_to_call = function_to_call
        self.arguments = arguments

    def run(self, all_nodes):
        """Runs the asynchronous events"""
        node = all_nodes[self.node_id]
        return self.function_to_call(node, **self.arguments)


class SimulatorEvent(object):
    """Event launched by the protocol to control the state of the simulation"""

    def __init__(self, arguments):
        self.arguments = arguments


class RouteFoundEvent(SimulatorEvent): #TODO - This is not a Simulator event. Change in the future.
    """Event that says the protocol has found a route to the destination"""

    def __init__(self, origin_id, destiny_id, route):
        arguments = {'origin_id': origin_id, 'destiny_id': destiny_id, 'route': route}
        SimulatorEvent.__init__(self, arguments=arguments)
