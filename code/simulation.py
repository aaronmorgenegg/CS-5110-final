# Simulation code for an Evolutionary Iterated Prisoner's Dilemma
# Simulation parameters can be tweaked to examine situations that encourage cooperation
# Aaron Morgenegg, A02072659

import random

RATIO_AD = .8 # Ratio of agents that start as Always Defect

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

if __name__ == '__main__':
    agentA = Agent()
    agentB = Agent()
    for i in range(5):
        print(PrisonersDilemma(agentA, agentB))
