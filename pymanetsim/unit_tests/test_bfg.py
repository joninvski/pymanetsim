import pdb
import unittest

from plane import Location, Plane
from protocols.bfg.node import BfgNode
from protocols.bfg.node import CONST_HELLO_MESSAGE_INTERVAL, CONST_CARD_P, LookForDestination, HelloMessage, GoBackMessage
from protocols.bfg.node import HelloMessage, GoBackMessage, FollowTunnelMessage, FollowHeatMessage
from protocols.bfg.bfg import BfgProtocolManager

from messages import MessageBroker
from events import RouteFoundEvent, EventBroker

from configuration import FAST

class TestBFG(unittest.TestCase):

    def setUp(self):
        self.location_a = Location(5, 3)
        self.location_b = Location(4, 3)
        self.location_c = Location(4, 2)
        self.location_d = Location(3, 2)

        self.message_broker = MessageBroker()

        self.protocol_manager = BfgProtocolManager()

    def test_bfg_node_creation(self):
        node_a = BfgNode(node_id="1", location=self.location_a)

        self.assert_(node_a.id)
        self.assertEquals(node_a.location, self.location_a)
        self.assertEquals(node_a.responded_queries, {})
        self.assertEquals(node_a.responded_queries, {})
        self.assert_(node_a.heat_mem)
        self.assertEqual(len(node_a.heat_mem), CONST_CARD_P)

    def test_create_simple_hello_messages(self):
        node_a = BfgNode(node_id="1", location=self.location_a)

        node_a.heat_mem[0].add('1000')

        hello_message = node_a.create_hello_message()

        self.assertEquals(hello_message.sender, node_a)
        self.assert_('1000' in hello_message.arguments['structure_m'][0])
        self.assertFalse('2' in hello_message.arguments['structure_m'][0])

        self.assertTrue(len(hello_message.arguments['structure_m']),  CONST_CARD_P - 1)

    def test_node_receive_hello_message(self):
        node_a = BfgNode(node_id="1", location=self.location_a)
        node_b = BfgNode(node_id="2", location=self.location_b)
        node_c = BfgNode(node_id="3", location=self.location_c)

        node_a.heat_mem[0].add('1000')
        node_a.heat_mem[2].add('2000')

        hello_message_a = node_a.create_hello_message()

        node_b.receive_hello_message(sender_id=node_a.id, structure_m=hello_message_a.arguments['structure_m'])

        self.assertTrue(node_a in node_b.direct_neighbours_ids)
        self.assertTrue(node_b not in node_b.direct_neighbours_ids)
        self.assertTrue(node_a.id in node_b.heat_mem[0])
        self.assertTrue('1000' in node_b.heat_mem[1])
        self.assertFalse('1000' in node_b.heat_mem[2])
        self.assertTrue('2000' in node_b.heat_mem[3])

        hello_message_b = node_b.create_hello_message()

        node_c.receive_hello_message(sender_id=node_b.id, structure_m=hello_message_b.arguments['structure_m'])

        self.assertTrue(node_a not in node_c.direct_neighbours_ids)
        self.assertTrue(node_b in node_c.direct_neighbours_ids)
        self.assertFalse(node_a.id in node_c.heat_mem[0])
        self.assertTrue(node_b.id in node_c.heat_mem[0])
        self.assertTrue(node_a.id in node_c.heat_mem[1])
        self.assertFalse('1000' in node_c.heat_mem[1])
        self.assertTrue('1000' in node_c.heat_mem[2])
        self.assertFalse('2000' in node_c.heat_mem[3])
        self.assertTrue('2000' in node_c.heat_mem[4])

        self.assertTrue('1000' in node_c.heat_mem[2])
        self.assertFalse('2000' in node_c.heat_mem[3])
        self.assertTrue('2000' in node_c.heat_mem[4])

    def test_bfg_node_pass_time(self):
        #It needs to generate hello messages
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_a.pass_time()

        new_messages = new_events_and_messages['messages']

        self.assertTrue(new_messages)
        self.assert_(isinstance(new_messages[0], HelloMessage))


        #And to pass time one the ERB filters
        node_c.heat_mem[0].add(node_b.id)
        self.assertTrue(node_b.id in node_c.heat_mem[0])

        for i in xrange(CONST_HELLO_MESSAGE_INTERVAL * 4):
            node_c.pass_time()
            self.message_broker.get_message_to_be_transmitted()

            if i < (CONST_HELLO_MESSAGE_INTERVAL * 2):
                self.assert_(node_b.id in node_c.heat_mem[0])
            if i >= (CONST_HELLO_MESSAGE_INTERVAL * 2):
                if not FAST: #This does not work if it is done FAST. Bloom filters have no memory loss
                    self.assertFalse(node_b.id in node_c.heat_mem[0])

    def test_found_heat_trail(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        node_a.heat_mem[3].add(node_c.id)
        node_a.heat_mem[4].add(node_c.id)

        node_b.heat_mem[2].add(node_c.id)
        node_b.heat_mem[3].add(node_c.id)
        node_b.heat_mem[4].add(node_c.id)

        new_events_and_messages = node_a.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_a.id, route=[node_a.id], random_walk_max_hop=30)

        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is BfgNode.receive_follow_heat_message.im_func)
        self.assertEquals(new_message[0].sender, node_a)
        self.assertEquals(new_message[0].emit_location, self.location_a)

        self.assert_(node_a.id in new_message[0].arguments['route'])


    def test_bfg_start_query_event(self):
        """
        Tests the creation of the new event and the reception of the event by a node
        """
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        node_a.direct_neighbours_ids.append(node_b)

        look_for_destination_event = LookForDestination(node_a.id, node_c.id)
        self.assert_(look_for_destination_event)

        self.assertEqual(look_for_destination_event.node_id, node_a.id)
        self.assertEqual(look_for_destination_event.arguments['destiny_id'], node_c.id)
        self.assertTrue(look_for_destination_event.function_to_call.im_func is BfgNode.start_looking_for_target.im_func)

        new_events_and_messages = look_for_destination_event.run({node_a.id:node_a, node_b.id:node_b, node_c.id:node_c})

        new_messages = new_events_and_messages['messages']

        self.assert_(new_messages)
        self.assertEqual(new_messages[0].arguments['origin_id'], node_a)
        self.assertEqual(new_messages[0].arguments['destiny_id'], node_c)
        self.assertEqual(new_messages[0].arguments['next_node_id'], node_b.id)
        self.assertEqual(new_messages[0].arguments['route'], [node_a])

    def test_bfg_node_receive_random_walk_and_retransmits(self):
        """
        Test in which a node receives a random walk
        """
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        node_b.direct_neighbours_ids.append(node_c)
        new_events_and_messages = node_b.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_b.id, route=[node_a.id], random_walk_max_hop=30)

        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is BfgNode.receive_random_walk_message.im_func)
        self.assertEquals(new_message[0].sender, node_b)
        self.assertEquals(new_message[0].emit_location, self.location_b)

        self.assertEquals(new_message[0].arguments['next_node_id'], node_c.id)
        self.assert_(node_b in new_message[0].arguments['route'])


    def test_bfg_node_receive_random_walk_and_NOT_retransmits(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        node_b.direct_neighbours_ids.append(node_c)
        new_events_and_messages = node_b.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_c.id, route=[node_a.id], random_walk_max_hop=30)

        self.assertFalse(new_events_and_messages['messages'])

    def test_bfg_node_receive_random_walk_and_is_destiny(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_c.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_c.id, route=[node_a.id, node_b.id], random_walk_max_hop=30)

        new_message = new_events_and_messages['messages']
        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is BfgNode.receive_go_back_route.im_func)
        self.assertEquals(new_message[0].sender, node_c)
        self.assertEquals(new_message[0].emit_location, self.location_c)

        self.assertEquals(new_message[0].arguments['next_node_id'], node_b.id)


    def test_bfg_node_receives_go_back_message_not_for_him(self):
        node_a = BfgNode(node_id="1", location=self.location_a)
        node_b = BfgNode(node_id="2", location=self.location_b)
        node_c = BfgNode(node_id="3", location=self.location_c)

        new_events_and_messages = node_b.receive_go_back_route(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, \
                                                               sender_id=node_b.id, next_node_id=node_c.id, route=[node_a.id, node_b.id])

        self.assertFalse(new_events_and_messages['messages'])

    def test_bfg_node_retransmits_go_back_message(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_b.receive_go_back_route(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, \
                                                               sender_id=node_c.id, next_node_id=node_b.id, route=[node_a.id, node_b.id, node_c.id])

        new_messages = new_events_and_messages['messages']

        self.assertTrue(new_messages)
        self.assertTrue(new_messages[0].function_to_call.im_func is BfgNode.receive_go_back_route.im_func)
        self.assertEquals(new_messages[0].sender, node_b)
        self.assertEquals(new_messages[0].emit_location, self.location_b)

        self.assertEquals(new_messages[0].arguments['next_node_id'], node_a.id)

    def test_bfg_node_go_back_message_reaches_origin(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_a.receive_go_back_route(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, sender_id=node_b.id, next_node_id=node_a.id, route=[node_a.id, node_b.id, node_c.id])
        self.assertFalse(new_events_and_messages['messages'])

        #And check that the simulator events that represents that the route was found is launched
        new_simulator_events = new_events_and_messages['simulator']

        self.assertTrue(new_simulator_events)
        self.assert_(isinstance(new_simulator_events[0], RouteFoundEvent))
        self.assertEqual(new_simulator_events[0].arguments['origin_id'], node_a.id)
        self.assertEqual(new_simulator_events[0].arguments['destiny_id'], node_c.id)
        self.assertEqual(new_simulator_events[0].arguments['route'], [node_a.id, node_b.id, node_c.id])

    def test_bfg_node_adds_id_to_tunnel_mem(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_b.receive_go_back_route(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, sender_id=node_b.id, next_node_id=node_b.id, route=[node_a.id, node_b.id, node_c.id])
        self.assertTrue(new_events_and_messages['messages'])
        self.assertTrue(isinstance(new_events_and_messages['messages'][0], GoBackMessage))

        self.assertTrue(node_b._node_in_my_tunnel_mem(node_c.id))
        self.assertEqual(node_b._node_in_what_level_of_mem(node_c.id, node_b.tunnel_mem), 0)
        self.assertFalse(node_b._node_in_my_heat_mem(node_c.id))

    def test_bfg_node_follows_tunnel_message(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)
        node_b.tunnel_mem[0].add(node_c.id)

        new_events_and_messages = node_b.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_b.id, route=[node_a.id, node_b.id, node_c.id], random_walk_max_hop=30)

        self.assertTrue(new_events_and_messages['messages'])
        self.assertTrue(isinstance(new_events_and_messages['messages'][0], FollowTunnelMessage))

        new_events_and_messages = node_a.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_a.id, route=[node_a.id, node_b.id, node_c.id], random_walk_max_hop=30)

        self.assertFalse(new_events_and_messages['messages'])

    def test_bfg_node_send_random_walk_having_not_received_any_hello_msg(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_a.receive_random_walk_message(query_id=10, origin_id=node_a.id, destiny_id=node_c.id, next_node_id=node_c.id, route=[node_a.id], random_walk_max_hop=30)
        self.assertFalse(new_events_and_messages['messages'])

    def test_bfg_node_send_multiple_random_walks(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        node_a.direct_neighbours_ids.append(node_b)
        node_a.direct_neighbours_ids.append(node_c)

        look_for_destination_event = LookForDestination(node_a.id, node_c.id, random_walk_multiply=2)
        new_events_and_messages = look_for_destination_event.run({node_a.id:node_a, node_b.id:node_b, node_c.id:node_c})

        self.assertEqual(len(new_events_and_messages['messages']), 2)

    def test_bfg_routes_to_find(self):
        bfg_protocol = BfgProtocolManager({'origin_ids':["1", "2"], 'destiny_ids':["3"], 'number_of_routes_to_find':4})

        message_broker = MessageBroker()
        event_broker = EventBroker()

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 1)

        bfg_protocol.manage(time=11, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 2)

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 3)

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 4)

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 4)

    def test_bfg_protocol_manager(self):
        bfg_protocol = BfgProtocolManager({'origin_ids':["1", "2"], 'destiny_ids':["3"], 'number_of_routes_to_find':2})

        message_broker = MessageBroker()
        event_broker = EventBroker()

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 1)

        event = event_broker.get_asynchronous_event()
        self.assertEqual(event.arguments['origin_id'], "1")
        self.assertEqual(event.arguments['destiny_id'], "3")

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 1)

        event = event_broker.get_asynchronous_event()
        self.assertEqual(event.arguments['origin_id'], "2")
        self.assertEqual(event.arguments['destiny_id'], "3")

        bfg_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 0)

    def test_bfg_draw_heat_map(self):
        all_nodes = {}
        # make all the nodes
        for i in xrange(50):
            node_a = BfgNode(node_id=str(i), protocol_manager=self.protocol_manager)
            all_nodes[str(i)] = node_a

        # make the plane
        import plane_builders
        from simulator import PlaneParameters
        plane_p = PlaneParameters(x_size = 10, y_size = 10, min_degree=1, max_degree=8, plane_builder_method=plane_builders.degree_plane_builder)
        plane = Plane.generate_plane(all_nodes=all_nodes, plane_parameters=plane_p)

        #make the protocol manager
        bfg_protocol = BfgProtocolManager({'origin_ids':["1", "2"], 'destiny_ids':["3"]})

        #Make heat spread
        #TODO

        #Draw the map
        bfg_protocol.draw_heat_map("Final Heat", all_nodes, plane, '3')

    def test_bfg_launch_dsr_type_messages(self):
        node_a = BfgNode(node_id="1", location=self.location_a)
        node_a.asked_queries = [('1', '3', 20), ('2', '3', 20), ('3', '3', 20), ('4', '3', 20), ('5', '3', 30)]
        node_a.time_counter = 20

        dsr_messages = node_a._launch_dsr_messages()

        self.assertEqual(len(dsr_messages), 4)

        self.assertEqual(dsr_messages[0].sender, node_a.id)
        self.assertEqual(dsr_messages[0].arguments['query_id'], ("1"))
        self.assertEqual(dsr_messages[1].arguments['query_id'], ("2"))
        self.assertEqual(dsr_messages[2].arguments['query_id'], ("3"))
        self.assertEqual(dsr_messages[2].arguments['destiny_id'], ("3"))

    def test_bfg_receive_dsr_type_messages(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        #Put the dsr message in a node
        new_events_and_messages = node_b.receive_dsr_type_message(("1", 1), node_a.id, node_a.id, node_c, [node_a.id])

        #It should leave another dsr message to continue to look for the destination
        self.assertTrue(new_events_and_messages['messages'])
        self.assertTrue((('1', 1), '1') in node_b.responded_dsr_queries)
        self.assertFalse((('1', 1), '2') in node_b.responded_dsr_queries)
        self.assertEqual(new_events_and_messages['messages'][0].arguments['route'], ['1','2'])

        #Put the dsr message again in the node
        new_events_and_messages = node_b.receive_dsr_type_message(("1", 1), node_a.id, node_a.id, node_c, [node_a.id])
        self.assertTrue((('1', 1), '1') in node_b.responded_dsr_queries)
        self.assertFalse((('1', 1), '2') in node_b.responded_dsr_queries)

        #It should not leave any other message
        self.assertFalse(new_events_and_messages['messages'])

    def test_bfg_dsr_type_message_reaches_end(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        #Put the dsr message in a node
        new_events_and_messages = node_c.receive_dsr_type_message(("1", 1), node_a.id, node_a.id, node_c, [node_a.id, node_b.id])

        self.assertTrue(new_events_and_messages['messages'])

        self.assertTrue(isinstance(new_events_and_messages['messages'][0], GoBackMessage))
        self.assertEqual(new_events_and_messages['messages'][0].arguments['next_node_id'], node_b)
        self.assertEqual(new_events_and_messages['messages'][0].arguments['route'], [node_a.id, node_b.id, node_c.id])

        #Now to check if it stays silent when the same message reaches it
        new_events_and_messages = node_c.receive_dsr_type_message(("1", 1), node_a.id, node_a.id, node_c, [node_a.id, node_b.id])
        self.assertFalse(new_events_and_messages['messages'])

    def test_bfg_receive_follow_tunnel_message(self):
        node_a = BfgNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = BfgNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = BfgNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)
        node_d = BfgNode(node_id="4", location=self.location_d, protocol_manager=self.protocol_manager)

        node_b.tunnel_mem[0].add(node_d)
        node_c.heat_mem[0].add(node_d)

        #Put the dsr message in a node
        new_events_and_messages = node_b.receive_follow_tunnel_message(node_a.id, node_a.id, node_d, ("1", 1), [node_a.id, node_b.id])
        self.assertTrue(new_events_and_messages['messages'])
        self.assertTrue(isinstance(new_events_and_messages['messages'][0], FollowTunnelMessage))

        #Now to check if it stays silent when the same message reaches it
        new_events_and_messages = node_b.receive_follow_tunnel_message(node_a.id, node_a.id, node_d, ("1", 1), [node_a.id, node_b.id])
        self.assertFalse(new_events_and_messages['messages'])

        #From the tunnel to the heat
        new_events_and_messages = node_c.receive_follow_tunnel_message(node_a.id, node_a.id, node_d, ("1", 1), [node_a.id, node_b.id])
        self.assertTrue(new_events_and_messages['messages'])
        self.assertTrue(isinstance(new_events_and_messages['messages'][0], FollowHeatMessage))

        #Now node d is the destiny
        new_events_and_messages = node_d.receive_follow_tunnel_message(node_a.id, node_a.id, node_d, ("1", 1), [node_a.id, node_b.id])
        self.assertTrue(new_events_and_messages['messages'])
        self.assertTrue(isinstance(new_events_and_messages['messages'][0], GoBackMessage))

        #Node a knows nothing
        new_events_and_messages = node_a.receive_follow_tunnel_message(node_a.id, node_a.id, node_d, ("1", 1), [node_a.id, node_b.id])
        self.assertFalse(new_events_and_messages['messages'])

if __name__ == '__main__':
    unittest.main()
