import pdb
from abstract_node import Node
from messages import BroadcastMessage
from events import AsynchronousEvent, RouteFoundEvent

import bloom

from configuration import DEBUG, FAST
import random

CONST_B = 400
CONST_N_HASHES = 3
CONST_CARD_P = 5
CONST_CARD_T = 2
CONST_HELLO_MESSAGE_INTERVAL = 30

# ------------ Node ------------>
class BfgNode(Node):
    """
    This class represents the Node for the bloom
    filter guided routing protocol
    """

    def __init__(self, node_id=None, location=None, node_parameters=None, protocol_manager=None):
        """
        Constructor.
        node_id - The node unique identifier
        location - The location of the node
        node_parameters - Extra parameters passed to the node
        protocol_manager - The protocol manager that manages all BfgNodes
        """
        Node.__init__(self, location=location, node_id=node_id, node_parameters=node_parameters)
        self.query_id = 0
        self.responded_queries = {}
        self.responded_dsr_queries = []
        self.asked_queries = []
        self.direct_neighbours_ids = []
        self.time_counter = 0
        self.protocol_manager = protocol_manager
        self.queries_completed = []
        self.heat_mem = [bloom.ErbBloomFilter(m=CONST_B, k=CONST_N_HASHES) for x in xrange(CONST_CARD_P)]
        self.tunnel_mem = [bloom.ErbBloomFilter(m=CONST_B, k=CONST_N_HASHES) for x in xrange(CONST_CARD_P)]

    def receive_hello_message(self, sender_id, structure_m):
        """
        The method called when a node receives an hello message
        """

        #Add the node that send as our neighbour
        self.direct_neighbours_ids.append(sender_id)
        self.heat_mem[0].add(sender_id)

        assert self._node_in_my_heat_mem(sender_id)

        #Spread the heat ;)
        bloom_layer = 1
        for bloom_in_m in structure_m:
            self.heat_mem[bloom_layer].merge(bloom_in_m)
            if DEBUG:
                if not FAST:
                    print self.heat_mem[bloom_layer].bits,
                    print self.heat_mem[bloom_layer].debug_symbols
            bloom_layer += 1

        return self._node_response(None)

    def create_hello_message(self):
        """
        Generates the hello message
        """
        hello_message = HelloMessage(sender=self, heat_mem=self.heat_mem)
        return hello_message

    def pass_time(self):
        """
        Passes a time cycle in the node

        In BFG it consists on making time passe in existing ERB filters and
        sending the node's hello messages
        """
        self.time_counter += 1
        response_msgs = []

        #Make the time pass in our heat_mems
        if ((self.time_counter -1) % (CONST_HELLO_MESSAGE_INTERVAL * 2)) == 0:
            for erp_bloom in self.heat_mem:
                erp_bloom.pass_time()

        if self.time_counter == 1 or self.time_counter % CONST_HELLO_MESSAGE_INTERVAL == 0:
            hello_message = self.create_hello_message()
            response_msgs = [hello_message]

        #If the BFG query wasn't sucesfull, launch the dsr query
        dsr_messages = self._launch_dsr_messages()

        return self._node_response(response_msgs + dsr_messages)

    def receive_dsr_type_message(self, query_id, origin_id, previous_node_id, destiny_id, route):
        if (query_id, origin_id) in self.responded_dsr_queries:
            return self._node_response(None)

        route = route[:]
        route.append(self.id)
        self.responded_dsr_queries.append((query_id, origin_id))

        if self.id == destiny_id:
            print "DSR reached: " + str(self.protocol_manager.test) + " " + str(self.time_counter)
            self.protocol_manager.test += 1

            next_node_id = route[route.index(self.id) - 1] #Choose the previous node
            go_back_message = GoBackMessage(origin_id=origin_id,
                                            sender=self,
                                            destiny_id=destiny_id,
                                            query_id=query_id,
                                            next_node_id=next_node_id,
                                            route=route)
            return self._node_response([go_back_message])

        #If i am not the destiny continue the dsr
        else:
            dsr_message = DsrTypeMessage(origin_id, self, destiny_id, query_id, route=route)
            return self._node_response([dsr_message])

    def start_looking_for_target(self, origin_id, destiny_id, random_walk_multiply, random_walk_max_hop, random_walk_time_to_give_up):
        """
        Start looking for target destiny

        destiny -- The target node to look for
        """
        assert origin_id == self.id

        self.query_id += 1
        self.asked_queries.append((self.query_id, destiny_id, random_walk_time_to_give_up  * 3 + self.time_counter))

        if not self.direct_neighbours_ids:
            return self._node_response(None)

        route = [self.id]

        query_messages = []
        for i in xrange(random_walk_multiply):
            next_node_id = self._choose_next_node_id(route)
            query_messages.append(RandomWalkMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id,
                                                      query_id=self.query_id, next_node_id=next_node_id, route=route,
                                                      random_walk_max_hop=random_walk_max_hop))

        return self._node_response(messages=query_messages)

    def _choose_next_node_id(self, route):
        random_shuffled_direct_neighbours_ids = self.direct_neighbours_ids[:]
        random.shuffle(random_shuffled_direct_neighbours_ids)

        for next_node_id in random_shuffled_direct_neighbours_ids:
            if not next_node_id in route:
                return next_node_id
        next_node_id = random.choice(self.direct_neighbours_ids)
        return next_node_id

    def receive_random_walk_message(self, origin_id, query_id, destiny_id, next_node_id, route, random_walk_max_hop):
        assert origin_id == route[0]

        if not next_node_id == self.id: #The message wasn't for me
            return self._node_response(None)

        if random_walk_max_hop <= len(route): #The max hop has been reached :(
            return self._node_response(None)

        route = route[:]
        route.append(self.id) #TODO - In the future maybe I can do more intelligent things here

        if self.id == destiny_id:
            messages_and_events = self._reached_destiny_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        #If the destiny is in my heat mem
        elif self._node_in_my_heat_mem(destiny_id):
            messages_and_events = self._reached_heat_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        #If it is on my tunnel mem
        if self._node_in_my_tunnel_mem(destiny_id):
            messages_and_events = self._reached_tunnel_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        #This is to respond to the case where I still don't know any neighbour
        elif not self.direct_neighbours_ids:
            return self._node_response(None)

        #Let's continue with the random walk
        else:
            messages_and_events = self._reached_random_walk_state(query_id, origin_id, destiny_id, route, random_walk_max_hop)
            return messages_and_events

    def receive_go_back_route(self, query_id, origin_id, destiny_id, sender_id, route, next_node_id):
        """
        Receives the go back message started after the destination is found
        """
        assert origin_id == route[0]

        #Check if the message is for me
        if not self.id == next_node_id:
            return self._node_response(None)

        #Check if I am who requested the route
        elif self.id == origin_id:

            #Check if I already got the anwser for this query
            if query_id in self.queries_completed:
                return self._node_response(None)
            else: #Now I have
                self.queries_completed.append(query_id)

            self.asked_queries = [] #TODO WRONG

            #Added the destiny to my tunnel map
            self.tunnel_mem[0].add(destiny_id) #TODO - Changing to tunnels

            #Statistical purposes
            self.protocol_manager.have_origin[self.id] = True

            #Inform the simulator of "EUREKA: I found it"
            simulator_event = RouteFoundEvent(origin_id=origin_id, destiny_id=destiny_id, route=route)
            return self._node_response(simulator=[simulator_event])

        #If i am simply a node in the go back route
        elif self.id in route:
            next_node_id = route[route.index(self.id) - 1] #Choose the previous node

            #Some small tests to see if efverything is OK
            assert next_node_id.count
            assert route.index(self) - 1 >= 0

            #Added the destiny to my heat map
            self.tunnel_mem[0].add(destiny_id) #TODO - Changing to tunnels

            #Send the message to the previous node in the  route
            go_back_message = GoBackMessage(origin_id=origin_id,
                                            sender=self,
                                            destiny_id=destiny_id,
                                            query_id=query_id,
                                            next_node_id=next_node_id,
                                            route=route)
            return self._node_response(messages=[go_back_message])

        #Should not get here
        else: assert False

    def receive_follow_tunnel_message(self, origin_id, previous_node_id, destiny_id, query_id, route):
        assert origin_id == route[0]

        #In here don't forget to see queries responded
        if (origin_id, query_id) in self.responded_queries:
            return self._node_response(None)

        route = route[:]
        route.append(self.id)

        if self.id == destiny_id:
            messages_and_events = self._reached_destiny_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        #If the destiny is in my heat mem
        elif self._node_in_my_heat_mem(destiny_id):
            messages_and_events = self._reached_heat_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        #If it is on my tunnel mem
        if self._node_in_my_tunnel_mem(destiny_id):
            messages_and_events = self._reached_tunnel_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        #I do not belong to the tunnel
        else:
            return self._node_response(None)

    def receive_follow_heat_message(self, origin_id, previous_node_id, destiny_id, query_id, route):
        #In here don't forget to see queries responded
        if (origin_id, query_id) in self.responded_queries:
            return self._node_response(None)

        route = route[:]
        route.append(self.id)

        if self.id == destiny_id:
            #Hurray the destiny was found"
            messages_and_events = self._reached_destiny_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

        elif not self._node_in_my_heat_mem(destiny_id):
            return self._node_response(None)

        #If I have the destiny in my heat_mem
        else:
            messages_and_events = self._reached_heat_state(query_id, origin_id, destiny_id, route)
            return messages_and_events

    def _node_in_my_heat_mem(self, node_id):
        """
        Checks if a node in the heat_mem
        """
        layer = self._node_in_what_level_of_mem(node_id, self.heat_mem)
        return layer != -1

    def _node_in_my_tunnel_mem(self, node_id):
        """
        Checks if a node in the heat_mem
        """
        layer = self._node_in_what_level_of_mem(node_id, self.tunnel_mem)
        return layer != -1

    def _node_in_what_level_of_mem(self, node_id, mem_structure):
        """
        Checks if a node in a memory

        Returns the level of the heat_mem
        """
        i = 0
        for i in xrange(0, len(mem_structure)) :
            if node_id in mem_structure[i]:
                return i
        return -1

    def _launch_dsr_messages(self):

        #Discover what queries are missing
        missing_queries = [(query_id, target) for query_id, target, time in self.asked_queries if time == self.time_counter ]

        #For each one of the target ids create a dsr type message -- TODO the query id is wrong
        messages = []

        for query_id, target_id in missing_queries:
            dsr_message = DsrTypeMessage(self.id, self, target_id, query_id, [self.id])
            messages.append(dsr_message)

        return messages

    def _node_response(self, messages=None, asynchronous=None, simulator=None, rec=[]):
        messages = messages or []
        asynchronous = asynchronous or []
        simulator = simulator or []

        for message in messages:
            self.protocol_manager.total_messages_sent += 1

            if isinstance(message, FollowHeatMessage):
                self.protocol_manager.total_follow_heat += 1
            if isinstance(message, RandomWalkMessage):
                self.protocol_manager.total_random_walk += 1
            if isinstance(message, GoBackMessage):
                self.protocol_manager.total_go_back += 1
            if isinstance(message, HelloMessage):
                self.protocol_manager.total_hello += 1
            if isinstance(message, DsrTypeMessage):
                self.protocol_manager.total_dsr += 1

        for sim_event in simulator:
            if isinstance(sim_event, RouteFoundEvent):
                self.protocol_manager.routes_found += 1

        return {'messages':messages, 'asynchronous':asynchronous, 'simulator':simulator}

    def _reached_destiny_state(self, query_id, origin_id, destiny_id, route):
        next_node_id = route[route.index(self) - 1] #Choose the previous node
        self.responded_queries[(origin_id, query_id)] = True # TODO #If i uncomment this I only get a return go back route

        self.protocol_manager.have_destiny[origin_id] = True
        go_back_message = GoBackMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id, query_id=query_id, next_node_id=next_node_id, route=route)
        return self._node_response(messages=[go_back_message])

    def _reached_heat_state(self, query_id, origin_id, destiny_id, route):
        self.responded_queries[(origin_id, query_id)] = True
        self.protocol_manager.have_heat[origin_id] = True
        follow_heat_message = FollowHeatMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id, query_id=query_id, route=route)
        return self._node_response(messages=[follow_heat_message])

    def _reached_tunnel_state(self, query_id, origin_id, destiny_id, route):
        self.responded_queries[(origin_id, query_id)] = True
        follow_tunnel_message = FollowTunnelMessage(origin_id=origin_id,
                                                sender=self,
                                                destiny_id=destiny_id,
                                                query_id=query_id,
                                                route=route)
        return self._node_response(messages=[follow_tunnel_message])

    def _reached_random_walk_state(self, query_id, origin_id, destiny_id, route, random_walk_max_hop):
        next_node_id = self._choose_next_node_id(route)
        random_walk = RandomWalkMessage(origin_id=origin_id, sender=self, destiny_id=destiny_id,
                                        query_id=query_id, next_node_id=next_node_id, route=route,
                                        random_walk_max_hop=random_walk_max_hop)
        return self._node_response(messages=[random_walk])

