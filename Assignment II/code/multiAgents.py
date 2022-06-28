# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        '''
        define max and min distances to compare with
        set them to be negative and positive infinity
        store the food dots available in the current gamestate
        '''
        pos_infinity = float("inf")
        neg_infinity = float("-inf")

        currentFood = currentGameState.getFood()

        #if the successor state is the goal state and is not a state where a ghost will be present, 
        #then return a very high value for evaluation function
        if (successorGameState.isWin() == True and newPos not in successorGameState.getGhostPositions()):
            return 9999999

        #calculate the manhattan distance between pacman and the nearest ghost
        distanceFromGhost = pos_infinity
        for ghost in successorGameState.getGhostPositions():
          dist = manhattanDistance(newPos, ghost)
          if (dist < distanceFromGhost):
            distanceFromGhost = dist
        
        #initialise the distance and use a check variable to check if distance is zero
        distanceFromFoodMin = pos_infinity       
        flag = 0
        
        #compute the manhattan distance between pacman and nearest food dot
        for food in newFood.asList():
          d = manhattanDistance(food, newPos)
          if (d < distanceFromFoodMin):
            distanceFromFoodMin = d
            flag = 1

        #if food dots are being eaten in this state, return a high function value
        foodEaten = 0
        if len(newFood.asList()) < len(currentFood.asList()):
          foodEaten = 10000

        #if the successor state has a capsule, set a high eval value
        capsuleEaten = 0
        if newPos in successorGameState.getCapsules():
          capsuleEaten = 10000
        
        #depending on how scared the ghost is and the distance from it,
        #return an appropriate number
        scared = min(newScaredTimes)
        ghostFactor = 0
        if distanceFromGhost < 3:
          #ghost is not very scared and very close to pacman
          #run!!  
          if scared < 3:
            ghostFactor = -999999
          else:
            ghostFactor = 100000

        #if the distance between pacman and the nearest food dot is not zero
        if flag == 1:
          return currentGameState.getScore() + distanceFromGhost + 1000.0 / distanceFromFoodMin + foodEaten + capsuleEaten + 2 * ghostFactor
        #if pacman is currently at a food dot
        #every term except for food distance is included
        else:
          return currentGameState.getScore() + distanceFromGhost + foodEaten + 2 * capsuleEaten + 5 * ghostFactor

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        '''
        define max and min distances to compare with
        set them to be negative and positive infinity
        store the food dots available in the current gamestate
        '''
        neg_infinity = float("-inf")
        pos_infinity = float("inf")

        #the number of ghosts is one less than the total number of agents
        #the one maxAgent being Pacman
        numGhosts = gameState.getNumAgents() - 1

        #agent 0 to represent the maxAgent, Pacman
        agent = 0

        '''
        maxValue function returns the utility value of the maxAgent
        '''
        def maxValue(gameState, depth, evalFunction):
            #increase depth to current depth
            depth += 1
            #if the current state is not a terminal state or goal state
            if (gameState.isWin() == False and gameState.isLose() == False and depth != self.depth): 
                #initlialise the max utility to be negative infinity
                maxvalue = neg_infinity
                tempMin = pos_infinity
                #compute the utility for all the successor states
                #and return the maximum utility
                for action in gameState.getLegalActions(0):
                    successor = gameState.generateSuccessor(0, action)
                    tempMin = minValue(successor, depth, 1, evalFunction)
                    if (maxvalue < tempMin):
                        maxvalue = tempMin
                #return the maximum utility with respect to Pacman
                return maxvalue

            #if the current state is a terminal state or goal state
            return evalFunction(gameState)
        
        #the ghosts are the minAgents
        #the function returns the utility value of the minAgent
        def minValue(gameState, depth, agentIndex, evalFunction):
            #if the current state is not a terminal state or goal state
            if (gameState.isWin()  == False and gameState.isLose() == False):  
                #initlialise the min utility to be positiive infinity
                minvalue = pos_infinity
                #compute the utility for all the successor states
                #and return the minimum utility
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    #if it is the terminal ghost agent, the next agent is Pacman
                    if agentIndex == (numGhosts):
                        minvalue = min(minvalue, maxValue(successor, depth, evalFunction))
                    #otherwise the next agent is also a ghost
                    else:
                        minvalue = min(minvalue, minValue(successor, depth, agentIndex + 1, evalFunction))
                #return the max utility with respect to the ghosts
                return minvalue

            #if the current state is a terminal state or goal state
            return evalFunction(gameState)
        
        #initiliasing the problem for the maxAgent at the first state
        #store the successors of the state in a list
        #the fields of which include the successor state and the action
        successors = []
        for action in gameState.getLegalActions(agent):
            succ = gameState.generateSuccessor(agent, action)
            successors.append((action, succ))

        #initialise the utility value and the optimal action
        utility = neg_infinity
        optAction = "default"
        minAgent = 1
        #compute the utility for all the successor states
        #and return the action corresponding to the maximum utility 
        for successor in successors:
            temp = minValue(successor[1], 0, minAgent, self.evaluationFunction)
            if temp > utility:
              optAction = successor[0]
              utility = temp
              # print(bestAction)
        return optAction
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        '''
        define max and min distances to compare with
        set them to be negative and positive infinity
        store the food dots available in the current gamestate
        '''
        neg_infinity = float("-inf")
        pos_infinity = float("inf")

        #the number of ghosts is one less than the total number of agents
        #the one maxAgent being Pacman
        numGhosts = gameState.getNumAgents() - 1

        #agent 0 to represent the maxAgent, Pacman
        agent = 0

        #maxValue function returns the utility value of the maxAgent
        def maxValue(gameState, depth, alpha, beta, evalFunction):
            #increase depth to current depth
            depth += 1
            #if the current state is not a terminal state or goal state
            if (gameState.isWin() == False and gameState.isLose() == False and depth != self.depth): 
                #initlialise the max utility to be negative infinity
                maxvalue = neg_infinity
                #compute the utility for all the successor states
                #and return the maximum utility
                for action in gameState.getLegalActions(0):
                    successor = gameState.generateSuccessor(0, action)
                    temp = minValue(successor, depth, 1, alpha, beta, evalFunction)
                    if (temp > maxvalue):
                        maxvalue = temp
                    #if the max possible utility of the other successor state is lesser,
                    #then we can return the present max value
                    if (maxvalue > beta):
                        return maxvalue
                        #if not, update the alpha value
                    if (maxvalue > alpha):
                        alpha = maxvalue

                #return the maximum utility with respect to Pacman
                return maxvalue

            #if the current state is a terminal state or goal state
            return evalFunction(gameState)
        
        #the ghosts are the minAgents
        #the function returns the utility value of the minAgent
        def minValue(gameState, depth, agentIndex, alpha, beta, evalFunction):
            #initlialise the min utility to be positiive infinity
            minvalue = pos_infinity
            #if the current state is not a terminal state or goal state
            if (gameState.isWin() == False and gameState.isLose() == False): 
                #compute the utility for all the successor states
                #and return the minimum utility
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    #if it is the terminal ghost agent, the next agent is Pacman
                    if (agentIndex == numGhosts):
                        minvalue = min (minvalue, maxValue(successor, depth, alpha, beta, evalFunction))
                        #return the minvalue if the next tree can be pruned
                        if (minvalue < alpha):
                            return minvalue
                    #otherwise the next agent is also a ghost
                    else:
                        minvalue = min(minvalue, minValue(successor, depth, agentIndex + 1 ,alpha, beta, evalFunction))
                        if (minvalue < alpha):
                            return minvalue
                    #otherwise update beta
                    beta = min(beta, minvalue)

                #return the max utility with respect to the ghosts
                return minvalue

            #if the current state is a terminal state or goal state
            return evalFunction(gameState)

        #initiliasing the problem for the maxAgent at the first state
        #store the successors of the state in a list
        #the fields of which include the successor state and the action
        #initialise the utility value and the optimal action
        currentScore = neg_infinity
        optAction = "default"
        alpha = neg_infinity
        beta = pos_infinity

        successors = []
        for action in gameState.getLegalActions(agent):
            succ = gameState.generateSuccessor(agent, action)
            successors.append((action, succ))

        #compute the utility for all the successor states
        #and return the action corresponding to the maximum utility 
        for successor in successors:
            score = minValue(successor[1], agent, 1, alpha, beta, self.evaluationFunction)
            # Choosing the action which is Maximum of the successors.
            if (score > currentScore):
                optAction = successor[0]
                currentScore = score
            #update alpha beta values at the root   
            if (score > beta):
                return optAction
            if (score > alpha):
                alpha = score
        return optAction
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        '''
        define max and min distances to compare with
        set them to be negative and positive infinity
        store the food dots available in the current gamestate
        '''
        neg_infinity = float("-inf")
        pos_infinity = float("inf")

        #the number of ghosts is one less than the total number of agents
        #the one maxAgent being Pacman
        numGhosts = gameState.getNumAgents() - 1

        #agent 0 to represent the maxAgent, Pacman
        agent = 0

        #maxValue function returns the utility value of the maxAgent
        def maxValue(gameState, depth, evalFunction):
            #increase depth to current depth
            depth += 1
            #if the current state is not a terminal state or goal state
            if (gameState.isWin() == False and gameState.isLose() == False and depth != self.depth):
                #initlialise the max utility to be negative infinity  
                maxvalue = neg_infinity
                tempExpect = 0
                #compute the utility for all the successor states
                #and return the maximum utility
                for action in gameState.getLegalActions(0):
                    successor = gameState.generateSuccessor(0, action)
                    tempExpect = expectValue(successor, depth, 1, evalFunction)
                    #fint the max expect value
                    if (tempExpect > maxvalue):
                        maxvalue = tempExpect

                #return the maximum utility with respect to Pacman
                return maxvalue

            #if the current state is a terminal state or goal state    
            return evalFunction(gameState)
        
        #the ghosts are the minAgents
        #the function returns the expect value
        def expectValue(gameState, depth, agentIndex, evalFunction):
            #if the current state is not a terminal state or goal state
            if (gameState.isWin() == False and gameState.isLose() == False): 
                #initlialise the expected value
                totalexpectedvalue = 0.00
                actions = gameState.getLegalActions(agentIndex)
                numActions = len(actions) + 0.00
                if (len(actions) != 0):
                    #compute the utility for all the successor states
                    #and return the expected utility
                    for action in actions:
                        successor = gameState.generateSuccessor(agentIndex, action)
                        #if the next agent is a ghost, ragain return the expected value
                        if (agentIndex != numGhosts):
                            expectedvalue = expectValue(successor, depth, agentIndex + 1, evalFunction)
                        else:
                            #if the next agent is pacman, return the max value
                            expectedvalue = maxValue(successor, depth, evalFunction)
                        #compute the total expected value of all the successor states
                        totalexpectedvalue += expectedvalue
                    return totalexpectedvalue / numActions
                return 0

            #if the current state is a terminal state or goal state
            return evalFunction(gameState)

        #initiliasing the problem for the maxAgent at the first state
        #store the successors of the state in a list
        #the fields of which include the successor state and the action
        #initialise the utility value and the optimal action
        successors = []
        for action in gameState.getLegalActions(agent):
            succ = gameState.generateSuccessor(agent, action)
            successors.append((action, succ))

        utility = neg_infinity
        optAction = "default"
        minAgent = 1

        #compute the utility for all the successor states
        #and return the action corresponding to the maximum utility
        for successor in successors:
            temp = expectValue(successor[1], 0, minAgent, self.evaluationFunction)
            if temp > utility:
              optAction = successor[0]
              utility = temp
              
        return optAction
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currentFood = currentGameState.getFood()
    currentPosition = currentGameState.getPacmanPosition()
    numCapsules = len(currentGameState.getCapsules()) # Keep total capsules
    
    #initiliase the evaluation function value to be returned
    finalScore = 0 

    #calculate the manhattan distance of Pacman from all the food dots 
    #store these in a list
    foodDistances = []
    for food in currentFood.asList():
        foodDistances.append(manhattanDistance(currentPosition, food))

    #food dots that are close to pacman arent good,
    #since Pacman has to eat them
    for dist in foodDistances:
        #penalise the closer dots by reducing the return value
        if dist < 50:
            finalScore += -3 * dist
        else:
            finalScore += -0.5 * dist

    #compute the distance of pacman from the ghosts
    #ghosts that are scared aren't good for Pacman, since Pacman has 
    #to eat them, penalise the scared ghosts
    #and reard the non scared ghosts
    ghostDistances = []
    for ghost in currentGameState.getGhostStates():
        dist = manhattanDistance(currentPosition, ghost.getPosition())
        if (ghost.scaredTimer > 0):
            ghostDistances.append(-dist)
        else:
            ghostDistances.append(dist)

    #ghosts that have negative distances are scared ghosts
    for d in ghostDistances:
        #penalise the non scared ghosts according to their distance
        if (d > 0 and d < 3):
            finalScore += 7 * d
        elif (d > 0 and d < 7):
            finalScore += 3 * d
        elif (d > 0):
            finalScore += 0.5 * d
        #heavily penalise the scared ghosts
        elif (d <= 0 and d > -3):
            finalScore += 25 * d
        else:
            finalScore += 15 * d

    #more the number of capsules, the worse the situation since pacman has to eat all of them
    #more the number of food dots, the worse, since pacman is far from its goal state
    #higher the current game score the better for Pacman, hence a positive multiplier
    return finalScore + -400 * numCapsules + -200 * len(currentFood.asList()) + 500 * currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
