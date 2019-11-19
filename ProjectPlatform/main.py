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
import os
import sys
import time
import json
def safeStartMission(agent_host, my_mission, my_client_pool, my_mission_record, role, expId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            # Attempt start:
            agent_host.startMission(my_mission, my_client_pool, my_mission_record, role, expId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)
# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
opponent = MalmoPython.AgentHost()
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
# Attempt to start a mission:
safeStartMission(spectator, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 0, 'Test')
safeStartMission(opponent, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 1, 'Test')
safeStartMission(agent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 2, 'Test')
# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = spectator.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = spectator.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
print()
print("Mission running ", end=' ')
spectator.sendCommand("chat /setblock 0 0 0 minecraft:repeating_command_block 0 destory {Command:\"/execute @e[type=Snowball] ~ ~ ~ /summon Fireball ~ ~ ~ {Motion:[0.0,0.0,0.0],direction:[0.0,0.0,0.0]}\"}")
spectator.sendCommand("chat /setblock 0 1 0 minecraft:redstone_block 0 replace")
# Loop until mission ends:
while world_state.is_mission_running:
    time.sleep(5)
    world_state = spectator.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
print()
print("Mission ended")
# Mission has ended.