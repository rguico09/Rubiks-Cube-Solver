# Current Algorithms
One of the easiest ways is to model the way humans solve the cube
- this works, but is not the most efficient way to solve the cube, given it takes a human 60 to 200 moves to solve a cube depending on their method of choice

Knowing that any cube can be solved in about 20 moves, there must be a better approach

## Neural Networks
> Neural networks are modeled after the human brain.

They work by going through a series of training phases called epochs
- each iteration updates weights on a node in a network at a specified learning rate to make it produce the expected value

1. Trying to solve a rubik's cube using a NN tends to be difficult since there is a large state space with only 1 correct solution
	- this means the NN will have a tough time knowing how to update the states since randomly doing moves will not likely stumble upon the solved cube state
	- one way to improve the performance of a NN is by the use of boosting using weak learners

	NNs can be combined with other algorithms to make a powerful solver
	- `DeepCubeA` "works by using approximate value iteration to train a deep NN (DNN) to approximate a function that outputs the cost to reach the goal (aka the cost-to-go function)"
		- this DNN is then combined with an A* search algorithm to help approximate and compare the values of various cube states while searching for a solution

2. Another group used a NN to help improve their solving algorithm by swapping between 2 different algorithms
	- they called their method `Approximate Policy Iteration` (API)

	The API "algorithms iterate between two policies: a slow policy (tree search) and a fast policy (a NN)"
	- by doing this, they were able to use the perks of both a search tree and a NN to train and build an accurate model

3. Another option is to give the NN easier training data in the beginning

	An example of this would be to give it cubes that have only been scrambled with 3 moves instead of 1000 moves
	- this will allow the NN to be trained at a much faster rate

	As the NN becomes more proficient at solving cubes in an easier state, we can increase the difficulty by training on cubes that have more scramble moves applied

> [!help] This also helps overcome the problem of there being a sparse reward in a large state space.

## A*
A* is a popular heuristic search algorithm that seeks to find the smallest cost, or shortest path, to a given goal node (the solved cube, in this case)

$$
f(n) = g(n) + h(n)
$$

This function helps the search algorithm determine which node to advance to
- this is applied to all the available nodes from the given starting node

$$
\begin{align}
 & N = \text{the next node on the path} \\
 & g(n) = \text{the cost of the path from the start node} \\
 & h(n) = \text{a heuristic that estimates the cost of the cheapest path from n to the goal}
\end{align}
$$

The algorithm chooses to advance to the ndoe that produces the lowest $f(n)$

> [!warning] Also important to note if it is not possible to extend the path, or it has reached some terminating state, then it goes back to the starting node and chooses the next minimum $f(n)$ value.

This algorithm is memory intensive since it has to store all the nodes it uses in its memory
- similar to the NN, it works well if combined with another algorithm technique

## Korf's / Iterative Deepening A*
> Korf's algorithm can find an optimal solution to solving a Rubiks' cube

The algorithm uses `"iterative-deepening-A* (IDA*), with a lower bound heuristic function based on large memory-based lookup tables, or pattern databases."`

This method uses the A* algorithm previously discussed but it can improve the searching with the pattern databases
- these pattern databases `"store the exact number of moves required to solve various subgoals of the problem"`

This technique allows this algorithm to solve the cube in the optimal number of moves, but this comes with the trade-off of time

> [!quote] "Korf's algorithm will always find the optimal solution from any given starting state; but, since it's a heuristic tree search, it will often have to explore many different states and it will take a long time to compute a solution."

Finding better ways to hash the cube will help minimise the amount of memory required to store all the cube states in the pattern database

## Kociemba / 2-Phase Algorithm
1. The first phase puts pieces into the correct position but doesn't change the orientation of any of the corners or edges
	- done by restricting the moves to only a small set of moves (`U, D, B2, F2, L2, R2`)
	- once this phase finds `"the shortest number of moves required to do this, it continues until it has a large enough supply of possible solutions ranging from the lowest number of moves to a much lagrer number"`

2. Advancing on to the second phase once all the permutations are restored, the algorithm searches for an optimal solution
	- this is not an optimal solution of the second phase, but rather an optimal solution of combining the moves of phase 1
	
	An example of this is given by `Ruwix`
	- they state `"for example, an 8 move phase 1 followed by a 15 move phase 2 is less optimal than a 10 move phase 1 followed by a 5 move phase 2"`

Because the 2 phases break the problem into smaller problems, multiple solutions can be found very quickly for each step and combined to make the most favourable solution

> [!quote] "This algorithm relies on human domain knowledge of the group theory of the Rubik's cube. Kociemba will always solve any cube given to it, and it runs very quickly."