# <------------ Node ------------


# ------------ Events and Messages ------------>
class HelloMessage(BroadcastMessage):
    """
    This class represents the Hello messages that are exchanged in the network
    """
    hello_message_count = 0

    def __init__(self, sender, heat_mem):
        """
        Constructor.
        """
        structure_m = [erp_bloom for erp_bloom in heat_mem[:-1]]
        self.sender_id = sender.id

        arguments = {'structure_m':structure_m, 'sender_id':sender.id}
        BroadcastMessage.__init__(self, sender=sender,
                                  emit_location=sender.location,
                                  function_to_call=BfgNode.receive_hello_message,
                                  arguments=arguments)

    def __str__(self):
        return ("Message from %s with P: %s" % (self.sender_id, self.arguments['structure_m']))

class LookForDestination(AsynchronousEvent):
    def __init__(self, origin_id, destiny_id, random_walk_multiply=1, random_walk_max_hop=100, random_walk_time_to_give_up=100+20):
        arguments = {'origin_id':origin_id, 'destiny_id':destiny_id, 'random_walk_multiply':random_walk_multiply, 'random_walk_max_hop':random_walk_max_hop, 'random_walk_time_to_give_up':random_walk_time_to_give_up}
        AsynchronousEvent.__init__(self, node_id=origin_id, function_to_call=BfgNode.start_looking_for_target, arguments=arguments)

