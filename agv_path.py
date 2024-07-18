import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

# 长和宽
forklift_len = 2
forklift_wid = 1
p0 = np.array([0, 0])  # start
p1 = np.array([5, 0])  # control
p2 = np.array([0, 5])
p3 = np.array([5, 5])  # end

# 贝塞尔曲线公式
def bezier_curve(p0, p1, p2, p3, t):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

# 100个点
t_values = np.linspace(0, 1, 100)
path = np.array([bezier_curve(p0, p1, p2, p3, t) for t in t_values])

# 切线角度
def angle_between_points(p1, p2):
    return np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

angles = np.array([angle_between_points(path[i], path[i + 1]) for i in range(len(path) - 1)])
angles = np.append(angles, angles[-1])

# 叉车4个坐标点
def get_forklift_position(center, angle, forklift_len, forklift_wid):
    fx, fy = center
    cos = np.cos(angle)
    sin = np.sin(angle)
    offset_len = forklift_len * -0.25  # 将中心向前移动到叉车长度的前四分之三处
    fx += offset_len * cos
    fy += offset_len * sin
    half_len = forklift_len / 2
    half_wid = forklift_wid / 2
    position = np.array([
        [fx + half_len * cos - half_wid * sin, fy + half_len * sin + half_wid * cos],  # rt
        [fx - half_len * cos - half_wid * sin, fy - half_len * sin + half_wid * cos],  # lt
        [fx - half_len * cos + half_wid * sin, fy - half_len * sin - half_wid * cos],  # lb
        [fx + half_len * cos + half_wid * sin, fy + half_len * sin - half_wid * cos]   # rb
    ])
    return position



# 生成随机点
def get_random_points(n_points=50, x_range=(-5, 15), y_range=(-5, 15)):
    random_points = np.array([(random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])) for _ in range(n_points)])
    return random_points

random_points = get_random_points()

# 判断点是否在四边形内
def is_point_in_polygon(point, polygon):
    def get_cross(p1, p2, randomp):
        return (p2[0] - p1[0]) * (randomp[1] - p1[1]) - (randomp[0] - p1[0]) * (p2[1] - p1[1])

    crosses = [get_cross(polygon[i], polygon[(i + 1) % 4], point) for i in range(4)]
    if all(cross > 0 for cross in crosses) or all(cross < 0 for cross in crosses):
        return True
    return False

# 创建图
fig, ax = plt.subplots()
ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)

line, = ax.plot([], [], 'r')
car_patch, = ax.plot([], [], 'b')
rect = plt.Polygon(get_forklift_position(path[0], angles[0], forklift_len, forklift_wid), fill=False, edgecolor='b')
ax.add_patch(rect)

# 绘制随机点
ax.scatter(random_points[:, 0], random_points[:, 1], color='g')

in_range_res = []

def init():
    line.set_data([], [])
    car_patch.set_data([], [])
    rect.set_xy(get_forklift_position(path[0], angles[0], forklift_len, forklift_wid))
    return line, car_patch, rect

def update(frame):
    car_center = path[frame]
    car_angle = angles[frame]
    car_position = get_forklift_position(car_center, car_angle, forklift_len, forklift_wid)
    line.set_data(path[:frame, 0], path[:frame, 1])
    car_patch.set_data(path[:frame, 0], path[:frame, 1])
    rect.set_xy(car_position)

    for point in random_points:
        if is_point_in_polygon(point, car_position):
            if point.tolist() not in in_range_res:
                in_range_res.append(point.tolist())

    return line, car_patch, rect

anim = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, interval=100, repeat=False)
plt.show()

for i, pos in enumerate(in_range_res):
    print(f"在轨迹中的坐标 {i}: {pos}")
