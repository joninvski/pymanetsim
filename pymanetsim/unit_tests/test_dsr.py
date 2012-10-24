import pdb
import unittest

from plane import Location
from protocols.dsr.dsr import DsrProtocolManager
from protocols.dsr.node import DsrNode

from events import RouteFoundEvent, EventBroker
from messages import MessageBroker

class TestDSR(unittest.TestCase):
    def setUp(self):
        self.location_a = Location(5, 3)
        self.location_b = Location(4, 3)
        self.location_c = Location(4, 2)
        self.protocol_manager = DsrProtocolManager()

    def test_dsr_node_creation(self):
        node_a = DsrNode(node_id="1", location=self.location_a)
        self.assert_(node_a.id)
        self.assertEquals(node_a.location, self.location_a)

    def test_dsr_start_query_event(self):
        node_a = DsrNode(node_id="2", location=self.location_a, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_a.start_looking_for_target(origin_id=node_a.id, destiny_id=node_c)
        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is DsrNode.run_node_forward.im_func)
        self.assertFalse(new_message[0].function_to_call.im_func is DsrNode.run_node_backward.im_func)
        self.assertEquals(new_message[0].sender, node_a)
        self.assertEquals(new_message[0].emit_location, self.location_a)

    def test_dsr_forward_origin(self):
        node_a = DsrNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="2", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_a.run_node_forward(query_id=10, origin_id=node_a.id, previous_node=None, destiny_id=node_c)
        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is DsrNode.run_node_forward.im_func)
        self.assertFalse(new_message[0].function_to_call.im_func is DsrNode.run_node_backward.im_func)
        self.assertEquals(new_message[0].sender, node_a)
        self.assertEquals(new_message[0].emit_location, self.location_a)

    def test_dsr_forward_retransmit(self):
        node_a = DsrNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = DsrNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_b.run_node_forward(query_id=10, origin_id=node_a.id, previous_node=node_a, destiny_id=node_c.id)

        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is DsrNode.run_node_forward.im_func)
        self.assertFalse(new_message[0].function_to_call.im_func is DsrNode.run_node_backward.im_func)
        self.assertEquals(new_message[0].sender, node_b)
        self.assertEquals(new_message[0].emit_location, self.location_b)

        self.assertEquals(node_b.responded_queries[(node_a.id, 10)], node_a)

    def test_dsr_forward_destiny_id(self):
        node_a = DsrNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = DsrNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_c.run_node_forward(query_id=10, origin_id=node_a.id, previous_node=node_b, destiny_id=node_c.id)
        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertFalse(new_message[0].function_to_call.im_func is DsrNode.run_node_forward.im_func)
        self.assertTrue(new_message[0].function_to_call.im_func is DsrNode.run_node_backward.im_func)

        self.assertEquals(new_message[0].sender, node_c)
        self.assertEquals(new_message[0].emit_location, self.location_c)

    def test_dsr_not_retransmit(self):
        node_a = DsrNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = DsrNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_b.run_node_forward(query_id=10, origin_id=node_a.id, previous_node=node_a, destiny_id=node_c.id)
        new_message = new_events_and_messages['messages']
        self.assert_(new_message)

        new_events_and_messages = node_b.run_node_forward(query_id=10, origin_id=node_a.id, previous_node=node_c, destiny_id=node_c.id)
        self.assertFalse(new_events_and_messages['messages'])

    def test_dsr_backward_retransmit(self):
        node_a = DsrNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = DsrNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        node_b.responded_queries[(node_a.id, 10)] = node_a
        new_events_and_messages = node_b.run_node_backward(query_id=10, origin_id=node_a.id, previous_node=node_c, destiny_id=node_c.id, next_node=node_b, route=[])
        new_message = new_events_and_messages['messages']

        self.assertTrue(new_message)
        self.assertTrue(new_message[0].function_to_call.im_func is DsrNode.run_node_backward.im_func)
        self.assertFalse(new_message[0].function_to_call.im_func is DsrNode.run_node_forward.im_func)
        self.assertEquals(new_message[0].sender, node_b)
        self.assertEquals(new_message[0].emit_location, self.location_b)

    def test_dsr_backward_no_retransmit(self):
        node_a = DsrNode(node_id="1", location=self.location_a)
        node_b = DsrNode(node_id="2", location=self.location_b)
        node_c = DsrNode(node_id="3", location=self.location_c)

        new_events_and_messages = node_b.run_node_backward(query_id=10, origin_id=node_a.id, previous_node=node_c, destiny_id=node_c, next_node=node_a, route=[])
        self.assertFalse(new_events_and_messages['messages'])

    def test_dsr_forward_reach_end(self):
        node_a = DsrNode(node_id="1", location=self.location_a, protocol_manager=self.protocol_manager)
        node_b = DsrNode(node_id="2", location=self.location_b, protocol_manager=self.protocol_manager)
        node_c = DsrNode(node_id="3", location=self.location_c, protocol_manager=self.protocol_manager)

        new_events_and_messages = node_a.run_node_backward(query_id=10, origin_id=node_a.id, previous_node=node_b, destiny_id=node_c.id, next_node=node_a, route=[])
        self.assertFalse(new_events_and_messages['messages'])

        #And check that the simulator events that represents that the route was found is launched
        new_simulator_events = new_events_and_messages['simulator']

        self.assertTrue(new_simulator_events)
        self.assert_(isinstance(new_simulator_events[0], RouteFoundEvent))


    def test_dsr_protocol_manager(self):
        dsr_protocol = DsrProtocolManager({'origin_ids':["1", "2"], 'destiny_ids':["3"], 'number_of_routes_to_find':2})

        message_broker = MessageBroker()
        event_broker = EventBroker()

        dsr_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 1)

        event = event_broker.get_asynchronous_event()
        self.assertEqual(event.arguments['origin_id'], "1")
        self.assertEqual(event.arguments['destiny_id'], "3")

        dsr_protocol.manage(time=11, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 1)

        event = event_broker.get_asynchronous_event()
        self.assertEqual(event.arguments['origin_id'], "2")
        self.assertEqual(event.arguments['destiny_id'], "3")

        dsr_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 0)

    def test_dsr_routes_to_find(self):
        dsr_protocol = DsrProtocolManager({'origin_ids':["1", "2"], 'destiny_ids':["3"], 'number_of_routes_to_find':4})

        message_broker = MessageBroker()
        event_broker = EventBroker()

        dsr_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 1)

        dsr_protocol.manage(time=11, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 2)

        dsr_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 3)

        dsr_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 4)

        dsr_protocol.manage(time=10, all_nodes=[], message_broker=message_broker, event_broker=event_broker)
        self.assertEqual(len(event_broker.asynchronous_events), 4)

    def test_dsr_protocol_manager_in_node(self):

        dsr_protocol_manager = DsrProtocolManager()
        dsr_node = DsrNode(node_id="1", protocol_manager=dsr_protocol_manager)

        self.assertEqual(dsr_node.protocol_manager, dsr_protocol_manager)

if __name__ == '__main__':
    unittest.main()
