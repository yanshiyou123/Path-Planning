import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

forklift_len = 2
forklift_wid = 1

# At initial rotation (0 degrees)
vertices = np.array([
    [-forklift_len / 2, -forklift_wid / 2],
    [forklift_len / 2, -forklift_wid / 2],
    [forklift_len / 2, forklift_wid / 2],
    [-forklift_len / 2, forklift_wid / 2]
])

# Calculate rotated vertices given rotation angle
def rotate_vertices(vertices, angle):
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])
    rotated_vertices = np.dot(vertices, rotation_matrix.T)
    return rotated_vertices

# Check if a point is inside the polygon
def is_point_in_polygon(point, polygon):
    def get_cross(p1, p2, randomp):
        return (p2[0] - p1[0]) * (randomp[1] - p1[1]) - (randomp[0] - p1[0]) * (p2[1] - p1[1])

    crosses = [get_cross(polygon[i], polygon[(i + 1) % 4], point) for i in range(4)]
    if all(cross > 0 for cross in crosses) or all(cross < 0 for cross in crosses):
        return True
    return False

# Generate random points
random_points = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(50)]

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# Plot
random_xs, random_ys = zip(*random_points)
random_scatter = ax.scatter(random_xs, random_ys, color='gray', label='Random Points')

forklift = plt.Polygon(vertices, closed=True, fill=None, edgecolor='blue')
ax.add_patch(forklift)

in_range_res = []

def update(frame):
    angle = np.radians(frame)
    
    # Rotate vertices
    rotated_vertices = rotate_vertices(vertices, angle)
    
    # Update forklift
    forklift.set_xy(rotated_vertices)
    
    # Check for random points
    for point in random_points:
        if is_point_in_polygon(point, rotated_vertices):
            if point not in in_range_res:
                in_range_res.append(point)
                print(f"Point {point} is inside the forklift area at angle {np.degrees(angle)} degrees.")
    
    random_scatter.set_offsets(random_points)

# Create animation
animation = FuncAnimation(fig, update, frames=np.arange(0, 91, 5), interval=200, repeat=False)
plt.legend()
plt.show()

# Print points within the forklift area
for i, pos in enumerate(in_range_res):
    print(f"Point within forklift area {i}: {pos}")









