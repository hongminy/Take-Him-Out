import json
class basic_agent:
    def __init__(self, name = 'DefaultAgent', log = False, alpha = 0.3, gamma = 1, n = 1):
        """Constructing an RL agent.

        Args
            alpha:  <float>  learning rate      (default = 0.3)
            gamma:  <float>  value decay rate   (default = 1)
            n:      <int>    number of back steps to update (default = 1)
        """
        self.alpha, self.gamma, self.n = alpha, gamma, n
        self.epsilon = 0.2
        self.q_table = {}
        self.step_count = 0
        self.lastCommand = None
        self.log = log
        self.name = name
        self.observation = None
        self.dataCollection = {'DamageTaken':0, 'DamageDealt':0, 'Life':0, 'XPos':0, 'ZPos':0}
        self.opponentDataCollection = {'Life':0, 'XPos':0, 'ZPos':0}
        self.observationFromPreviousMission = {'DamageTaken':0, 'DamageDealt':0}
        self.round = 1


    def get_possible_actions(self):
        return ["turn 1", "turn -1", "turn 0", "move 1", "move -1", "move 0" "strafe 1", "strafe -1", "strafe 0", "use 1", "use 0"]

    def stopLastCommand(self, agent_host):
        if self.lastCommand != None:
            agent_host.sendCommand(self.lastCommand[:-1].strip() + '0')

    def act(self, agent_host, command):
        self.stopLastCommand(agent_host)
        agent_host.sendCommand(command)
        self.lastCommand = command
        if self.log:
            print("Round {}: {} choose to: {}".format(self.round, self.name, command))
        self.round += 1

    def log(self):
        print("Round {}".format(self.round))
        print("{} 's state: {}\n".format(self.name, self.dataCollection))

        print("After considering his opponent's state: {}\n".format(self.opponentDataCollection))
        print("He choose to: {}".format(self.name, self.lastCommand))

    def observe(self, worldstate, opponent_state):
        # update the observation

        if worldstate.number_of_observations_since_last_state > 0:
            state = json.loads(worldstate.observations[-1].text)
            if self.round <= 1:
                self.observationFromPreviousMission['DamageTaken'] = state['DamageTaken']
                self.observationFromPreviousMission['DamageDealt'] = state['DamageDealt']
                self.dataCollection['DamageTaken'] = state['DamageTaken'] - self.observationFromPreviousMission['DamageTaken']
                self.dataCollection['DamageDealt'] = state['DamageDealt'] - self.observationFromPreviousMission['DamageDealt']
            else:
                self.dataCollection['DamageTaken'] = state['DamageTaken'] - self.observationFromPreviousMission['DamageTaken']
                self.dataCollection['DamageDealt'] = state['DamageDealt'] - self.observationFromPreviousMission['DamageDealt']
                self.dataCollection['Life'] = state['Life']
                self.dataCollection['XPos'] = state['XPos']
                self.dataCollection['ZPos'] = state['ZPos']
        if opponent_state.number_of_observations_since_last_state > 0:
            opponent_state = json.loads(opponent_state.observations[-1].text)
            self.opponentDataCollection['Life'] = opponent_state['Life']
            self.opponentDataCollection['XPos'] = opponent_state['XPos']
            self.opponentDataCollection['ZPos'] = opponent_state['ZPos']

        if self.log:
            print("{} 's state: {}".format(self.name, self.dataCollection))
            print("{} 's opponent: {}".format(self.name, self.opponentDataCollection))











