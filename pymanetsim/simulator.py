from plane import Plane
from abstract_node import Node

from events import EventBroker
from messages import MessageBroker

from configuration import DEBUG

from UserDict import UserDict

class Simulation(object):
    """
    This class represents a simulation
    """

    def __init__(self, simulation_parameters):
        """
        Constructor.

        simulation_parameters - The parameters to be used to run this simulation
        """
        self.type_of_nodes = simulation_parameters.config_p['type_of_nodes']
        self._max_cycles = simulation_parameters.config_p['max_cycles']

        self.number_messages_out = 0
        self.number_messages_in = 0

        self.number_asynchronous_events = 0
        self.number_simulation_events = 0

        self.all_nodes = {}
        self.time = 0

        self.protocol_manager = \
                simulation_parameters.config_p['protocol_manager'](protocol_arguments=simulation_parameters.protocol_p)

        self.event_broker = EventBroker()
        self.message_broker = MessageBroker()

        node_parameters = simulation_parameters.node_p
        type_of_nodes = simulation_parameters.config_p['type_of_nodes']
        events_to_launch = simulation_parameters.config_p['events']

        # If the simulator is generating the plane
        if not 'scenario_file' in simulation_parameters.plane_p:
            generated_nodes = Node.generate_nodes(number_to_generate=simulation_parameters.plane_p['number_of_nodes'], \
                                                  type_of_nodes=type_of_nodes, node_parameters=node_parameters, \
                                                  protocol_manager=self.protocol_manager)
            for node in generated_nodes:
                self.all_nodes[node.id] = node
            self.plane = Plane.generate_plane(all_nodes=self.all_nodes, plane_parameters=simulation_parameters.plane_p)

        # If the simulator is loading the plane from a file
        else:
            (self.all_nodes, self.plane) = Plane.load_plane(plane_parameters=simulation_parameters.plane_p, \
                                                            node_parameters=simulation_parameters.node_p, \
                                                            type_of_nodes=self.type_of_nodes, \
                                                            protocol_manager=self.protocol_manager)
        #Now putt the events to launch in the event broker
        for event in events_to_launch:
            self.event_broker.add_asynchronous_event(event)

    def __str__(self):
        """
        Returns the string representation of a simulation
        """
        return "Time: %d of %d" % (self.time, self._max_cycles)

    def run(self, cycles_to_run=None):
        """
        Runs the simulation for a number of cycles.

        If the number of cycles isn't specified in the arguments,
        the simulation is run until the defined max_cycles.
        """
        cycles_to_run = cycles_to_run or (self._max_cycles - self.time)

        for i in xrange(cycles_to_run):
            self.time += 1
            self.run_cycle()
            if DEBUG and self.time % 100 == 0:
                print self.time, '\t',

    def run_cycle(self):
        """
        Runs a single cycle in the simulated network
        """
        self.protocol_manager.manage(self.time, all_nodes=self.all_nodes, \
                                     event_broker=self.event_broker, \
                                     message_broker=self.message_broker, plane=self.plane)

        new_events_and_messages_a = self.run_asynchronous_events()
        new_events_and_messages_b = self.run_message_delivery()
        new_events_and_messages_c = self.run_node_time()

        self._add_events_and_messages((new_events_and_messages_a, new_events_and_messages_b, new_events_and_messages_c))

    def _add_events_and_messages(self, list_of_new_events_and_messages):
        """
        Adds the messages and events to the lists which contain all the messages
        and events that will be used in future cycles
        """
        for new_events_and_messages in list_of_new_events_and_messages:
            for message in new_events_and_messages['messages']:
                self.message_broker.add_to_be_transmitted(message)
                self.number_messages_out += 1

            for asynchronous_event in new_events_and_messages['asynchronous']:
                self.event_broker.add_asynchronous_event(asynchronous_event)
                self.number_asynchronous_events += 1

            for simulator_event in new_events_and_messages['simulator']:
                self.event_broker.add_simulator_event(simulator_event)
                self.number_simulation_events += 1

    def _merge_events_and_messages(self, next_cycle_events_and_messages, new_events_and_messages):
        """
        Merges the messages and events present in the dictionary new_events_and_messages with passed
        dictionary of next_cycle_events_and_messages.

        Returns the next_cycle_events_and_messages with the merged values
        """

        next_cycle_events_and_messages['messages'] += new_events_and_messages['messages']
        next_cycle_events_and_messages['simulator'] += new_events_and_messages['simulator']
        next_cycle_events_and_messages['asynchronous'] += new_events_and_messages['asynchronous']

        return next_cycle_events_and_messages

    def run_asynchronous_events(self):
        """
        Runs all the asynchronous events present in the event broker
        """
        next_cycle_events_and_messages = {'messages': [], 'asynchronous': [], 'simulator': []}

        while not self.event_broker.is_asynchronous_events_empty():
            event_to_run = self.event_broker.get_asynchronous_event()
            new_events_and_messages = event_to_run.run(self.all_nodes)
            next_cycle_events_and_messages = self._merge_events_and_messages(next_cycle_events_and_messages, new_events_and_messages)

        return next_cycle_events_and_messages

    def run_message_delivery(self):
        """
        Delivers all the messages present in the message broker
        """
        next_cycle_events_and_messages = {'messages': [], 'asynchronous': [], 'simulator': []}

        while not self.message_broker.still_msgs_to_be_transmitted():
            new_events_and_messages = self.message_broker.get_message_to_be_transmitted().run(self.plane, self.all_nodes)
            next_cycle_events_and_messages = self._merge_events_and_messages(next_cycle_events_and_messages, new_events_and_messages)

        return next_cycle_events_and_messages

    def run_node_time(self):
        """
        Informs the nodes that a cycle has passed
        """
        next_cycle_events_and_messages = {'messages': [], 'asynchronous': [], 'simulator': []}

        for node_id in self.all_nodes:
            new_events_and_messages = self.all_nodes[node_id].pass_time()
            next_cycle_events_and_messages = self._merge_events_and_messages(next_cycle_events_and_messages, new_events_and_messages)

        return next_cycle_events_and_messages

    def end_simulation(self):
        end_sim_func = getattr(self.protocol_manager, "end_simulation", None)

        if callable(end_sim_func):
            self.protocol_manager.end_simulation(self.all_nodes, self.plane)