class RandomWalkMessage(BroadcastMessage):
    def __init__(self, origin_id, sender, destiny_id, query_id, next_node_id, route, random_walk_max_hop):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'destiny_id':destiny_id, 'next_node_id':next_node_id, 'route':route, 'random_walk_max_hop':random_walk_max_hop}

        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=BfgNode.receive_random_walk_message, arguments=arguments)

class GoBackMessage(BroadcastMessage):
    go_back_message_count = 0

    def __init__(self, origin_id, sender, destiny_id, query_id, next_node_id, route):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'sender_id':sender.id, 'destiny_id':destiny_id, 'next_node_id':next_node_id, 'route':route}
        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=BfgNode.receive_go_back_route, arguments=arguments)

class FollowHeatMessage(BroadcastMessage):
    follow_heat_message_count = 0

    def __init__(self, origin_id, sender, destiny_id, query_id, route):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'previous_node_id':sender.id, 'destiny_id':destiny_id, 'route':route}
        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=BfgNode.receive_follow_heat_message, arguments=arguments)

class FollowTunnelMessage(BroadcastMessage):
    follow_tunnel_message_count = 0

    def __init__(self, origin_id, sender, destiny_id, query_id, route):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'previous_node_id':sender.id, 'destiny_id':destiny_id, 'route':route}
        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=BfgNode.receive_follow_tunnel_message, arguments=arguments)

class DsrTypeMessage(BroadcastMessage):
    follow_heat_message_count = 0

    def __init__(self, origin_id, sender, destiny_id, query_id, route):
        arguments = {'query_id':query_id, 'origin_id':origin_id, 'previous_node_id':sender.id, 'destiny_id':destiny_id, 'route':route}
        BroadcastMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=BfgNode.receive_dsr_type_message, arguments=arguments)
# <------------ Events and Messages ------------
