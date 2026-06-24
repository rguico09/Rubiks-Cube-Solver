# Kociemba's Algorithm
## Two Phase Approach
### Two-Phase
The core of the 2-phase approach is:
- solve the cube into a state with a certain property
- solve the rest of the cube

If we select `F2L` as our property, we get:
- solve the first 2 layers
- solve the last layer
	- if we solve F2L with the fewest moves possible, then solve the resulting LL case optimally, we'll end up with a decently short solution
	- however, there might be a shorter solution: in that case, the first phase might take more moves, but get us an easy LL case

### Iterative Deepening (for Phase 1)
Let's say our first solution took 15 moves for F2L and 11 moves for LL
- that means our cube takes at most `15 + 11 = 26` moves to solve

So let's try looking at all the solutions that take 15 moves for F2L
- if any of them give us an LL that takes fewer than 11 moves, we can find a shorter solution
- in fact, we can extend this and keep looking

> [!answer] Here's our plan:
> - try all the solutions that take 15 moves for F2L and fewer than 26 - 15 = 11 moves for LL.
> - try all the solutions that take 16 moves for F2L and fewer than 26 - 16 = 10 moves for LL.
> - try all the solutions that take 17 moves for F2L and fewer than 26 - 17 = 9 moves for LL.
> - ...
> - try all the solutions that take 25 moves for F2L and fewer than 26 - 25 = 1 moves for LL.
> - try all the solutions that take 26 moves for F2L and fewer than 26 - 26 = 0 moves for LL.

If there's a solution that takes fewer than 26 moves for the entire cube, F2L clearly has to be finished in at most 26 moves
- therefore, our optimal overall solution has to be in one of these cases

Now let's say that along the way we find a solution that takes 17 moves for F2L and 8 moves for LL
- now we know that the entire cube can be solved in `17 + 8 = 25` moves
- we abort the original 26-plan and continue our search with a new upper bound

> [!answer] Here's our plan:
> - try all the solutions that take 17 moves for F2L and fewer than 25 - 17 = 8 moves for LL.
> - try all the solutions that take 18 moves for F2L and fewer than 25 - 18 = 7 moves for LL.
> - ...
> - try all the solutions that take 25 moves for F2L and fewer than 25 - 25 = 0 moves for LL.

In principle, we can run Kociemba's 2-phase algorithm until it finds a phase 1 suboptimal solution for which the phase 2 solution has length 0
- in this case, we have found the optimal solution – but this isn't the intention of the algorithm
- usually, we just run it until the desired total length (`phase 1 length + phase 2 length`) is below a certain threshold, but without any guarantee that the solution found is optimal

## The Domino Phase
Of course, Kociemba's algorithm doesn't solve F2L first
- once we've solved F2L, we can only do U moves without breaking up our progress, which is counterproductive

Instead, Kociemba gets the cube into one of the states in `"G1"`, which means it has the following properties:
- all the corners are oriented (like in 3OP)
- all the edges are oriented (like in 3OP)
- all the middle layer edges are already in the middle layer

From there, we can solve the cube by using only `U, D, F2, B2, R2, L2`
- that is, we can basically pretend it's a 3x3x2 domino
 
 > [!note] !!!
 > The nice thing about this is that once the cube is in the G1/domino, we can search for an optimal domino solution
 > 
 > More importantly, every cube solution ends with some number of domino moves
 > - that number might be 0, but there's a good chance that there's some optimal solution that uses a few
 > - this means we can run the 2-phase search similar to before, except we can restrict ourselves to a domino search in the second half

> [!important] There are lots of details, including:
> - solving a cube into G1 is about as hard as solving the rest
> 	- this means that both parts of the search take roughly the same time
> - since G1 is a group, there is a lot of symmetry in the search
> 	- this speeds things up by allowing us to search multiple things at once
> - we can take lots of shortcuts
> 	- let's say we already have a solution of 26 moves, and are considering a solution that has taken 18 moves already
> 	- if we know that it takes at least 10 more moves to solve the corners, then we can stop searching for that solution
> 	- (there are efficient ways to do this by using prune tables)
> - if we run Kociemba for a short while, we can get a pretty short solution
> 	- if we run it for longer, we will quickly get some better solutions
> 	- the choice of G1 really helps with this
> - solvers for other puzzles usually use a similar approach, except they use more phases
> 	- this WCA scrambler for 4x4x4 uses 4 phases to generate a scramble for a random state (but it doesn't continue to find an optimal solution)
> - instead of iterative deepening, Kociemba implementations usually use IDA*, which is iterative deepening combined with a heuristic
> 	- instead of going through the solutions blindly, the algorithm tries to go down path that look like they might have a shorter solution
> 	- this helps find shorter solutions earlier, which cuts down on the additional searching

## Example Reconstruction
Look at the reconstruction of `Mats Walk's 5.55 WR`

The scramble is:
		`D2 U' R2 U F2 D2 U' R2 U' B' L2 R' B' D2 U B2 L' D' R2`

Notice that the first half use only `U, D, F2, B2, R2, L2`

This is because TNoodles yses Shuang Chen's min2phase to do the following:
- generate a random state
- solve the state using Kociemba
- invert the solution to get a scramble for the state

The last half of the solution becomes the first half of the scramble, which is why the initial moves are in G1
