try:
    from malmo import MalmoPython
except:
    import MalmoPython

from utility import safeStartMission,reload,updateWorldState
from basicAgent import basic_agent
import os
import sys
import time

NUM_OF_GAMES = 100

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)
# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
opponent_host = MalmoPython.AgentHost()
spectator = MalmoPython.AgentHost()

try:
    spectator.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(spectator.getUsage())
    exit(1)
if spectator.receivedArgument("help"):
    print(spectator.getUsage())
    exit(0)
mission_file = './simple_arena.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission.forceWorldReset()
my_mission_record = MalmoPython.MissionRecordSpec()
# Making a ClientPool
client_pool = MalmoPython.ClientPool()
for x in range(10000, 10000 + 3 + 1):
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1', x) )




#---MainLoop------MainLoop------MainLoop------MainLoop------MainLoop------MainLoop---#

for i in range(NUM_OF_GAMES):
    # Attempt to start a mission for opponent, Steve, and spectator:
    my_mission.forceWorldReset()
    agent = basic_agent("Steve",False) 
    safeStartMission(spectator, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 0, 'Test')
    safeStartMission(opponent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 1, 'Test')
    safeStartMission(agent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 2, 'Test')
    # Loop until mission starts:
    print("Waiting for the mission to start ", end=' ')
    spectator_state, agent_state, opponent_state = updateWorldState(spectator,agent_host,opponent_host)
    while not (spectator_state.has_mission_begun and agent_state.has_mission_begun and opponent_state.has_mission_begun):
        print(".", end="")
        time.sleep(0.1)
        spectator_state, agent_state, opponent_state = updateWorldState(spectator, agent_host, opponent_host)
        for error in spectator_state.errors:
            print("Error:",error.text)
    print()
    print("Mission running ", end=' ')
    print()
    spectator.sendCommand("chat Guys, this is a new mission")
    spectator.sendCommand("chat /gamerule sendCommandFeedback false")
    spectator.sendCommand("chat /gamerule commandBlockOutput false")
    spectator.sendCommand("chat /gamerule naturalRegeneration false")
    spectator.sendCommand("chat /setblock 0 0 0 minecraft:repeating_command_block 0 destory {Command:\"/execute @e[type=Snowball] ~ ~ ~ /summon Fireball ~ ~ ~ {ExplosionPower:0,Motion:[0.0,0.0,0.0],direction:[0.0,0.0,0.0]}\",auto:1b}")
    #---------------- Current mission started --------------------#
    while agent_state.is_mission_running and opponent_state.is_mission_running:
        spectator_state, agent_state, opponent_state = updateWorldState(spectator,agent_host,opponent_host)
        reload(spectator,spectator_state,agent_state,opponent_state)
        # reload the agents with "snowball" when they are out of ammo
        agent.observe(agent_state,opponent_state)
        observation = agent.get_observation()
        observation = agent.get_observation()
        reward = agent.calculate_reward()
        # make the agent observe worldstate
        # action = agent.get_possible_actions()
        # agent.act(agent_host,action)
        time.sleep(0.1)
