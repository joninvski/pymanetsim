*********************
Architecture Overview
*********************

Core Classes
============

The PyManetSim is defined by a few core classes:

* The simulation class

  This class is how simulations are encapsulated.
  It receives as arguments the conditions which completely characterize the simulation.

  Each simulation has a message_broker and a event_broker.
  The message_broker is responsible for storing pending messages that are to be transmitted between nodes in the next cycle.
  The event_broker has a similar role but with simulator events and asynchronous events.

* The Nodes and the Protocol Manager

  When you implement a protocol most work relies on developing these two classes.
  The node class should implement the behaviour expected by a node which can deal with the protocol.

  The protocol manager is responsible to:
   * Manage the global behaviour of the protocol, by for example sending events to the nodes.
   * Recording the desired measurements
   * Deal with the node creation (TODO - Not at this time, but this maybe useful)

* Job_list and jobs

  You specify the tests to be run in the PyManetSim simulator by first creating a new job in the simulator/jobs directory.
  This job file should contain the various parameters that will passed when creating a new simulation.

  In the job_list module you should list all the jobs that you wish to test

Simulation Time
===============
To represent the concept of time in PyManetSim, a simulation class does specific workflow in a atomic time unit (which will call cycle).

Each cycle the simulation instance does the following actions:

* Tells the protocol manager to manage (Duh!!) the cycle

  This is an opportunity for the protocol manager to look at the state of the protocol, and to do the action that it wishes to to.

* Runs any pending asynchronous events

  Every pending asynchronous event is executed. No relative order is guaranteed between the events.
  The only thing which is guaranteed is that all pending events will be executed that cycle.
  Once again no relative order between the messages in a cycle is guaranteed

* Delivers pending messages to the correct nodes

  All messages present in the message broker are delivered to the respective correct destinations. This depends on the location
  and transmission power of the broadcaster, as well as it nodes.

* Tells nodes that another cycle has passed

  This is done to represent the passing of time in the node. Whenever the node is told that a time unit (cycle) has
  passed it can for example increment a time counter.

Making different map types
==========================
There are several map builders available to you in TODO

Making nodes move
=================
Still TODO
