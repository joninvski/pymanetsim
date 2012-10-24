from abstract_node import Node
from messages import DirectMessage
from events import AsynchronousEvent

class SimpleNode(Node):

    def __init__(self, node_id=None, location=None, node_parameters=None, protocol_manager=None):
        """
        Constructor.
        node_id - The node unique identifier
        location - The location of the node
        node_parameters - Extra parameters passed to the node
        protocol_manager - The protocol manager that manages all DsrNodes
        """
        Node.__init__(self, location=location, node_id=node_id, node_parameters=node_parameters)
        self.protocol_manager = protocol_manager
        self.time_counter = 0

    def pass_time(self):
        self.time_counter += 1
        return {'messages':[], 'asynchronous':[], 'simulator':[]}

    def receive_simple_message(self, text):
        print "I have received the text:", text
        return {'messages':[], 'asynchronous':[], 'simulator':[]}

    def handle_send_msg_event(self, destiny_id):
        text="Hello. I am " + self.id + " and my time is " + str(self.time_counter)
        simple_message = SimpleMessage(sender=self, destiny_id=destiny_id, text=text)
        return {'messages':[simple_message], 'asynchronous':[], 'simulator':[]}

class SimpleMessage(DirectMessage):
    def __init__(self, sender, destiny_id, text):
        arguments = {'text':text}
        DirectMessage.__init__(self, sender=sender, emit_location=sender.location, destination_list=[destiny_id], \
                               function_to_call=SimpleNode.receive_simple_message, arguments=arguments)

class SendSimpleMsgEvent(AsynchronousEvent):
    def __init__(self, origin_id, destiny_id):
        arguments = {'destiny_id':destiny_id}
        AsynchronousEvent.__init__(self, node_id=origin_id, function_to_call=SimpleNode.handle_send_msg_event, arguments=arguments)

class SimpleManager(object):
    def __init__(self, protocol_arguments=None):
        pass

    def manage(self, time, all_nodes, event_broker, message_broker):
        pass
