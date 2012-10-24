from arguments import DsrProtocolArguments

from node import LookForDestination

# ------------ Protocol Manager ---------------->
class DsrProtocolManager(object):
    def __init__(self, protocol_arguments=None):
        self.total_messages_sent = 0
        self.routes_found = 0
        self.total_search_messages = 0
        self.total_go_back_message = 0

        self.events_launched = 0

        self.arguments = DsrProtocolArguments(protocol_arguments)

    def manage(self, time, all_nodes, event_broker, message_broker, plane=None):
        if self._time_to_launch_event(time):
            origin_id = self.arguments.origin_ids[self.events_launched % len(self.arguments.origin_ids)]
            event = LookForDestination(origin_id, self.arguments.destiny_ids[0])
            event_broker.add_asynchronous_event(event)
            self.events_launched += 1

    def _time_to_launch_event(self, time):
        return self.arguments.origin_ids and not (time + self.arguments.start_time) % self.arguments.time_interval and self.events_launched < self.arguments.number_of_routes_to_find

    def get_total_messages_sent(self):
        return self.total_messages_sent

    def get_routes_found(self):
        return self.routes_found

    def get_total_go_back_messages(self):
        return self.total_go_back_message

    def get_total_search_messages(self):
        return self.total_search_messages
# <------------ Protocol Manager ----------------
