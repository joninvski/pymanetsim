from simulator import PlaneParameters

plane_p = PlaneParameters(scenario_file = "../maps/map1.txt")

from simulator import ConfigurationParameters
from protocols.simple_and_direct.protocol import SimpleNode, SimpleManager

config_p = ConfigurationParameters(
                    max_cycles=60, # The maximum number of cycles the simulation will run
                    events=[], #Starting events when the simulation starts
                    type_of_nodes=SimpleNode, #What is the type of nodes to be used in the simulation
                    protocol_manager=SimpleManager #What is the protocol manager responsible managing the protocol
                )

from simulator import Simulation, SimulationParameters

simulation_parameters = SimulationParameters(config_parameters=config_p, plane_parameters=plane_p)
sim1 = Simulation(simulation_parameters)
sim1.run(cycles_to_run=2) #Nothing should happen

from protocols.simple_and_direct.protocol import SendSimpleMsgEvent

#Let create an event for a node to send a msg to another
event = SendSimpleMsgEvent(origin_id="1", destiny_id="2")
sim1.event_broker.add_asynchronous_event(event)

sim1.run(cycles_to_run=2) #You should see that the message was received

