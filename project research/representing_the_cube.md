# Representing the Cube
There are approx. 43 quintillion possible states the cube can be in, and only 1 correct solution

> This number is obtained by knowing that 8 corner cuboids can be rotated in three different ways. Knowing this, we can multiply the number of combinations of the corners by the number of combination of the edges and divide by the number of correct orbits

$$
\frac{(3^8*8!)(2^12*12!)}{3*2*2} \approx 4.3*10^{19}
$$

## Notation
| Symbol | Meaning                       |
| ------ | ----------------------------- |
| `U`    | Up face clockwise             |
| `D`    | Down face clockwise           |
| `L`    | Left face clockwise           |
| `R`    | Right face clockwise          |
| `F`    | Front face clockwise          |
| `B`    | Back face clockwise           |
| `X2`   | Turn face X twice (180°)      |
| `X'`   | Turn face X counter-clockwise |
> A `face` is simply the collection of `facelets` on a given side (a rubik's cube has 6 faces).

## How Humans Solve the Cube
The most common methods are the `beginner's method` and `CFOP`

Beginner's method consists of 7 steps:
1. Cross
2. Corners
3. Middle layer
4. Top cross
5. Fix cross
6. Permutation of corners
7. Orientation of Corners

In contrast, CFOP is only 4 steps:
1. Cross
2. First two layers (F2L)
3. Orientation of the last layer (OLL)
4. Permutation of the last layer (PLL)

> A dedicated speedcuber will memorise all 57 OLL cases and all 21 PLL cases. An algorithm for one of these steps can involve anywhere between 7 and 17 moves.

> A novice using the beginner's method can solve in about 200 moves, while a speedcuber using CFOP can solve in roughly 60 moves.

The optimal number of moves to solve is 20
- this was achieved by reducing the 43 quintillion possible combinations by a factor of 48 using symmetry and mirrored states

There are 24 ways we can orient a rubik's cube in space and we can multiply this by 2 to account for mirrored states
- after this reduction, only a set of 55,882,296 states had to be examined

## Representing the Cube in Code
A few common ways are:
- 1-D array, 2-D array, 3-D array
- OOP
- Matrix
- Binary

> [!tip] There are many more other ways we can represent the cube such as the use of strings and other data structures.

Another important design choice is to consider how to represent the facelet of the cube
- usually, a facelet will store the colour, but optionally it might also store the location depending on how the cube is being represented

### 1-D Array
Using a 1-D array, each facelet of the cube can be labeled 0 through 53.
- each of these labels map the respective facelet to the index in the array
- a move to the cube can be executed by performing a mapping function that rearranges the facelets accordingly

### 2-D Array
A cube can be represented using a 2-D array to store an array of faces
- this approach stores 6 faces, where each face is an array of the 9 facelets corresponding to the given face

### 3-D Array
Using OOP principles, a cube can be represented using a 3-D array
- working with an abstract cubie class, corners, edges, and centers can all extend from this class
- the 3-D array can consist of cubies
	- each one located in its corresponding location to where its 3-D coordinate would be on a real cube

### Matrix
A matrix can be used to store the cubes state by using a 6x54 matrix
- each of the columns represents 1 facelet on the cube and a 1 is placed in the column corresponding to its colour row

Example:
$$
\begin{pmatrix}
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & \dots \\
0 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & \dots \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & \dots \\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & \dots \\
0 & 0 & 0 & 1 & 0 & 1 & 0 & 0 & 0 & \dots \\
1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & \dots 
\end{pmatrix}
$$
- 6 colours x 54 facelets

### Binary
This approach is similar to the 2-D array approach
- it stores 64 bit integers, one for each face of the cube

Each byte (8 bits) stores the colour encoded in binary
- since the centres never move, we can omit them and just store the 8 remaining facelets
- this gives the advantage of operations such as bit shifting and masks to manipulate the cube, leading to fast execution time and efficient space complexity
