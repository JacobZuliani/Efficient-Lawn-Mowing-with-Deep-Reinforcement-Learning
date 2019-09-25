# Efficient-Lawn-Mowing-with-Deep-Reinforcement-Learning

This is a client project done for Dassault Systèmes. The lawn mowing problem I present here is analogous to the problem faced by Dassault.

Given any lawn shape and size how can we quickly discover the most efficient lawn mowing pattern? (assuming you're using a push mower)

Environment:
The environment is the lawn.
A state of this environment consists of a 2d matrix where:
    0 represents un-mowed lawn
    1 represents a space the mower cannot occupy, (ex. house, trees, etc.)
    2 represents a space that can be occupied but not mowed, (ex. driveway)
    3 represents mowed lawn
    4 represents the mower
    
(add picture)

Loss Function:
I have a push mower and when I'm mowing the lawn my goal is minimize the number of pivots (when I need to lift the front wheels and turn).
The loss here is structured the same way.
Loss is equalivent to the number of moves taken by the agent, the simulation ends when the entire lawn has been mowed.
If the agent pivots it costs 1 move and does not mow any lawn because the agents location doesn't change.
This causes the agent to find a way to mow the lawn with as few pivots as possible.
s
Agent:
The agent is the lawnmower.
At every timestep the lawn mower can choose one of the following actions:
    advance, move one space in the direction the mower is facing
    pivot left, rotate 90° to the left
    pivot right, rotate 90° to the right
    sweep 1
    sweep 2
    sweep 3
    sweep 4
A sweep is a long turn that is discounted (it's easier to take a long sweeping turn than it is to take a short pivot).
Where the turn below would normally take 7 moves, the agent can take this move at a cost of 5 because it's easier for a human to take this turn than a sharp pivot.

(add picture)

The larger the sweeping turn the higher the discount.

(add picture)

If the agent takes an illegal action (ex. trying to mow into a house) the move cost is 2.

The agent has the following attributes:
    position (x,y location on the lawn)
    direction (n,s,e,w the direction the mower is facing)
    
Result Visualization:
To visualize the pattern the agent took to mow the lawn, the simulation maintains a second 2d matrix where:
    0 represents un-mowed lawn
    1 represents a space the mower cannot occupy, (ex. house, trees, etc.)
    2 represents a space that can be occupied but not mowed, (ex. driveway)
    3-6 represents mowed lawn where the mower did not change direction, the number on the mowed surface represents the direction in which it has been mowed
    3 = north
    4 = south
    5 = east
    6 = west
    7-10 represents mowed lawn where the mower also changed direction
    7 = north to west, or east to south
    8 = north to east, or west to south
    9 = south to west, or east to north
    10 = south to east, or west to north

Given this matrix I can construct a clear visualization of the path the agent took to mow the entire lawn.
I plan to do this by placing images at each index of the matrix.
Recording this matrix at each timestep allows me to create an animation of the lawn being mowed by the agent.
