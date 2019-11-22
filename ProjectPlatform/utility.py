try:
    from malmo import MalmoPython
except:
    import MalmoPython
import os
import sys
import time
import json
import random

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


def updateWorldState(spectator,steve,opponent):
    return spectator.getWorldState(), steve.getWorldState(), opponent.getWorldState()


def reload(spectator,spectator_state,steve_state,opponent_state):

    if steve_state.number_of_observations_since_last_state > 0:
        if json.loads(steve_state.observations[-1].text)['Hotbar_0_size'] <= 60:
            spectator.sendCommand("chat /replaceitem entity \"Steve\" slot.hotbar.0 minecraft:snowball 64")
    if opponent_state.number_of_observations_since_last_state > 0:
        if json.loads(opponent_state.observations[-1].text)['Hotbar_0_size'] <= 60:
            spectator.sendCommand("chat /replaceitem entity \"Opponent\" slot.hotbar.0 minecraft:snowball 64") 