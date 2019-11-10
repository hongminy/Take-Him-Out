class basic_agent:
    def __init__(self, name = 'DefaultAgnet' ,alpha = 0.3, gamma = 1, n = 1):
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
        self.log = True
        self.name = name


    def get_possible_actions(self):
        return ["turn 1", "turn -1", "turn 0", "move 1", "move -1", "move 0" "strafe 1", "strafe -1", "strafe 0", "attack 1", "attack 0"]

    def stopLastCommand(self, agent_host):
        if self.lastCommand != None:
            agent_host.sendCommand(self.lastCommand[:-1].strip() + '0')

    def act(self, agent_host, command):
        self.stopLastCommand(agent_host)
        agent_host.sendCommand(command)
        self.lastCommand = command
        if self.log:
            print("{} choose: {}".format(self.name, command))