class NodeParameters(UserDict):
    """
    This class represents the node parameters that can change

    These arguments are passed when a new node is build
    """
    pass

class ConfigurationParameters(UserDict):
    """
    This class represents the simulation parameters that can change

    Constructor.

        max_cycles -- The maximum number of cycles the simulation will run
        events -- The events which are present when the simulation starts (TODO - Deprecate future???)
        type_of_nodes -- The type of nodes to be used for the simulation (TODO - Pass to the protocol parameters in the future???)
        protocol_manager -- The protocol manager to be used for this simulation
    """
    def __str__(self):
        return "max_cycles: %s " % (str(self['max_cycles'])) + \
               ", events: %s " % (self['events']) + \
               ", type_of_nodes: %s " % (self['type_of_nodes']) + \
               ", protocol_manager: %s " % (str(self['protocol_manager']))

class ProtocolParameters(UserDict):
    """
    This class represents the parameters than can be changed in a protocol
    """
    pass

class PlaneParameters(UserDict):
    """
    This class represents the plane parameters than can changed

    Constructor. for the plane parameters

        x_size = The horizontal length of the plane
        y_size = The vertical length of the plane
        plane_builder_method = The method to call to build a plane
        min_degree = The minimum degree of neighbours each node in the plane should have
        max_degree = The maximum degree of neighbours each node in the plane should have

        scenario_file = The path for the map file (used mainly for test purposes)
    """
    def __str__(self):
        return "x_size: %d, y_size:%d, " % (self['x_size'], self['y_size']) + \
               "min_degree: %d, max_degree: %d, " % (self['min_degree'], self['max_degree']) + \
               "number_of_nodes: %d" % (self['number_of_nodes'])

class SimulationParameters(object):
    """
    This class represents group of parameters that can change in a simulation
    """

    def __init__(self, config_parameters, node_parameters = None, protocol_parameters = None, plane_parameters= None):
        """
        Constructor.

        node_parameters -- The parameters that can change the node class
        protocol_parameters -- The parameters that can change the protocol class
        plane_parameters -- The parameters that can change the plane construction
        """
        self.config_p = config_parameters

        self.node_p = node_parameters or NodeParameters()
        self.protocol_p = protocol_parameters or ProtocolParameters()
        self.plane_p = plane_parameters or PlaneParameters()

    def __str__(self):
        return """Simulation Parameters

            Node Parameters:
                %s

            Protocol Parameters:
                %s

            Plane Parameters:
                %s

            Config Parameters:
                %s
                """ % (self.node_p, self.protocol_p, self.plane_p, self.config_p)
