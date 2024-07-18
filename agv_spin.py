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




def update(frame):
   
    angle = np.radians(frame)
    
    # Rotate vertices
    rotated_vertices = rotate_vertices(vertices, angle)
    
    # Update forklift
    forklift.set_xy(rotated_vertices)
    
    # Check for random points
    for point in random_points:
        x, y = point
        # Convert point to polar coordinates
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # Check if the point is within the sector
        if (0 <= theta <= angle) and (r <= forklift_len):
            print(f"Point {point} is inside the sector at angle {np.degrees(angle)} degrees.")
    

    random_scatter.set_offsets(random_points)
    
# Create animation
animation = FuncAnimation(fig, update, frames=np.arange(0, 91, 5), interval=200, repeat=False)
plt.legend()
plt.show()









