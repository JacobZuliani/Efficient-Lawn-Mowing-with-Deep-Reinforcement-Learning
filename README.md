# Efficient Lawn Mowing with Deep Reinforcement Learning

This is a client project done for Dassault Systèmes. Lawn mowing is analogous to many optimization problems such as milling for example, this is why I'm attempting to solve it.

Given any lawn shape and size how can we quickly discover the most efficient lawn mowing pattern? (assuming you're using a push mower)

### Reproducing with Docker:

To make the project as reproducible as possible I published the environment and code as a docker image available at the below link.
There are intructions in the docker hub repo on how to build the image.
https://hub.docker.com/r/jzuliani/lawn-mowing

### Environment:
The environment is the lawn.
A state of this environment consists of a matrix of three character strings
I call each string a 'tile_id' because it identifies the tile displayed at that index

To read more about tile_id's see the documentation in visualization.py

Here is an example environment state:
![](https://i.ibb.co/vxMc8cN/environment-state-example.png)

Here is an example environment state after the agent made some progress:
![](https://i.ibb.co/cChrkMw/environment-state-with-progress-example.png)

Sorry if github won't display the entire image, idk why, here's the link:
https://i.ibb.co/cChrkMw/environment-state-with-progress-example.png

### Loss Function:
I have a push mower and when I'm mowing the lawn my goal is minimize the number of pivots (when I need to lift the front wheels and turn).
The loss here is structured the same way.
Loss is equalivent to the number of moves taken by the agent, the simulation ends when the entire lawn has been mowed.
If the agent pivots it costs 1 move and does not mow any lawn because the agents location doesn't change.
This causes the agent to find a way to mow the lawn with as few pivots as possible.

### Agent:
The agent is the lawnmower.
At every timestep the lawn mower can choose one of the following actions:
- advance, move one space in the direction the mower is facing
- pivot left, rotate 90° to the left
- pivot right, rotate 90° to the right

If the agent takes an illegal action (ex. trying to mow into a wood tile) then the agents position remains the same and the cost is still one move.

The agent has the following attributes:
    position (x,y location on the lawn)
    direction (n,s,e,w the direction the mower is facing)
