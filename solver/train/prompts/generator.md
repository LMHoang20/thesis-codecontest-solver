# System Task:
You are a problem manager that is tasked with searching and organizing the information in the correct order that someone need to figure out if they want to solve the problem.
You have access to the private, hidden observation space of the problem, you use the name of the problem to find the correct observation space corresponding.
Explanation of the system:
    - The observation space is a set of all correct observations about the problem.
    - An observation is a statement that is always true given the premise of the problem.
    - A premise is a statement that is explicitly stated in the problem statement or a statement that is always true in mathematics that is NOT overwritten by the premise of the problem.
    - The observation space is modelled as a directed graph. Each node is an observation, and each edge is a logical implication.
What you MUST do:
- Write the SQL query to find the correct observation space for the problem.
- Write the output of the query. The format of the output is a set of (ID | [array of previous observation IDs required to make the implication] | observation) tuples, ordered by ID.
Note:
Array of observation IDs is a list of integers, where each integer is the ID of the observation. If the array is empty, the observation is a premise.
# Problem statement:
## Name:
681_E. Runaway to a Shadow
## Tags:
geometry, sortings
## Description:
Dima is living in a dormitory, as well as some cockroaches.
At the moment 0 Dima saw a cockroach running on a table and decided to kill it. Dima needs exactly T seconds for aiming, and after that he will precisely strike the cockroach and finish it.
To survive the cockroach has to run into a shadow, cast by round plates standing on the table, in T seconds. Shadow casted by any of the plates has the shape of a circle. Shadow circles may intersect, nest or overlap arbitrarily.
The cockroach uses the following strategy: first he equiprobably picks a direction to run towards and then runs towards it with the constant speed v. If at some moment t ≤ T it reaches any shadow circle, it immediately stops in the shadow and thus will stay alive. Otherwise the cockroach is killed by the Dima's precise strike. Consider that the Dima's precise strike is instant.
Determine the probability of that the cockroach will stay alive.
Input
In the first line of the input the four integers x0, y0, v, T (|x0|, |y0| ≤ 109, 0 ≤ v, T ≤ 109) are given — the cockroach initial position on the table in the Cartesian system at the moment 0, the cockroach's constant speed and the time in seconds Dima needs for aiming respectively.
In the next line the only number n (1 ≤ n ≤ 100 000) is given — the number of shadow circles casted by plates.
In the next n lines shadow circle description is given: the ith of them consists of three integers xi, yi, ri (|xi|, |yi| ≤ 109, 0 ≤ r ≤ 109) — the ith shadow circle on-table position in the Cartesian system and its radius respectively.
Consider that the table is big enough for the cockroach not to run to the table edges and avoid Dima's precise strike.
Output
Print the only real number p — the probability of that the cockroach will stay alive.
Your answer will be considered correct if its absolute or relative error does not exceed 10 - 4.
Examples
Input
0 0 1 1
3
1 1 1
-1 -1 1
-2 2 1
Output
0.50000000000
Input
0 0 1 0
1
1 0 1
Output
1.00000000000
Note
The picture for the first sample is given below. 
<image>
Red color stands for points which being chosen as the cockroach's running direction will cause him being killed, green color for those standing for survival directions. Please note that despite containing a circle centered in ( - 2, 2) a part of zone is colored red because the cockroach is not able to reach it in one second.

# Model Answer
SQL:
```sql
SELECT * FROM observation_space WHERE problem_name = '681_E. Runaway to a Shadow';
```
OUTPUT:
```
1 | [] | At the moment 0 Dima saw a cockroach running on a table and decided to kill it.
2 | [] | Dima needs exactly T seconds for aiming, and after that he will precisely strike the cockroach and finish it.
3 | [] | To survive the cockroach has to run into a shadow, cast by round plates standing on the table, in T seconds.
4 | [] | Shadow casted by any of the plates has the shape of a circle.
5 | [] | Shadow circles may intersect, nest or overlap arbitrarily.
6 | [] | The cockroach uses the following strategy: first he equiprobably picks a direction to run towards and then runs towards it with the constant speed v.
7 | [] | If at some moment t ≤ T it reaches any shadow circle, it immediately stops in the shadow and thus will stay alive.
8 | [] | Otherwise the cockroach is killed by the Dima's precise strike.
9 | [] | Consider that the Dima's precise strike is instant.
10 | [1, 2, 3, 4, 6, 7, 8, 9] | Assume the case when cockroach at the moment $0$ is already inside or on the border of some circle. In that case the cockroach will always survive, i. e. the probability is $1$.
11 | [6] | The cockroach will have time to run to every point inside the circle with center of $x_0$, $y_0$ and radius $v × T$. Let's call this circle "cockroach circle".
12 | [] | The probability of the cockroach surviving is the probability of the cockroach choosing the angle that reach one of the shadow circles.
13 | [] | The cockroach can choose an angle somewhere between $0$ and $2π$.
14 | [4, 11, 12, 13] | For each circle, we can find a start angle and an end angle, each between $0$ and $2π$ where if the cockroach chooses a direction in that range, it will survive.
15 | [14] | The start and end angles of the arc are bounded by the lines from the center of the "cockroach circle" to the intersection points on the shadow circle.
16 | [14] | These start and end angles form an arc on the "cockroach circle".
17 | [16] | The probability the cockroach survive is the sum of non-overlapping arc lengths of on the "cockroach circle" divided by $2π$. 
18 | [15] | If there is no intersection points or there is only one, then current circle is too far away from cockroach.
19 | [15] | Once we have the start and end angles for each shadow circle, we can sort the angles and calculate the sum of the lengths of the non overlapping arcs that they form.
20 | [12, 13, 19] | This length divided by $2π$ will give us the answer.
```