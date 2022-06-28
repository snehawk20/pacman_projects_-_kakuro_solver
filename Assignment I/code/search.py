# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    '''
    create lists to store the visited nodes,
    the successor of every node, and the current path
    '''
    visited = []              
    successor_data = [] 
    path = []

    '''
    create stacks for both the frontier list
    and the path list
    stack is a LIFO date structure
    '''
    path_list = util.Stack() 
    frontier_list = util.Stack() 

    '''
    problem.getStartState() returns the coordinates of the start state
    current_state = (x, y), is a tuple
    if the einitial state is a goal state, return an empty list
    '''
    current_state =  problem.getStartState()
    if (problem.isGoalState(current_state) == True):
        return path
    '''
    keep running the following loop until 
    the goal state is found, or 
    the entire search space has been searched, but no goal was found
    in the former return the path prom the initial state of the final goal state
    in the latter case return an empty list
    '''
    while (1):
        '''
        we do not want nodes that have already been expanded to be searched again
        hence we won't pick nodes that are in the visited list
        problem.getSuccessors() returns a list containing
        as many tuples as there are successors
        each tuple contains the coordinates of the child node, the direction, 
        and the cost of the move
        '''
        if (current_state not in visited):
            successor_data = problem.getSuccessors(current_state)

            '''
            write the children nodes (coordinates) and their 
            respective direction into two separate lists
            '''
            children = [item[0] for item in successor_data]
            route = [item[1] for item in successor_data]

            '''
            push the children into the frontier list
            and push the corresponding direction into the path list
            '''
            for i in range(len(successor_data)):
                path_list.push(path + [route[i]])
                frontier_list.push(children[i])

            #push the visited node into the explored list
            visited.append(current_state)

        #if the frontier is not empty, pop a node
        if (frontier_list.isEmpty() == True):
            return []
        else:
            current_state = frontier_list.pop()

        #pop a path from the path list too
        if (path_list.isEmpty() == False):
            path = path_list.pop()
        else:
            sys.exit("Path list empty")

        '''
        if the current state is the goal state return the path
        this path gives directions from the current state to the goal state found
        '''
        if (problem.isGoalState(current_state) == True):
            return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    '''
    create lists to store the visited nodes,
    the successor of every node, and the current path
    '''
    visited = []              
    successor_data = [] 
    path = []

    '''
    create queues for both the frontier list
    and the path list
    queue is a FIFO date structure
    '''
    path_list = util.Queue() 
    frontier_list = util.Queue() 

    '''
    problem.getStartState() returns the coordinates of the start state
    current_state = (x, y), is a tuple
    if the einitial state is a goal state, return an empty list
    '''
    current_state =  problem.getStartState()
    if (problem.isGoalState(current_state) == True):
        return path
    '''
    keep running the following loop until 
    the goal state is found, or 
    the entire search space has been searched, but no goal was found
    in the former return the path prom the initial state of the final goal state
    in the latter case return an empty list
    '''
    while (1):
        '''
        we do not want nodes that have already been expanded to be searched again
        hence we won't pick nodes that are in the visited list
        problem.getSuccessors() returns a list containing
        as many tuples as there are successors
        each tuple contains the coordinates of the child node, the direction, 
        and the cost of the move
        '''
        if (current_state not in visited):
            successor_data = problem.getSuccessors(current_state)

            '''
            write the children nodes (coordinates) and their 
            respective direction into two separate lists
            '''
            children = [item[0] for item in successor_data]
            route = [item[1] for item in successor_data]

            #push the visited node into the explored list
            visited.append(current_state)

            '''
            push the children into the frontier list
            and push the corresponding direction into the path list
            '''
            for i in range(len(successor_data)):
                path_list.push(path + [route[i]])
                frontier_list.push(children[i])

        #if the frontier is not empty, pop a node
        if (frontier_list.isEmpty() == True):
            return []
        else:
            current_state = frontier_list.pop()

        #pop a path from the path list too
        if (path_list.isEmpty() == False):
            path = path_list.pop()
        else:
            sys.exit("Path list empty")

        '''
        if the current state is the goal state return the path
        this path gives directions from the current state to the goal state found
        '''
        if (problem.isGoalState(current_state) == True):
            return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    '''
    create lists to store the visited nodes,
    the successor of every node, and the current path
    '''
    visited = []              
    successor_data = [] 
    path = []

    '''
    create prority queues for both the frontier list
    and the path list
    this is a heap like data structure
    '''
    path_list = util.PriorityQueue() 
    frontier_list = util.PriorityQueue() 

    '''
    problem.getStartState() returns the coordinates of the start state
    current_state = (x, y), is a tuple
    if the einitial state is a goal state, return an empty list
    '''
    current_state =  problem.getStartState()
    if (problem.isGoalState(current_state) == True):
        return path

    '''
    keep running the following loop until 
    the goal state is found, or 
    the entire search space has been searched, but no goal was found
    in the former return the path prom the initial state of the final goal state
    in the latter case return an empty list
    '''

    while (1):
        '''
        we do not want nodes that have already been expanded to be searched again
        hence we won't pick nodes that are in the visited list
        problem.getSuccessors() returns a list containing
        as many tuples as there are successors
        each tuple contains the coordinates of the child node, the direction, 
        and the cost of the move
        '''
        if (current_state not in visited):
            successor_data = problem.getSuccessors(current_state)

            '''
            write the children nodes (coordinates) and their 
            respective direction into two separate lists
            '''
            children = [item[0] for item in successor_data]
            route = [item[1] for item in successor_data]

            #push the visited node into the explored list
            visited.append(current_state)

            '''
            push the children into the frontier list
            and push the corresponding direction  and cost into the path list
            '''
            for i in range(len(successor_data)):
                cost = problem.getCostOfActions(path + [route[i]])
                path_list.push(path + [route[i]], cost)
                frontier_list.push(children[i], cost)

        #if the frontier is not empty, pop a node
        if (frontier_list.isEmpty() == True):
            return []
        else:
            current_state = frontier_list.pop()

        #pop a path from the path list too
        if (path_list.isEmpty() == False):
            path = path_list.pop()
        else:
            sys.exit("Path list empty")

        '''
        if the current state is the goal state return the path
        this path gives directions from the current state to the goal state found
        '''
        if (problem.isGoalState(current_state) == True):
            return path
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    '''
    create lists to store the visited nodes,
    the successor of every node, and the current path
    '''
    visited = []              
    successor_data = [] 
    path = []

    '''
    create prority queues for both the frontier list
    and the path list
    this is a heap like data structure
    '''
    path_list = util.PriorityQueue() 
    frontier_list = util.PriorityQueue() 

    '''
    problem.getStartState() returns the coordinates of the start state
    current_state = (x, y), is a tuple
    if the einitial state is a goal state, return an empty list
    '''
    current_state =  problem.getStartState()
    if (problem.isGoalState(current_state) == True):
        return path

    '''
    keep running the following loop until 
    the goal state is found, or 
    the entire search space has been searched, but no goal was found
    in the former return the path prom the initial state of the final goal state
    in the latter case return an empty list
    '''
    while (1):
        '''
        we do not want nodes that have already been expanded to be searched again
        hence we won't pick nodes that are in the visited list
        problem.getSuccessors() returns a list containing
        as many tuples as there are successors
        each tuple contains the coordinates of the child node, the direction, 
        and the cost of the move
        '''
        if (current_state not in visited):
            successor_data = problem.getSuccessors(current_state)

            '''
            write the children nodes (coordinates) and their 
            respective direction into two separate lists
            '''
            children = [item[0] for item in successor_data]
            route = [item[1] for item in successor_data]

            #push the visited node into the explored list
            visited.append(current_state)

            '''
            push the children into the frontier list
            and push the corresponding direction and heuristic into the path list
            '''
            for i in range(len(successor_data)):
                cost = problem.getCostOfActions(path + [route[i]]) + heuristic(children[i], problem)
                path_list.push(path + [route[i]], cost)
                frontier_list.push(children[i], cost)

        #if the frontier is not empty, pop a node
        if (frontier_list.isEmpty() == True):
            return []
        else:
            current_state = frontier_list.pop()

        #pop a path from the path list too
        if (path_list.isEmpty() == False):
            path = path_list.pop()
        else:
            sys.exit("Path list empty")

        '''
        if the current state is the goal state return the path
        this path gives directions from the current state to the goal state found
        '''
        if (problem.isGoalState(current_state) == True):
            return path

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
