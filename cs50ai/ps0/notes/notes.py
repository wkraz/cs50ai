"""
NOTES
--------------
Search
    search algorithms are how AI looks through a ton of data and determines the most optimal choice
        tic-tac-toe moves, driving directions, etc
    agent - entity that perceives environment and acts upon it
    state - configuration of an agent in its environment (arrangement of pieces in slide puzzle)
    actions - choices that can be made in a state
        function: action(state)
        takes state as input and returns output of every possible action in that state
    transition model - function that takes inputs: state, action and outputs the state after doing the action
    state space - the set of all possible states that can be reached from the initial state with the allowed actions
        can be represented with node graph: nodes = states, arrows = actions
    goal test - way to check if we've reached our goal or not yet
    path cost function - how "expensive" each course of action is
        looking for optimal solution
    to track this we use the node data type a bunch
        keeps track of state, parent node, the action the parent used to generate it, and path cost (from initial to current)
    solving search problem approach:
        start w/ frontier that contains initial state
        repeat:
            if frontier is empty, there is no solution
            remove a node from the frontier
            if this node is the goal state, return the solution
            expand the node (look at all possible actions from current state)
    however, this can cause an infinite loop if you go back in forth from ones you've explored already
    revised approach:
        start w/ frontier that is initial state
        create empty explored set
        repeat:
            if frontier is empty, no solution
            remove a node from frontier
            if this node is goal state, return solution
            add this node to explored set
            expand node and add all nodes not in explored set or frontier to frontier
    
    depth first search
        utilizes a stack (last in, first out)
        basically, pick a node and keep going down the line 
            for example, pick the leftmost node from each parent and stop once you reach the bottom
    
    breadth first search
        uses a queue (fifo)
        explores all the children before moving onto grandchildren
    
    OOP is very important for search algorithms -- in code below
    dfs and bfs are uninformed search -- they have no outside knowledge about the task at hand
    greedy breadth first search -- informed search
        in a maze, it knows the location of the end goal so it bases its choices off moving closer towards it
        algorithm that expands the node closest to the goal, estimated by heuristic function h(n)
    
    A* search
        search algorithm that expands node with lowest value of g(n) + h(n)
            h(n) is heuristic function that estimates cost to reach goal
            g(n) is the cost to reach the node 
        when you start going down a "wrong path" g(n) will grow and you will look at potentially better paths instead
    
    Minimax
        used when you have to account for an opponent making moves against you (games)
        in tic-tac-toe you can assign values: -1 = O wins, 0 = tie, 1 = X wins (as X)
            now, the computer understands what winning vs losing is
            O wants to minimize score, X wants to maximize score
        Setting up tic tac toe game
            s: state
            player(s): returns which player's turn it is to move in state s
            action(s): legal moves in state s
            result(s, a): returns state after taking action a in state s
            terminal(s): checks if the game is over
            utility(s): returns numerical value (1, 0, -1) after the game ends (who won)
        Recursive algorithm (playing as X)
            goes through all moves for X
                in each move, goes through all moves for O
                    in each O move, goes through each X...
                    until it reaches terminal state and looks at result to minimax
            goes down to base state, and base O's moves off whatever moves minimize their score
            Then maximize your move and continue until you reach the current state, and choose optimal node
        Given a state s, MAX returns action a in action(s) that produces highest value of min-value(result(s, a))
        Same thing for MIN but with max-value(result(s, a))
        implementing max-value(state)
        function max-value(state):
            if terminal(state):
                return utility(state)
            v = -INFINITY # this is the minimum value that you will constantly trying to beat (so you pick the smallest number)
            for action in actions(state):
                v = max(v, min-value(result(state, action))) # recursively calls min-value, which recursively calls max-value
            return v
        function min-value(state): is the same exact thing but setting v = INFINITY and swapping max and min
        notice how this can take veryyyyyy long -- important to optimize
        alpha-beta pruning
            if you have a long search tree, you don't have to look at everything
                you are max and one of your choices is 4, every node with any children below 4 you can scrap
        depth-limited minimax
            at a certain point, you draw the line and stop looking "10 moves deep"
                saves computational power
            contains evaluation function
                estimates the expected utility of the game from a given state


"""
import sys 

# solving maze using dfs/bfs 

# making node class
class Node():
    # defining traits of a node (note we're leaving out the path cost in this b/c it's calculated at the end)
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
    
# dfs - stack
class StackFrontier():
    # creates an initial frontier - empty list
    def __init__(self):
        self.frontier = []
    
    # adds a node to the end of the list
    def add(self, node):
        self.frontier.append(node)
    
    # checks if the function contains a particular state
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    # checks if frontier is empty, if returns true then no solution
    def empty(self):
        return len(self.frontier) == 0
    
    # removing something from the frontier (last element), need to make sure it's not empty first
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1] # gets last item in list
            self.frontier = self.frontier[:-1] # removes that node
            return node
        
# bfs - queue
class QueueFrontier(StackFrontier): # inherits from stack frontier
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] # first element instead of last like in stack
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
    
    def solve(self):
        """Looks for solution to maze if it exists"""
        # pretend all the functions called have been defined

        # keep track of how many states have been explored
        self.num_explored = 0

        # initialize frontier to starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # initialize an empty explored set
        self.explored = set()

        # keep looping until solution found
        while True:

            if frontier.empty(): # if nothing in frontier, no path
                raise Exception("no solution")
            # choose node from frontier
            node = frontier.remove()
            self.num_explored += 1

            # see if node is goal
            # if it is, then we want to backtrack and see what actions we took to get there
            if node.state == self.goal:
                actions = []
                cells = []

                # follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                # they are in reverse chronological order, so reverse it to see what was first
                actions.reverse()
                cells.reverse()

                self.solution = (actions, cells)
                return 
            
            # not the goal, so mark it as explored
            self.explored.add(node.state)

            # add neighbors to frontier
            for action, state in self.neighbors(node.state): # look at all our neighbors
                if not frontier.contains_state(state) and state not in self.explored: # checking if state is in frontier or been explored
                    child = Node(state=state, parent=node, action=action) # add new child node whose parent is the node
                    frontier.add(child)
    
