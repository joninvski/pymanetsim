class MessageBroker(object):
    """
    This class represents broker for the messages of a simulation
    """

    def __init__(self, messages_to_be_transmitted = None):
        """
        Constructor.

        messages_to_be_transmitted -- The message that are to be transmitted
        """
        self.to_be_transmitted = messages_to_be_transmitted or []

    def add_to_be_transmitted(self, event):
        """Adds a message to be transmitted"""
        self.to_be_transmitted.append(event)

    def reset_messages_to_transmit(self):
        """Resets (clears) the messages to be transmitted"""
        self.to_be_transmitted = []

    def get_message_to_be_transmitted(self):
        """Get a message to be transmitted"""
        if not self.to_be_transmitted:
            return None
        return self.to_be_transmitted.pop()

    def still_msgs_to_be_transmitted(self):
        """Ask if there are still messages to be transmitted"""
        return not self.to_be_transmitted

    def __str__(self):
        """Returns the string representation of the message broker"""
        return "Messages To be transmitted\n" + str(self.to_be_transmitted)

class Message(object):

    def __init__(self, sender, emit_location, function_to_call, arguments):
        """Constructor"""
        self.sender = sender
        self.emit_location = emit_location

        self.function_to_call = function_to_call
        self.arguments = arguments


class DirectMessage(Message):
    """Message with a specific node list destination"""

    def __init__(self, sender, emit_location, function_to_call, destination_list, arguments):
        """Constructor"""
        Message.__init__(self, sender=sender, emit_location=emit_location, function_to_call=function_to_call, \
                         arguments=arguments)

        self.destination_list = destination_list

    def run(self, plane, all_nodes):
        """Sends the message to the respective nodes which could hear it"""

        event_and_messages = {'messages': [], 'asynchronous': [], 'simulator': []}

        for node_id in self.destination_list:
            new_events_and_messages = self.function_to_call(all_nodes[node_id], **self.arguments)

            event_and_messages['messages'] += new_events_and_messages['messages']
            event_and_messages['simulator'] += new_events_and_messages['simulator']
            event_and_messages['asynchronous'] += new_events_and_messages['asynchronous']

        return event_and_messages


class BroadcastMessage(Message):
    """Message sent by a node which the neighbours for that node receive"""

    def __init__(self, sender, emit_location, function_to_call, arguments):
        """Constructor"""
        Message.__init__(self, sender=sender, emit_location=emit_location, function_to_call=function_to_call, arguments=arguments)

        #In the future, possibly include a power on the message signal
        self.power = sender.power

    def run(self, plane, all_nodes):
        """Sends the message to the respective nodes which could hear it"""
        power = self.sender.power

        #Get the nodes that heard the message
        node_ids_that_heard_message = plane.get_neighbours_ids_at_distance(self.emit_location, distance=power)

        event_and_messages = {'messages': [], 'asynchronous': [], 'simulator': []}

        #For each one of the neighbours
        for node_id in node_ids_that_heard_message:
            new_events_and_messages = self.function_to_call(all_nodes[node_id], **self.arguments)

            event_and_messages['messages'] += new_events_and_messages['messages']
            event_and_messages['simulator'] += new_events_and_messages['simulator']
            event_and_messages['asynchronous'] += new_events_and_messages['asynchronous']

        return event_and_messages
