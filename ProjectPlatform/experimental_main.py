try:
    from malmo import MalmoPython
except:
    import MalmoPython
from utility import safeStartMission,reload,updateWorldState
from basicAgent import basic_agent
import os
import sys
import time
#---------- RL Libraries ------------#
from DeepQ import Agent
import numpy as np

from utility import plotLearning

import keras
import tensorflow as tf


NUM_OF_GAMES = 1000

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


if __name__ == '__main__':

    #------------------ GPU CONFIG --------------------#
    keras.backend.tensorflow_backend._get_available_gpus()
    lr = 0.0005
    n_games = 100
    DQN_AGENT = Agent(gamma=0.99, epsilon=0.4, alpha=lr, input_dims=10, epsilon_dec=0.999,
                  n_actions=7, mem_size=1000000, batch_size=64, epsilon_end=0.4)

    MODEL_NUM = 30
    DQN_AGENT.load_model('Models/Model_'+str(MODEL_NUM))
    print("Loading Model_"+str(MODEL_NUM))
    scores = []
    eps_history = []
    times = []

    for i in range(MODEL_NUM, NUM_OF_GAMES):
        # ---------------Epsiode setup------------#
        score = 0
        my_mission.forceWorldReset()
        agent = basic_agent("Steve",False) 

        check_time = time.time()
        # Attempt to start a mission for opponent, Steve, and spectator:
        safeStartMission(spectator, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 0, 'Test')
        safeStartMission(opponent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 1, 'Test')
        safeStartMission(agent_host, my_mission, client_pool, MalmoPython.MissionRecordSpec(), 2, 'Test')


        # Loop until mission starts:
        retry_flag = False
        spectator_state, agent_state, opponent_state = updateWorldState(spectator,agent_host,opponent_host)
        while not (spectator_state.has_mission_begun and agent_state.has_mission_begun and opponent_state.has_mission_begun):
            wait_time = time.time()
            if(wait_time - check_time) > 10:
                i -= 1
                retry_flag = True
                print("Mission Start error retrying...")
                break
            time.sleep(0.1)
            spectator_state, agent_state, opponent_state = updateWorldState(spectator, agent_host, opponent_host)
            for error in spectator_state.errors:
                print("Error:",error.text)
        if retry_flag:
            continue
        spectator.sendCommand("chat Guys, this is a new mission")
        spectator.sendCommand("chat /gamerule sendCommandFeedback false")
        spectator.sendCommand("chat /gamerule commandBlockOutput false")
        spectator.sendCommand("chat /gamerule naturalRegeneration false")
        spectator.sendCommand("chat /setblock 0 0 0 minecraft:repeating_command_block 0 destory {Command:\"/execute @e[type=Snowball] ~ ~ ~ /summon Fireball ~ ~ ~ {ExplosionPower:0,Motion:[0.0,0.0,0.0],direction:[0.0,0.0,0.0]}\",auto:1b}")
        observation = agent.get_observation()
        #---------------- Current mission started --------------------#
        while agent_state.is_mission_running and opponent_state.is_mission_running:
            start_time = time.time()
            done = (agent_state.is_mission_running and opponent_state.is_mission_running)
            spectator_state, agent_state, opponent_state = updateWorldState(spectator,agent_host,opponent_host)
            reload(spectator,spectator_state,agent_state,opponent_state)
            # reload the agents with "snowball" when they are out of ammo

            action = DQN_AGENT.choose_action(observation)
            agent.act(agent_host,action)
            # choose action and act

            #------------------ Agent Learn---------------#
            agent.observe(agent_state,opponent_state)
            observation_ = agent.get_observation()
            reward = agent.calculate_reward()
            score += reward
            DQN_AGENT.remember(observation, action, reward, observation_, int(done))
            observation = observation_
            DQN_AGENT.learn()
            time.sleep(0.15)
            #----------------- Agent Learn---------------#

        eps_history.append(DQN_AGENT.epsilon)
        scores.append(score)
        times.append((time.time() - start_time))

        avg_score = np.mean(scores[max(0, i-100):(i+1)])
        print('episode: ', i,'score: %.2f' % score,
              ' average score %.2f ' % avg_score, 'Epsilon:', DQN_AGENT.epsilon)

        if i % 10 == 0 and i > 0:
            DQN_AGENT.save_model('Models/Model_{}'.format(i))

    score_file = 'Graphs/DQN_Score.png'
    time_file = 'Graphs/DQN_Time.png'
    x = [i+1 for i in range(NUM_OF_GAMES)]
    plotLearning(x, scores, eps_history, score_file)
    plotLearning(x, times, eps_history, time_file)
    DQN_AGENT.save_model('Models/Final.h5')

