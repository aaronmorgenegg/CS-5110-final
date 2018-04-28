# Simulation code for an Evolutionary Iterated Prisoner's Dilemma
# Simulation parameters can be tweaked to examine situations that encourage cooperation
# Aaron Morgenegg, A02072659

import random

# Parameters/Constants to manipulate the program

RATIO_AD = .8 # Ratio of agents that start as Always Defect
NUMBER_OF_GAMES = 6 # number of games agents will play for each round
CONNECTION_PROBABILITY = .01 # chance for agents to be connected
SOCIETY_SIZE = 500 # Number of agents in each society
NUMBER_OF_GENERATIONS = 10 # Number of evolutionary generations for each society's iterated games
NUMBER_OF_SOCIETIES = 100 # Number of societies to test and aggregate


class Agent:
    def __init__(self):
        # True represents Tit-for-Tat, False represents Always Defect
        self.trust = self.GetStartingTrust()
        self.payoff = 0
        self.last_result = True
        self.discontent = 0
        self.content = 0

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

    def __str__(self):
        return('Trust({}) Payoff({}) Discontent({}) Content({})'.format(self.trust, self.payoff, self.discontent, self.content))

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
        self.connections = self.SetConnectedAgents()

    def GetStartingAgents(self, num_agents):
        agents = []
        for i in range(num_agents):
            agents.append(Agent())
        return agents

    def SetConnectedAgents(self):
        connections = []
        for i in range(len(self.agents)):
            connections.append([])

        for i in range(len(self.agents)-1):
            for j in range(i+1, len(self.agents)):
                if(random.random() <= CONNECTION_PROBABILITY):
                    if j not in connections[i]: connections[i].append(j)
                    if i not in connections[j]: connections[j].append(i)

        return connections

    def RunIteratedPrisonersDilemma(self):
        self.ResetPayoffs()
        for i in range(len(self.agents)-1):
            for j in range(i+1, len(self.agents)):
                IteratedPrisonersDilemma(self.agents[i], self.agents[j])

        self.UpdateStrategies()

    def RunConnectedIteratedPrisonersDilemma(self):
        self.ResetPayoffs()
        for i in range(len(self.agents) - 1):
            for j in range(i + 1, len(self.agents)):
                if i in self.connections[j] and j in self.connections[i]:
                    IteratedPrisonersDilemma(self.agents[i], self.agents[j])

        self.UpdateStrategies()

    def RunEvolutionaryIteratedPrisonersDilemma(self, num_trials):
        print('Pre Trial Trust({}/{}) Content({}) Discontent({})'.format(self.MeasureTrust(), len(self.agents),
                                                                               self.MeasureContentness(),
                                                                               self.MeasureDiscontentness()))
        for i in range(num_trials):
            self.RunIteratedPrisonersDilemma()
            print('Trial({}) Trust({}/{}) Content({}) Discontent({})'.format(i, self.MeasureTrust(), len(self.agents), self.MeasureContentness(), self.MeasureDiscontentness()))

    def RunConnectedEvolutionaryIteratedPrisonersDilemma(self, num_trials):
        print('Pre Trial Trust Ratio({})'.format(self.MeasureTrust()/len(self.agents)))
        for i in range(num_trials):
            self.RunConnectedIteratedPrisonersDilemma()
            print('Trial({}) Trust({}/{}) Content({}) Discontent({})'.format(i, self.MeasureTrust(), len(self.agents), self.MeasureContentness(), self.MeasureDiscontentness()))
        print('Post Trial Trust Ratio({}) Contentness Ratio({})'.format(self.MeasureTrust() / len(self.agents), round(self.MeasureContentness()/self.MeasureDiscontentness(), 3)))

    def ResetPayoffs(self):
        for agent in self.agents:
            agent.ResetPayoff()

    def MeasureTrust(self):
        count = 0
        for agent in self.agents:
            if agent.trust:
                count += 1

        return count

    def MeasureContentness(self):
        count = 0
        for agent in self.agents:
            count += agent.content

        return count

    def MeasureDiscontentness(self):
        count = 0
        for agent in self.agents:
            count += agent.discontent

        return count

    def UpdateStrategies(self):
        # getting new strategies
        new_strategies =[]
        for i in range(len(self.agents)):
            max_connected_payoff = 0
            best_strategy = self.agents[i].trust
            for connection in self.connections[i]:
                if self.agents[connection].payoff > max_connected_payoff:
                    max_connected_payoff = self.agents[connection].payoff
                    best_strategy = self.agents[connection].trust
            new_strategies.append(best_strategy)

        # updating strategies and contentness
        for i in range(len(self.agents)):
            if self.agents[i].trust != new_strategies[i]:
                self.agents[i].trust = new_strategies[i]
                if new_strategies[i] == False:
                    self.agents[i].discontent += 1
                else:
                    self.agents[i].content += 1

    def __str__(self):
        society_str = '--- Society ---\n'
        for i in range(len(self.agents)):
            society_str += 'Agent({}) {}\n'.format(i, str(self.agents[i]))

        return society_str

if __name__ == '__main__':
    trust_data = []
    contentness_data = []
    for i in range(NUMBER_OF_SOCIETIES):
        print('===Society ({})==='.format(i))
        my_society = Society(SOCIETY_SIZE)
        my_society.RunConnectedEvolutionaryIteratedPrisonersDilemma(NUMBER_OF_GENERATIONS)
        trust_data.append(my_society.MeasureTrust()/len(my_society.agents))
        contentness_data.append(round(my_society.MeasureContentness()/my_society.MeasureDiscontentness(), 3))

    trust_data.sort()
    contentness_data.sort()
    print('\n===Simulation Complete===\n')
    print('Number of Societies Tested: {}'.format(NUMBER_OF_SOCIETIES))
    print('  Trust Data: {}'.format(trust_data))
    print('    Mean Trust Ratio: {}'.format(round(sum(trust_data)/len(trust_data), 3)))
    print('    Median Trust Ratio: {}'.format(trust_data[int(len(trust_data)/2)]))
    print('  Contentness Data: {}'.format(contentness_data))
    print('    Mean Contentness Ratio: {}'.format(round(sum(contentness_data)/len(contentness_data), 3)))
    print('    Median Contentness Ratio: {}'.format(contentness_data[int(len(contentness_data)/2)]))
