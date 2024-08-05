"""
NOTES
Optimization
--------------

local search - search algorithm that maintains a single node and searches by moving to a neighboring node
    useful when we don't care about the path it takes to get to a goal, but when we want to actually know what the goal is

state-space landscape
    chart of vertical bars that represent potential states in a world
    height is measured by an objective function 
        we want to find the maximum/minimum in this graph
        usually want to minimize a cost function
    neighbors are the bars next to each bar
    in local search you just go through this chart
    hill climbing - when looking at your neighbors, pick the one that optimizes what you're looking for
        only gives you local extrema, not global

simulated annealing - a way to find absolute extrema instead of local extrema like hill climbing
    idea: sometimes we want to make the wrong move so that we can find the absolute max/min
    early on, make more bad moves, later on make less bad moves b/c we're more likely to have found global extrema

function simulated-annealing(problem, max):
    current = initial state of problem
    for t = 1 to max:
        T = temperature(t)
        neighbor = random neighbor of current
        E = how much better neighbor is than current
        if E > 0:
            current = neighbor
        with probability e^(E/T) set current = neighbor
        
linear programming
    minimizing a cost function c1x1 + c2x2 ... + cnxn
    with constraints a1x1 + a2x2 ... + anxn <= b or = b

constraint satisfaction - making a node graph that connects each constraint that relies on each other

arc consistency - when do nodes depend on each other, make sure they don't conflict
    function AC-3(csp): # function that handles arc consistency (csp = constraint satisfaction problem)
        queue = all arcs in csp
        while queue is not empty:
            (x, y) = dequeue(queue) # want to make x arc consistent with y
            if revise(csp, x, y): # returns true if you end up removing something from x's domain to make room for y
                if size of x.domain == 0:
                    return false
                for each z in x.neighbors - {y}:
                    enqueue(queue, (z, x)) # add back queues to arc
        return true
                
backtracking search 
    idea: if we ever get stuck, we can just backtrack and try something else
    function backtrack(assignment, csp):
        if assignment complete: return assignment
        var = select-unassigned-var(assignment, csp)
        for value in domain-values(var, assignment, csp):
            if value consistent with assignment:
                add {var = value} to assignment
                result = backtrack(assignment, csp) # recursive call
                if result is not failure: return result
            remove {var = value} from assignment # if it doesn't work, then backtrack and try another variable
        return failure
    # basically, take a variable and look at every possible value and backtrack until it satisfies all constraints
    kind of like what you do in sudoku by just picking a value for a variable that works and seeing if problems arise
    in other variables that depend on it -- if so, backtrack and try a new value there


"""
