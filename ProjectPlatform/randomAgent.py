from basicAgent import basic_agent
import random
class random_agent(basic_agent):
    def __init__(self, name = 'DefaultAgnet' ,alpha = 0.3, gamma = 1, n = 1):
        basic_agent.__init__(self, name, alpha, gamma, n)


    def get_possible_actions(self):
        return random.choice(["turn 1", "turn -1", "move 1", "move -1", "strafe 1", "strafe -1", "attack 1", "attack 0"])



