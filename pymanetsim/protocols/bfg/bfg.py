import pdb
import random

from protocols.bfg.arguments import BfgProtocolArguments
from protocols.bfg.node import LookForDestination
import bloom


from configuration import DEBUG
from configuration import DRAW_MAPS

if DRAW_MAPS:
    #For the heat map without the masks
    import numpy as np
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    from pylab import subplot



# ------------ Protocol Manager ---------------->
class BfgProtocolManager(object):
    def __init__(self, protocol_arguments=None):
        self.arguments = BfgProtocolArguments(protocol_arguments)

        # This is for counting things ---->
        self.total_messages_sent = 0
        self.routes_found = 0

        self.total_follow_heat = 0
        self.total_random_walk = 0
        self.total_go_back = 0
        self.total_hello = 0
        self.total_dsr = 0
        self.have_heat = {}
        self.have_destiny = {}
        self.have_origin = {}
        self.test  = 0

        self.events_launched = 0
        # <----- Ended things for counting

        if DRAW_MAPS:
            plt.figure(1)


    def manage(self, time, all_nodes, event_broker, message_broker, plane=None):
        if self._time_to_launch_event(time):
            origin_id = self.arguments.origin_ids[self.events_launched % len(self.arguments.origin_ids)]
            event = LookForDestination(origin_id, self.arguments.destiny_ids[0],
                                       random_walk_multiply = self.arguments.random_walk_multiply,
                                       random_walk_max_hop = self.arguments.random_walk_max_hop,
                                       random_walk_time_to_give_up = self.arguments.random_walk_time_to_give_up)
            event_broker.add_asynchronous_event(event)
            self.events_launched += 1

        if DEBUG and time % 100 == 0:
            print "Heat: ", len(self.have_heat)
            print "Destiny:", len(self.have_destiny)
            print "Origin: ", len(self.have_origin)
            print "Found: ", self.routes_found
            print ""

        if DRAW_MAPS and (time % 5000) == 0 and len(self.arguments.destiny_ids) and plane > 0:
            subplot(6, 10, (time/5000))
            self.draw_heat_map(time, all_nodes, plane, self.arguments.destiny_ids[0])

    def _time_to_launch_event(self, time):
        return self.arguments.origin_ids and not (time + self.arguments.start_time) % self.arguments.time_interval and self.events_launched < self.arguments.number_of_routes_to_find

    def get_total_messages_sent(self):
        return self.total_messages_sent

    def get_total_follow_heat(self):
        return self.total_follow_heat

    def get_total_random_walk(self):
        return self.total_random_walk

    def get_total_go_back(self):
        return self.total_go_back

    def get_total_hello(self):
        return self.total_hello

    def get_total_dsr(self):
        return self.total_dsr

    def get_read_collision(self):
        value = bloom.BloomFilter.total_collisions_read
        bloom.BloomFilter.total_collisions_read = 0
        return value

    def get_routes_found(self):
        return self.routes_found

    def end_simulation(self, all_nodes, plane):
        #Lets draw the maps prior to the end
        if DRAW_MAPS:
            plt.savefig('/tmp/' + 'teste.png', dpi=500)
            self.draw_interesting_maps(all_nodes, plane)

    def draw_interesting_maps(self, all_nodes, plane):
        plt.figure(2)
        subplot(1,2,1)
        self.draw_heat_map("Final", all_nodes, plane, self.arguments.destiny_ids[0])

        subplot(1,2,2)
        self.draw_route_maps(all_nodes, plane, self.arguments.origin_ids, self.arguments.destiny_ids[0])

        plt.savefig('/tmp/' + str(random.random())[2:])

    def draw_heat_map(self, time, all_nodes, plane, target_id):
        #Draw the array of arrays that will be the draw map
        delta = 1
        x = [-1]*plane.x_size
        y = [-1]*plane.y_size
        X = np.meshgrid(x, y)

        #Fill the map with heats from all nodes
        for node in all_nodes.values():
            #Get its heat value (Higher values have less heat (so the graphic looks nice)
            heat = len(node.heat_mem) - node._node_in_what_level_of_mem(target_id, node.heat_mem) + 1

            #Put that value on the heat map
            x = node.location.x
            y = node.location.y
            X[0][x][y] = heat

        #Our target id will have a very high value to be caught by the next mask
        #TODO - Make this with multiple destinations
        location = all_nodes[target_id].location
        X[0][location.x][location.y] = len(node.heat_mem) + 11

        #Mask the target_id value (which is very high) and also mask the places where there are no nodes
        Zm = np.masked_where(X[0] > len(node.heat_mem) + 10, X[0])
        palette = cm.gray
        palette.set_over('b', 0.0) #Where there are nodes that know nothing
        palette.set_under('black', 0.0) #Where there are no nodes
        palette.set_bad('r', 0.0) #Where the target id is

        plt.axis('off')

        #Draw the heat map
        im = plt.imshow(Zm, interpolation='nearest',
                        cmap=palette,
                        norm = colors.Normalize(vmin = 0, vmax = len(node.heat_mem) + 1, clip = False),
                        origin='lower',
                        extent=[0,plane.x_size,0,plane.y_size])
        plt.title(str(time) + " Heat map", fontsize=4)


    def draw_route_maps(self, all_nodes, plane, origin_ids, target_id):
        """ Right now it only draws the origins """
        #Draw the array of arrays that will be the draw map
        delta = 1
        x = [-1]*plane.x_size
        y = [-1]*plane.y_size
        X = np.meshgrid(x, y)

        #Fill the map with heats from all nodes
        for node in all_nodes.values():
            #Get its heat value (Higher values have less heat (so the graphic looks nice)
            heat = node._node_in_what_level_of_mem(target_id, node.tunnel_mem)

            #Put that value on the heat map
            x = node.location.x
            y = node.location.y
            if heat == 0:
               X[0][x][y] = heat + 1

        #Fill the map with heats from all nodes
        for id in origin_ids:
            #Get its heat value (Higher values have less heat (so the graphic looks nice)
            #Put that value on the heat map
            node = all_nodes[id]
            x = node.location.x
            y = node.location.y
            X[0][x][y] = 10

        palette = cm.gray
        palette.set_over('b', 0.0) #Where there are nodes that know nothing
        palette.set_under('black', 0.0) #Where there are no nodes
        palette.set_bad('r', 0.0) #Where the target id is

        Zm = np.masked_where(X[0] > 9, X[0])
        #Draw the heat map
        im = plt.imshow(Zm, interpolation='nearest',
                        cmap=palette,
                        norm = colors.Normalize(vmin = 0, vmax = 1, clip = False),
                        origin='lower',
                        extent=[0,plane.x_size,0,plane.y_size])
        plt.title("Route map")
# <------------ Protocol Manager ----------------
