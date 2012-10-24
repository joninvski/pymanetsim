#########
Tutorials
#########

Tutorial 1 - Simple and direct
==============================

In this tutorial I will try to explain how to create a very simple protocol capable of sending a message from a source node to a destination node. This example is particularly useful for simulating any real protocol, but will introduce you with the basic concepts present in PyManetSim.

1 - Setting up variables
------------------------
I have to check this better, but for now the only variable you need to set up is PYTHONPATH.
Just do in your prompt::

   PYTHONPATH=.


2 - Create a Simple Node
------------------------
Let's start by creating the nodes which will send and receive the messages. You can check this code at pymanetsim/protocols/simple_and_direct/protocol.py

A node must implement two basic methods. The constructor and the pass time method which tells the node that a time unit (called a cycle) has just passed::

    from node import Node

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
            return {'messages':[], 'asynchronous':[], 'simulator':[]} #Don't forget to say the simulator you do not whish to send anything new

        def handle_send_msg_event(self, destiny_id):
            text="Hello. I am " + self.id + " and my time is " + str(self.time_counter)
            simple_message = SimpleMessage(sender=self, destiny_id=destiny_id, text=text)
            return {'messages':[simple_message], 'asynchronous':[], 'simulator':[]}

In the pass_time method we use the time_counter variable to be our own time watch. The return value is a simple dictionary in which we say to the simulator that the node does not which to send any messages, any asynchronous event, and any simulator event. Basically we want the node to remain quiet.

The last two methods (receive_simple_message and handle_send_msg_event) will be explained in the following sections.

3 - Simple message and event
----------------------------
Now we will create the messages and events that our simple protocol will deal with::

    from messages import DirectMessage

    class SimpleMessage(DirectMessage):
        def __init__(self, sender, destiny_id, text):
            arguments = {'text':text}
            DirectMessage.__init__(self, sender=sender, emit_location=sender.location, function_to_call=SimpleNode.receive_simple_message, arguments=arguments)

Note that the function to call is the receive_simple_message specified in the Node class. The dictionary "arguments" will have as keys the parameters of that function (which in this case is text).

Now for the event. We will create the SendSimpleMsgEvent which tells a node that it must send a message::

    from events import AsynchronousEvent

    class SendSimpleMsgEvent(AsynchronousEvent):
        def __init__(self, origin_id, destiny_id):
            arguments = {'destiny_id':destiny_id}
            AsynchronousEvent.__init__(self, node_id=origin_id, function_to_call=SimpleNode.handle_send_msg_event, arguments=arguments)

Now look at the method: handle_send_msg_event at the SimpleNode class. It's parameters are the arguments passed in the event. In this case the destiny_id of the node that the message will be sent to.

4 - Create the ProtocolManager
------------------------------
For now our ProtocolManager won't do nothing. Just create it to make the simulator happy::

    class SimpleManager(object):
        def __init__(self, protocol_arguments=None):
            pass

        def manage(self, time, all_nodes, event_broker, message_broker):
            pass

If you look pymanetsim/protocols/simple_and_direct/protocol.py you will see that actually simple manager has some more things. But these are for the tutorial number two. For this tutorial the previous code also works.

5 - Specify the map
-------------------
Ok, let's now start to create the map we're all our nodes will reside. I admit that your current path is at the PyManetSim directory. From now on use an interactive python console, like ipython. If you want all the following commands are in the file pymanetsim/protocols/simple_and_direct/test_it.py.

PyManetSim gives us two options for creating our maps. Loading a previously generated map from a file or specify various parameters and let the simulator create a random map which obeys those parameters.

Let's start by loading an already existing map::

    from simulator import PlaneParameters

    plane_p = PlaneParameters(scenario_file = "../maps/map1.txt")

map1.txt is simply a map with only three nodes all next to each other.

6 - Create a configuration parameter
------------------------------------
Now lets define what are the configuration parameters for the simulation::

    from simulator import ConfigurationParameters
    from protocols.simple_and_direct.protocol import SimpleNode, SimpleManager

    config_p = ConfigurationParameters(
                    max_cycles=60, # The maximum number of cycles the simulation will run
                    events=[], #Starting events when the simulation starts
                    type_of_nodes=SimpleNode, #What is the type of nodes to be used in the simulation
                    protocol_manager=SimpleManager #What is the protocol manager responsible managing the protocol
                )

7 - Start the simulation
------------------------

Ok. Now you only need to create the simulation and run it::

    from simulator import Simulation, SimulationParameters

    simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)
    sim1 = Simulation(simulation_parameters)
    sim1.run(cycles_to_run=2) #Nothing should happen

Nothing happened because no asynchronous event has yet trigger the sending of a message. Imagine asynchronous events to be the event of a user requesting to send a message. You must tell the simulator when this has happened::

    from protocols.simple_and_direct.protocol import SendSimpleMsgEvent

    #Let create an event for a node to send a msg to another
    event = SendSimpleMsgEvent(origin_id="1", destiny_id="2")
    sim1.event_broker.add_asynchronous_event(event)

    sim1.run(cycles_to_run=2) #You should see that the message was received


Tutorial 2 - Automatizing things
================================

Now that the basic functions of pymanetsym where introduced in the first tutorial, let's explore a little bit more by automatizing several simulation parameters. This should replace the steps 5 to 8 in the previous tutorial.

1 - Create a job file
---------------------

Let's create a job file with the name job_simple_protocol at the pymanetsim/ where all the parameters for the simulation will be specified::

    from protocols.simple_and_direct.protocol import SimpleNode, SimpleManager

    plane_parameters = {
        'x_size':30,        #Horizontal lenght of the map
        'y_size':30,        #Vertical height of the map
        'min_degree':-1,    #Min degree of neighbhours (We put -1 to remember us that this parameter will be changed)
        'max_degree':7,     #Min degree of neighbhours
        'number_of_nodes':30 #Number of nodes in the plane

    }

    protocol_parameters = {
        'arguments':{
            'time_interval_to_launch_events':2, # The protocol manager will launch all 2 cycles
            'number_of_events_to_lauch':5       # Until 5 events are launched
        },
    }

    node_parameters = {
        'arguments':{}, #The arguments to pass when builind a node
    }

    config_parameters = {
        'max_cycles':100,           #Max cycles that the simulation will run
        'events':{},                #The events the simulation starts with
        'type_of_nodes':SimpleNode, #The type of node to create
        'protocol_manager':SimpleManager, #The protocol manager to use
    }

    x_variable_field = "plane_p.min_degree" #Tells what is the field that changes
    x_variable_name = "min_degree" #Tells what is the human readable name of the field that changes
    x_variable_values = range(2, 7) #A list containing all the values that the x_variable_field will variate
    y_variables = {
                    'total_messages':SimpleManager.get_total_messages, #What will we read in the y variables
                  }
    job_name = "simple_protocol"

**Note**: In the plane parameters you could also do as with the previous tutorial and specify a scenario_file. You could do this by changing plane_parameters to::

    plane_parameters = {
        'scenario_file':"../maps/map1.txt",        #Horizontal lenght of the map
    }

But then the variable to change could no longer be the minimum degree of neighbours in the plane as the map was not generate by the simulator.

2 - Register the job
--------------------

Now that the job file which gives the specifications a simulation is specified, we need to register the job so that pymanetsim know that it must run it.

To do so, open the file job_list.py and insert the module at the ALL_JOBS list::

    import simulations.jobs.job_simple

Tutorial 3 - Epidemic Broadcast Protocol
========================================

TODO
