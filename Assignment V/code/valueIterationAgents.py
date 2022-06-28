# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
import copy

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        neg_infinity = float("-inf")
        states = self.mdp.getStates()
        for iteration in range(self.iterations):
            #initialise an empty disctionary
            val = self.values.copy()
            #find the best action
            for state in states:
                maxVal = neg_infinity
                vals = []
                #if the current state is not a terminal state
                if self.mdp.isTerminal(state) == False:
                    vals = [self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)]
                    #find the best action after iterating over all the actions
                    #compare with the previous best action
                    for value in vals:
                        maxVal = max(value, maxVal)
                    val[state] = maxVal
            #record the dictionary of optimum actions
            self.values = val

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        return_val = 0.0
        #tuple of transition probability and next state
        transitionStates_and_prob = self.mdp.getTransitionStatesAndProbs(state, action)
        for state_prob in transitionStates_and_prob:
            #use the given discount to compute the discounted value to be added
            discounted_val = self.mdp.getReward(state, action, state_prob[0]) + self.discount * self.getValue(state_prob[0])
            #find the final value using the transition probability
            return_val += state_prob[1] * discounted_val
        #return the computed Q value
        return return_val
        
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        neg_infinity = float("-inf")
        #create an initialised dictionary
        store_actions =  util.Counter()

        actions = self.mdp.getPossibleActions(state)
        #from the list of possible actions
        for act in actions:
            #populate the dictionary with those values
            #corresponding to each action
            value = self.getQValue(state, act)
            store_actions[act] = value

        max_action = None
        max_val = neg_infinity
        #return the action that maximises the value
        for key in store_actions.keys():
            if store_actions[key] > max_val:
                max_action = key
                max_val = store_actions[max_action]
        return max_action

        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
