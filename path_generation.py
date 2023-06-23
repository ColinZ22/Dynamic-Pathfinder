import math

# Calculate the distance between two points
def point_to_point_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Calculate the neighbors of a point
def neighbors(point):
    x, y = point
    return [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1), (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]


# Check if a point is inside a polygon
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_inters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Function used to get the location of a dynamic obstacle at each frame
def get_dynamic_obstacle_location(obstacle, frame):
    point = obstacle['initial_position']
    velocity = obstacle['velocity']
    vx, vy = velocity[0], velocity[1]
    x = [i[0] + frame * vx for i in point]
    y = [i[1] + frame * vy for i in point]
    return x, y

# Calculate the cost when dynamic obstacles are present
def dynamic_obstacles_cost(neighbor, dynamic_obstacles, frame):

    # Cost constant to add to the cost of the neighbor when dynamic obstacle is near
    w_dynamic_obstacle = 2

    obstacle_positions = []
    for obstacle in dynamic_obstacles:
        # Calculate the positions of each dynamic obstacle 1 frame ahead
        x, y = get_dynamic_obstacle_location(obstacle, frame + 1)
        obstacle_positions.append((x[0], y[0]))

    dist_to_obstacle = []
    # Calculate the distance between the neighbor and the closest obstacle
    for obstacle_position in obstacle_positions:
        dist_to_obstacle.append(point_to_point_distance(neighbor, obstacle_position))
    dist_to_obstacle.sort()

    # If the closest obstacle is 1 unit away, return the constant
    if dist_to_obstacle[0] < 1:
        return w_dynamic_obstacle
    else:
        return 0


# function to check if a point is an obstacle
def is_static_obstacle(point, static_obstacles):
    # Check if point is in static obstacles
    for obstacle in static_obstacles:
        if point_in_polygon(point, obstacle):
            return True

    return False


def generate_path(start, goal, static_obstacles, dynamic_obstacles, frame):
    # Initialize the unexplored_points and explored_points lists
    unexplored_points = []
    explored_points = []

    # Initialize the costs and previous_point dictionaries
    known_cost = {start: 0}
    estimate_cost = {start: point_to_point_distance(start, goal)}
    previous_point = {start: None}

    # Add the start point to the unexplored_points list
    unexplored_points.append((estimate_cost[start], start))

    # Continue searching until the unexplored_points list is empty
    while unexplored_points:
        # Get the point with the lowest estimate_cost from the unexplored_points list
        current_estimate_cost, current_point = min(unexplored_points)

        # Remove the current point from the unexplored_points list
        unexplored_points.remove((current_estimate_cost, current_point))

        # Check if we have reached the goal
        if current_point == goal:
            # Reconstruct the path and return it
            path = []
            while current_point:
                path.append(current_point)
                current_point = previous_point[current_point]
            path.reverse()
            return path

        # Add the current point to the explored_points list
        explored_points.append(current_point)

        # Explore the neighbors of the current point
        for neighbor in neighbors(current_point):
            # Check if the neighbor is already in the explored_points list
            if neighbor in explored_points:
                continue
            # Check if the neighbor is a static obstacle
            if is_static_obstacle(neighbor, static_obstacles):
                continue

            # Calculate the temp_known_cost for the neighbor
            temp_known_cost = known_cost[current_point] + point_to_point_distance(current_point, neighbor)

            # Check if the neighbor is not in the known_cost list,
            #    or if the temp_known_cost is lower than the known cost
            if neighbor not in known_cost or temp_known_cost < known_cost[neighbor]:

                temp_known_cost += dynamic_obstacles_cost(neighbor, dynamic_obstacles, frame)

                # Update the cost and previous_point dictionaries for the neighbor
                known_cost[neighbor] = temp_known_cost
                estimate_cost[neighbor] = temp_known_cost + point_to_point_distance(neighbor, goal)
                previous_point[neighbor] = current_point

                # Add the neighbor to the explored_points list
                unexplored_points.append((estimate_cost[neighbor], neighbor))

        # Sort the explored_points list by cost
        unexplored_points.sort()

    # If we reach here, there is new available path to the goal
    return None

