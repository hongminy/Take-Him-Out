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
import gym
from utility import plotLearning
from gym import wrappers
import keras
import tensorflow as tf


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


if __name__ == '__main__':
    config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 6} ) 
    sess = tf.Session(config=config) 
    keras.backend.set_session(sess)
    lr = 0.0005
    n_games = 100
    DQN_AGENT = Agent(gamma=0.99, epsilon=1, alpha=lr, input_dims=10,
                  n_actions=7, mem_size=1000000, batch_size=64, epsilon_end=0.0)

    #DQN_AGENT.load_model()
    scores = []
    eps_history = []

    for i in range(NUM_OF_GAMES):
        # ---------------Epsiode setup------------#
        score = 0
        my_mission.forceWorldReset()
        agent = basic_agent("Steve",False) 

        # Attempt to start a mission for opponent, Steve, and spectator:
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
        observation = agent.get_observation()
        #---------------- Current mission started --------------------#
        while agent_state.is_mission_running and opponent_state.is_mission_running:
            done = (agent_state.is_mission_running and opponent_state.is_mission_running)
            spectator_state, agent_state, opponent_state = updateWorldState(spectator,agent_host,opponent_host)
            reload(spectator,spectator_state,agent_state,opponent_state)
            # reload the agents with "snowball" when they are out of ammo

            action = DQN_AGENT.choose_action(observation)
            agent.act(agent_host,action)
            agent.observe(agent_state,opponent_state)
            observation_ = agent.get_observation()
            reward = agent.calculate_reward()
            score += reward
            DQN_AGENT.remember(observation, action, reward, observation_, int(done))
            observation = observation_
            DQN_AGENT.learn()
            time.sleep(0.05)

        eps_history.append(DQN_AGENT.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[max(0, i-100):(i+1)])
        print('episode: ', i,'score: %.2f' % score,
              ' average score %.2f' % avg_score)

        if i % 10 == 0 and i > 0:
            DQN_AGENT.save_model()

    filename = 'Take-Him-Out.png'

    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)


    # for i in range(n_games):
    #     score = 0
    #     observation = env.reset()
    #     while not done:
    #         action = agent.choose_action(observation)
    #         observation_, reward, done, info = env.step(action)
    #         score += reward
    #         agent.remember(observation, action, reward, observation_, int(done))
    #         observation = observation_
    #         agent.learn()

    #     eps_history.append(agent.epsilon)
    #     scores.append(score)

    #     avg_score = np.mean(scores[max(0, i-100):(i+1)])
    #     print('episode: ', i,'score: %.2f' % score,
    #           ' average score %.2f' % avg_score)

    #     if i % 10 == 0 and i > 0:
    #         agent.save_model()

# Mission has ended.