# Simulation code for an Evolutionary Iterated Prisoner's Dilemma
# Simulation parameters can be tweaked to examine situations that encourage cooperation
# Aaron Morgenegg, A02072659

import random

# Parameters/Constants to manipulate the program

RATIO_AD = .9 # Ratio of agents that start as Always Defect
NUMBER_OF_GAMES = 10 # number of games agents will play for each round


class Agent:
    def __init__(self):
        # True represents Tit-for-Tat, False represents Always Defect
        self.trust = self.GetStartingTrust()
        self.payoff = 0
        self.last_result = True

    def Play(self):
        if self.trust is False:
            # always defect
            return False
        if self.trust is True:
            # TFT strategy
            return self.last_result

    def GetStartingTrust(self):
        if random.random() <= RATIO_AD:
            return False
        else:
            return True

    def ResetPayoff(self):
        self.payoff = 0

def PrisonersDilemma(agentA, agentB):
    if agentA.Play() is True and agentB.Play() is True:
        # Both agents cooperate
        agentA.last_result = True
        agentB.last_result = True
        return (2,2)
    if agentA.Play() is True and agentB.Play() is False:
        # A cooperates, B defects
        agentA.last_result = False
        agentB.last_result = True
        return (0,3)
    if agentA.Play() is False and agentB.Play() is True:
        # A defects, B cooperates
        agentA.last_result = True
        agentB.last_result = False
        return (3,0)
    if agentA.Play() is False and agentB.Play() is False:
        # Both agents defect
        agentA.last_result = False
        agentB.last_result = False
        return (1,1)

def IteratedPrisonersDilemma(agentA, agentB):
    for k in range(0, NUMBER_OF_GAMES):
        result = PrisonersDilemma(agentA, agentB)
        agentA.payoff += result[0]
        agentB.payoff += result[1]
    agentA.last_result = agentA.trust
    agentB.last_result = agentB.trust

class Society:
    def __init__(self, num_agents):
        self.agents = self.GetStartingAgents(num_agents)

    def GetStartingAgents(self, num_agents):
        agents = []
        for i in range(num_agents):
            agents.append(Agent())
        return agents

    def RunIteratedPrisonersDilemma(self):
        self.ResetPayoffs()
        for i in range(len(self.agents)-1):
            for j in range(i+1, len(self.agents)):
                IteratedPrisonersDilemma(self.agents[i], self.agents[j])


    def ResetPayoffs(self):
        for agent in self.agents:
            agent.ResetPayoff()

    def __str__(self):
        society_str = '--- Society ---\n'
        for i in range(len(self.agents)):
            society_str += 'Agent: {}, Trust: {}, Payoff: {}\n'.format(i, self.agents[i].trust, self.agents[i].payoff)

        return society_str

if __name__ == '__main__':
    my_society = Society(100)
    my_society.RunIteratedPrisonersDilemma()
    print(my_society)
