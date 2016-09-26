"""
Ramer-Douglas-Peuckar algorithm for simplifying the path
"""
from math import sqrt


class RDP(object):
    @classmethod
    def distance(cls, a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    @classmethod
    def point_line_distance(cls, point, start, end):
        if start == end:
            return cls.distance(point, start)
        else:
            n = abs((end[0] - start[0]) * (start[1] - point[1]) -
                    (start[0] - point[0]) * (end[1] - start[1])
                    )
            d = sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            return n / d

    @classmethod
    def run(cls, points, eps):
        dmax = 0.0
        index = 0
        for i in range(1, len(points) - 1):
            d = cls.point_line_distance(points[i], points[0], points[-1])
            if d > dmax:
                index = i
                dmax = d
        if dmax >= eps:
            results = cls.run(points[:index + 1], eps)[:-1] + \
                      cls.run(points[index:], eps)
        else:
            results = [points[0], points[-1]]
        return results








    # def runing(self):
    #     simplified = np.array()