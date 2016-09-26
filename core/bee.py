import numpy as np

from rdp import RDP


class Bee(object):
    RDP_TOLERANCE = 5

    def __init__(self, id, path, bee_len, bee_width, bee_angle, start):
        self.id = id
        self.path = [path]
        self.x_px = [path[0]]
        self.y_px = [path[1]]
        self.bee_len = [bee_len]
        self.bee_width = [bee_width]
        self.bee_angle = [bee_angle]
        self.start_frame = start
        self.end_frame = None

    def refresh_params(self, point, length, width, angle):
        if point == (0, 0) and self.path:
            point = self.path[-1]
        self.path.append(point)
        self.x_px.append(point[0])
        self.y_px.append(point[1])
        self.bee_len.append(length)
        self.bee_width.append(width)
        self.bee_angle.append(angle)

    def calculate_end_frame(self):
        self.end_frame = self.start_frame + len(self.path)

    def speed(self):
        x = np.array(self.x_px)
        y = np.array(self.y_px)
        return np.sqrt((x[1:] - x[:-1]) ** 2 + (y[1:] - y[:-1]) ** 2)

    def __angle(self, dir):

        dir2 = dir[1:]
        dir1 = dir[:-1]
        return np.arccos((dir1 * dir2).sum(axis=1) / (
            np.sqrt((dir1 ** 2).sum(axis=1) * (dir2 ** 2).sum(axis=1))))

    def filter_path_rdp(self):
        min_angle = np.pi * 0.45

        # simplified = np.array(RDP.run(self.path[:1500], self.RDP_TOLERANCE))
        simplified = np.array(RDP.run(self.path, self.RDP_TOLERANCE))
        sx, sy = simplified.T

        directions = np.diff(simplified, axis=0)
        theta = self.__angle(directions)
        # print (theta * 180) / np.pi
        idx = list(range(len(theta)))
        # idx = np.where(theta > min_angle)[0] + 1
        # print idx
        return sx, sy, idx
