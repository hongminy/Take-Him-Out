# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------
# Tutorial sample #7: The Maze Decorator
try:
    from malmo import MalmoPython
except:
    import MalmoPython

from utility import safeStartMission,reload,updateWorldState
from basicAgent import basic_agent
from randomAgent import random_agent
import os
import sys
import time
import json

# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
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
my_mission_record = MalmoPython.MissionRecordSpec()
# Making a ClientPool
client_pool = MalmoPython.ClientPool()
for x in range(10000, 10000 + 3 + 1):
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1', x) )

# Attempt to start a mission for opponent, Steve, and spectator:
safeStartMission(spectator, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 0, 'Test')
safeStartMission(opponent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 1, 'Test')
safeStartMission(agent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 2, 'Test')

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
spectator_state = spectator.getWorldState()
agent_state = agent_host.getWorldState()
opponent_state = opponent_host.getWorldState()

while not (spectator_state.has_mission_begun and agent_state.has_mission_begun and opponent_state.has_mission_begun):
    print(".", end="")
    time.sleep(0.1)
    spectator_state = spectator.getWorldState()
    opponent_state = opponent_host.getWorldState()
    agent_state = agent_host.getWorldState()
    for error in spectator_state.errors:
        print("Error:",error.text)
print()
print("Mission running ", end=' ')
spectator.sendCommand("chat Guys, this is a new mission")
spectator.sendCommand("chat /gamerule commandBlockOutput false")
spectator.sendCommand("chat /gamerule sendCommandFeedback false")
spectator.sendCommand("chat /setblock 0 0 0 minecraft:repeating_command_block 0 destory {Command:\"/execute @e[type=Snowball] ~ ~ ~ /summon Fireball ~ ~ ~ {ExplosionPower:0,Motion:[0.0,0.0,0.0],direction:[0.0,0.0,0.0]}\",auto:1b}")
spectator.sendCommand("chat /setblock 0 1 0 minecraft:redstone_block 0 replace")

agent = random_agent("Steve",True) #log = False
opponent = random_agent("Opponent",True)





# clear Worldstate before start

#---MainLoop------MainLoop------MainLoop------MainLoop------MainLoop------MainLoop---#


# Loop until mission ends:
while spectator_state.is_mission_running and agent_state.is_mission_running and opponent_state.is_mission_running:

    # Update: DamageTaken problem got fixed in basicAgent.py
    # update the three worldstates in the beginning of the loop
    # spectator, agent_host, opponent_host
    spectator_state, agent_state, opponent_state = updateWorldState(spectator,agent_host,opponent_host)
    reload(spectator,spectator_state,agent_state,opponent_state)
    # reload the agents with "snowball" when they are out of ammo
    agent.observe(agent_state,opponent_state)
    opponent.observe(opponent_state,agent_state)
    # make the agent observe worldstate
    action = agent.get_possible_actions()
    agent.act(agent_host,action)
    action = opponent.get_possible_actions()
    opponent.act(opponent_host,action)
    time.sleep(0.4)
    for error in spectator_state.errors:
        print("Error:",error.text)
print()
print("Mission ended")

# Mission has ended.
