import events

from messages import BroadcastMessage
from events import AsynchronousEvent, RouteFoundEvent

from abstract_node import Node

# ------------ Node ------------>
class DsrNode(Node):
    """
    Class that mimics the DSR routing algorithm
    """

    def __init__(self, node_id=None, location=None, node_parameters=None, protocol_manager=None):
        """
        Constructor.
        node_id - The node unique identifier
        location - The location of the node
        node_parameters - Extra parameters passed to the node
        protocol_manager - The protocol manager that manages all DsrNodes
        """
        Node.__init__(self, location=location, node_id=node_id, node_parameters=node_parameters)
        self.responded_queries = {}
        self.protocol_manager = protocol_manager
        self.my_query_id = 0

    def run_node_forward(self, query_id, origin_id, destiny_id, previous_node):
        """
        Runs the algorithm while it is trying to find the destiny
        """
        # Check if I have already responded to this query
        if (origin_id, query_id) in self.responded_queries:
            return self._node_response(None)
        else:
            self.responded_queries[(origin_id, query_id)] = previous_node

        #If I am the destination
        if self.id == destiny_id:
            #Launch the go backward part of the algorithm
            next_node = self.responded_queries[(origin_id, query_id)]
            go_back_message = GoBackwardMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id, query_id=query_id, next_node=next_node, route=[self])

            return self._node_response(messages=[go_back_message])

        #I am still not the destination, continue to broadcast the message
        query_message = SearchTargetMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id, query_id=query_id)
        return self._node_response(messages=[query_message])

    def run_node_backward(self, query_id, origin_id, previous_node, destiny_id, next_node, route):
        """
        Runs the algorithm after it found the destiny and is going backward
        """
        if not next_node == self:
            return self._node_response(None)

        else: #If the message is for me
            #Add me to the route
            route.append(self)

            #If am the origin, then I got to the end
            if self.id == origin_id:
                simulator_event = events.RouteFoundEvent(origin_id=origin_id, destiny_id=destiny_id, route=route)
                return self._node_response(simulator=[simulator_event])

            #If I am not the origin, then the next node is the previous in the responded_queries
            if (origin_id, query_id) in next_node.responded_queries:
                next_node = next_node.responded_queries[(origin_id, query_id)]

            else: #Somehow the path to go back isn't complete
                raise Exception("Something has happenend. I don't have anyone prior to me")

            go_back_message = GoBackwardMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id, query_id=query_id, next_node=next_node, route=route)
            return self._node_response(messages=[go_back_message])

    def start_looking_for_target(self, origin_id, destiny_id):
        assert self.id == origin_id
        self.my_query_id += 1
        self.responded_queries[(origin_id, self.my_query_id)] = None
        query_message = SearchTargetMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id, query_id=self.my_query_id)

        return self._node_response(messages=[query_message])

    def _node_response(self, messages=None, asynchronous=None, simulator=None):
        messages = messages or []
        asynchronous = asynchronous or []
        simulator = simulator or []

        for message in messages:
            self.protocol_manager.total_messages_sent += 1

            if isinstance(message, SearchTargetMessage):
                self.protocol_manager.total_search_messages += 1
            if isinstance(message, GoBackwardMessage):
                self.protocol_manager.total_go_back_message += 1

        for sim_event in simulator:
            if isinstance(sim_event, RouteFoundEvent):
                self.protocol_manager.routes_found += 1

        return {'messages':messages, 'asynchronous':asynchronous, 'simulator':simulator}
# <------------ Node ------------


# ------------ Events and Messages ------------>
class SearchTargetMessage(BroadcastMessage):
    def __init__(self, origin_id, sender, destiny_id, query_id):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'previous_node':sender, 'destiny_id':destiny_id}
        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=DsrNode.run_node_forward, arguments=arguments)

class GoBackwardMessage(BroadcastMessage):
    def __init__(self, origin_id, sender, destiny_id, query_id, next_node, route):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'previous_node':sender, 'destiny_id':destiny_id, 'next_node':next_node, 'route':route}
        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=DsrNode.run_node_backward, arguments=arguments)

class LookForDestination(AsynchronousEvent):
    def __init__(self, origin_id, destiny_id):
        arguments = {'origin_id':origin_id, 'destiny_id':destiny_id}
        AsynchronousEvent.__init__(self, node_id=origin_id, function_to_call=DsrNode.start_looking_for_target, arguments=arguments)
# <------------ Events and Messages ------------
