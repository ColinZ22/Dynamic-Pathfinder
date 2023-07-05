# Dynamic Pathfinder
This dynamic pathfinder algorithm finds and plots the shortest path in the presence of both static and dynamic (moving) obstacles.

## Visual Demo:
* Static Obstacles:
![](https://github.com/ColinZ22/Dynamic-Pathfinder/blob/main/Demos/Static_Demo.gif)

* Dynamic Obstacles:
![](https://github.com/ColinZ22/Dynamic-Pathfinder/blob/main/Demos/Dynamic_Demo_1.gif)
![](https://github.com/ColinZ22/Dynamic-Pathfinder/blob/main/Demos/Dynamic_Demo_2.gif)
![](https://github.com/ColinZ22/Dynamic-Pathfinder/blob/main/Demos/Dynamic_Demo_3.gif)
![](https://github.com/ColinZ22/Dynamic-Pathfinder/blob/main/Demos/Dynamic_Demo_4.gif)

## Algorithm Details
The algorithm models the environment as a graph and attempts to find the shortest path between the start and end points by exploring neighbors of points in the direction of least “cost.” 
The cost in this algorithm is defined to be roughly equal to the distance between the point in question and the goal point with additional measures taken to account for possible dynamic obstacles around the path. The cost function effectively directs the search towards the goal point and reduces the number of inefficient paths searched compared to other search algorithms that I had considered (like Dijkstra's Algorithm). 
## Time Complexity
The overall time complexity of the program is estimated to be around O(N * log N ), where N is the number of total unexplored points in the environment. As the distance between the start and goal increases (therefore increasing the number of unexplored points in the environment), the time it takes for the program to explore and sort the unexplored_points list also increases.
## Potential Changes
The implementation of a priority queue in the search algorithm can potentially increase the performance of the program. A priority queue will reduce the time complexity of the overall algorithm when the distance between the start and goal is large. The time complexity to go through the unexplored_points list is O( N ), where N is the number of total number of unexplored points in the environment. However, the time complexity would reduce to O ( log(N) ) if a priority queue is used, which is much better than O ( N ) at large N values. 
