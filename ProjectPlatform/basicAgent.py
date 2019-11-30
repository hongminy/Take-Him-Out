import json
import numpy as np

class basic_agent:
    def __init__(self, name = 'DefaultAgent', log = False):
        """Constructing an RL agent.

        Args
            alpha:  <float>  learning rate      (default = 0.3)
            gamma:  <float>  value decay rate   (default = 1)
            n:      <int>    number of back steps to update (default = 1)
        """
        self.step_count = 0
        self.lastCommand = None
        self.log = log
        self.name = name
        self.lastDamageTaken = 0
        self.lastDamageDelt = 0
        self.dataCollection = {'DamageTaken':0, 'DamageDealt':0,
                               'Life':0, 'XPos':0, 'ZPos':0,
                               'DistanceToOpponent':0, 'Yaw':0
                               }
        self.opponentDataCollection = {'Life':0, 'XPos':0, 'ZPos':0}
        self.observationFromPreviousMission = {'DamageTaken':0,'DamageDealt':0,
                                               'OpponentDamageTaken':0}

        self.observationNum = 1
        self.opponentObservationNum = 1
        self.actions = ["turn 1", "turn -1", "move 1", "move -1", "strafe 1", "strafe -1", "use 1"]

    def stopLastCommand(self, agent_host):
        if self.lastCommand != None:
            agent_host.sendCommand(self.lastCommand[:-1].strip() + '0')

    def act(self, agent_host, command):
        command = self.actions[command]
        self.stopLastCommand(agent_host)
        agent_host.sendCommand(command)
        self.lastCommand = command

    def log(self):
        print("{} 's state: {}\n".format(self.name, self.dataCollection))

        print("After considering his opponent's state: {}\n".format(self.opponentDataCollection))
        print("He choose to: {}".format(self.lastCommand))

    def observe(self, worldstate, opponent_state):
        # update the observation

        if self.observationNum<= 1 or self.opponentObservationNum <=1:
            if worldstate.number_of_observations_since_last_state > 0:
                state = json.loads(worldstate.observations[-1].text)
                self.observationFromPreviousMission['DamageTaken'] = state['DamageTaken']
                self.observationFromPreviousMission['DamageDealt'] = state['DamageDealt']
                self.dataCollection['DamageTaken'] = state['DamageTaken'] - self.observationFromPreviousMission[
                    'DamageTaken']
                self.dataCollection['DamageDealt'] = state['DamageDealt'] - self.observationFromPreviousMission[
                    'DamageDealt']
            if opponent_state.number_of_observations_since_last_state > 0:
                state = json.loads(opponent_state.observations[-1].text)
                self.observationFromPreviousMission['OpponentDamageTaken'] = state['DamageTaken']


        if worldstate.number_of_observations_since_last_state > 0:
            self.observationNum += 1
            state = json.loads(worldstate.observations[-1].text)
            #print(state)
            self.dataCollection['DamageTaken'] = state['DamageTaken'] - self.observationFromPreviousMission['DamageTaken']
            self.dataCollection['Life'] = state['Life']
            self.dataCollection['XPos'] = state['XPos']
            self.dataCollection['ZPos'] = state['ZPos']
            self.dataCollection['Yaw'] = state['Yaw']
            self.dataCollection['DistanceToOpponent'] = ((self.dataCollection['XPos']-\
                                                        self.opponentDataCollection['XPos'])**2 + (
                self.dataCollection['ZPos'] - self.opponentDataCollection['ZPos'] **2))**0.5

        if opponent_state.number_of_observations_since_last_state > 0:
            self.opponentObservationNum += 1
            state = json.loads(opponent_state.observations[-1].text)
            self.dataCollection['DamageDealt'] = state['DamageTaken'] - self.observationFromPreviousMission['OpponentDamageTaken']
            self.opponentDataCollection['Life'] = state['Life']
            self.opponentDataCollection['XPos'] = state['XPos']
            self.opponentDataCollection['ZPos'] = state['ZPos']

        if self.log:
            if worldstate.number_of_observations_since_last_state > 0:
                print("{} 's state: {}".format(self.name, self.dataCollection))
            if opponent_state.number_of_observations_since_last_state > 0:
                print("{} 's opponent: {}".format(self.name, self.opponentDataCollection))

    def get_observation(self):
        return np.array(list(self.dataCollection.values())+list(self.opponentDataCollection.values()))

    def refresh(self):
        self.lastDamageTaken = 0
        self.lastDamageDelt = 0
        self.lastCommand = None
        self.step_count = 0

    def calculate_reward(self):
        reward = 0
        reward -= 0.1
        if (self.dataCollection['DamageDealt'] > self.lastDamageDelt):
            reward += 50
            self.lastDamageDelt = self.dataCollection['DamageDealt']
        if self.dataCollection['DamageTaken'] > self.lastDamageTaken:
            reward -= 50
            self.lastDamageTaken = self.dataCollection['DamageTaken']
        return reward










