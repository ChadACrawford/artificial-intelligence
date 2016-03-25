import mdp
import math
import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt


def distance(x1, x2):
    d = math.sqrt(sum([(a - b)**2 for a, b in zip(list(x1), list(x2))]))
    return d


class ContinuousNavigation(mdp.ContinuousStateMDP):
    def __init__(self, max_x, max_y, step_cost):
        self._max_x = max_x
        self._max_y = max_y
        self._goals = dict()
        self._rocks = dict()
        self._step_cost = step_cost

    def in_bound(self, s):
        return all([dmin <= sd <= dmax for sd, (dmin, dmax) in zip(list(s), self.dimensions)])

    def add_goal(self, s, r, g):
        self._goals[s] = r, g

    def is_goal(self, s1):
        for s, (r, g) in self._goals.iteritems():
            if distance(s1, s) < r:
                return g
        return False

    def start(self):
        return np.tile(0., self.num_dimensions)

    def add_rock(self, s, r):
        self._rocks[s] = r

    def is_rock(self, s1):
        for s2, r in self._rocks.iteritems():
            if distance(s1, s2) < r:
                return True
        return False

    @property
    def dimensions(self):
        return [(0, self._max_x), (0, self._max_y)]

    def actions(self, s=None):
        return ["left", "right", "up", "down"]

    def is_terminal(self, s):
        if self.is_goal(s):
            return True
        return False

    def r(self, s1, s2):
        g = self.is_goal(s2)
        if g:
            return g
        return self._step_cost

    move_left = np.array([.5, 0.], dtype='float64')
    move_right = np.array([-.5, 0.], dtype='float64')
    move_up = np.array([0., .5], dtype='float64')
    move_down = np.array([0., -.5], dtype='float64')

    def move(self, s, a):
        s = np.copy(s)
        if a == "up":
            s += self.move_up + npr.multivariate_normal(np.array([0., 0]), np.diag([0.25,0.125]))
        elif a == "down":
            s += self.move_down + npr.multivariate_normal(np.array([0., 0]), np.diag([0.25, 0.125]))
        elif a == "left":
            s += self.move_left + npr.multivariate_normal(np.array([0., 0]), np.diag([0.125, 0.25]))
        elif a == "right":
            s += self.move_right + npr.multivariate_normal(np.array([0., 0]), np.diag([0.125, 0.25]))
        else:
            pass
        return s

    def act(self, s, a):
        s2 = self.move(s, a)
        if self.is_rock(s2) or not self.in_bound(s2):
            s2 = np.copy(s)
        return s2, self.r(s, s2)

    def draw(self, fig):
        plt.xlim(self.dimensions[0])
        plt.ylim(self.dimensions[1])
        for s, r in self._rocks.iteritems():
            fig.gca().add_artist(plt.Circle(s, r, color='black'))
        for s, (r, g) in self._goals.iteritems():
            if g > 0:
                fig.gca().add_artist(plt.Circle(s, r, color='g'))
            else:
                fig.gca().add_artist(plt.Circle(s, r, color='r'))

import linear_fapprox as lf


def mdp1():
    m = ContinuousNavigation(10, 10, -0.01)
    m.add_goal((10, 10), 2, 10)
    m.add_goal((10, 1), 1, -10)
    m.add_rock((5, 5), 2)
    return m, 0, 10, 0, 10


def gen_heatmap(theta, f, xmin, xmax, ymin, ymax, dx, dy):
    nx = int(math.ceil((xmax-xmin)/dx))
    ny = int(math.ceil((ymax-ymin)/dy))
    q = np.zeros((nx, ny))
    for xi in range(nx):
        x = xmin + xi * dx
        for yi in range(ny):
            y = ymin + yi * dy
            phi = f.features((x, y))
            q[xi, yi] = sum(theta * phi)
    return q


def run():
    m, xmin, xmax, ymin, ymax = mdp1()
    fig = plt.gcf()
    f = lf.TileEncoding(m, 5, 1, 10)
    pi, theta = lf.qlearn1(m, f, num_episodes=100)
    heatmap = gen_heatmap(theta, f, xmin, xmax, ymin, ymax, 0.1, 0.1)
    print heatmap
    plt.clf()
    plt.imshow(heatmap)
    # m.draw(fig)
    # x = npr.uniform(m.dimensions[0][0], m.dimensions[0][1], 1000)
    # y = npr.uniform(m.dimensions[1][0], m.dimensions[1][1], 1000)
    # to_v = lambda x: (-1, 0) if x == "left" else\
    #     (1, 0) if x == "right" else\
    #     (0, 1) if x == "up" else\
    #     (0, -1)
    # vx, vy = zip(*[to_v(pi((x1, y1))) for x1, y1 in zip(x, y)])
    # plt.quiver(x, y, vx, vy)
    plt.show()


if __name__ == '__main__':
    run()
