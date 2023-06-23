import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import path_generation as pg

# Functions used to plot obstacles
def plot_polygon(polygon, color):
    x, y = zip(*polygon)
    axes.fill(x, y, color=color)

# Function used to update the animation at each frame
def update_animation(frame):
    # update dynamic obstacles
    for i, obstacle in enumerate(dynamic_obstacles):
        x, y = pg.get_dynamic_obstacle_location(obstacle, frame + 1)
        dynamic_obstacles_location[i].set_data(x, y)

    if frame > 0:
        # Generate the path from 1 frame ago
        prevPath = pg.generate_path(start, goal, static_obstacles, dynamic_obstacles, frame - 1)

        # White-out the previous path for clearer illustration of the updated path
        x = [i[0] for i in prevPath[:frame + 1]]
        y = [i[1] for i in prevPath[:frame + 1]]
        axes.plot(x, y, color='white')

    # Generate new path
    newPath = pg.generate_path(start, goal, static_obstacles, dynamic_obstacles, frame)

    # If new path is not available, and it is not the first frame, use the previous path
    if newPath is None and frame > 0:
        path = prevPath
    else:
        path = newPath

    # Plot the path as a red line up to the current frame
    x = [i[0] for i in path[:frame + 1]]
    y = [i[1] for i in path[:frame + 1]]
    axes.plot(x, y, color='red')

    # Plot the start and goal points as green and blue circles, respectively
    axes.scatter(start[0], start[1], color='green', s=100)
    axes.scatter(goal[0], goal[1], color='blue', s=100)
    return []


# Define the start and goal points as tuples
start = (-2, -2)
goal = (8, 6)

# Define the static obstacles as a list of polygons
static_obstacles = [
    [(2, 2), (2, 8), (3, 8), (3, 3), (8, 3), (8, 2)],
    [(6, 6), (7, 6), (7, 7), (6, 7)]
]

# Define the dynamic obstacles as a list of points
dynamic_obstacles = [
    {'initial_position': [
        (10, 1)], "velocity": [random.uniform(-1, 1), random.uniform(-1, 1)]},
    {'initial_position': [
        (2.5, 10)], "velocity": [random.uniform(-1, 1) * .5, random.uniform(-1, 1) * .5]},
    {'initial_position': [
        (5, 5)], "velocity": [random.uniform(-1, 1) * .2, random.uniform(-1, 1) * .2]},
    {'initial_position': [
        (0, 2.5)], "velocity": [random.uniform(-1, 1) * .1, random.uniform(-1, 1) * .1]}
]

# Create the figure and axes
fig = plt.figure(figsize=(5, 5))
axes = fig.add_subplot(111)
plt.xlim(-5, 15)
plt.ylim(-5, 15)
plt.xlabel('X')
plt.ylabel('Y')

dynamic_obstacles_location = []

# Plot the obstacles
for i, obstacle in enumerate(dynamic_obstacles):
    point, = axes.plot([], [], 'ok', ms=20)
    dynamic_obstacles_location.append(point)

for i, obstacle in enumerate(static_obstacles):
    plot_polygon(obstacle, 'darkgray')


# Create the animation using FuncAnimation
animation = FuncAnimation(fig, update_animation, frames=45, interval=250, blit=True)

# Show the plot
plt.show()