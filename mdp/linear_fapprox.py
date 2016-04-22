import numpy as np
import numpy.random as npr
import math
import random


def qlearn1(m, f, lmbda=0.1, alpha=0.3, gamma=0.9999, epsilon=0.2, num_episodes=100):
    theta = np.zeros((f.num_features,))
    t = 1
    for _ in range(num_episodes):
        s = m.start()
        a = npr.choice(m.actions(s))
        e = np.zeros((theta.size,))
        print t
        while not m.is_terminal(s):
            #print t
            #print s
            phi_a1 = feature_estimate(m, s, a, f)
            e += phi_a1
            s2, r2 = m.act(s, a)
            delta = r2 - sum(theta * phi_a1)
            q = []
            for a2 in m.actions(s2):
                phi_a2 = feature_estimate(m, s2, a2, f)
                q.append(sum(theta * phi_a2))
            delta += (gamma**t) * max(q)
            theta = (1-alpha) * theta + alpha * delta * e
            if npr.random() < 1 - epsilon:
                a2 = max(zip(m.actions(s2), q), key=lambda x: x[1])[0]
                e *= (gamma**t) * lmbda
            else:
                a2 = npr.choice(m.actions(s2))
                e = np.zeros((theta.size,))
            s = s2
            a = a2
            t += 1

    pi = lambda s: max([(a, sum(theta * feature_estimate(m, s, a, f))) for a in m.actions(s)], key=lambda x: x[1])[0]
    return pi, theta


def qlearn2(m, f, alpha=0.5, gamma=1.0, epsilon=0.2, num_episodes=1000):
    actions = m.actions()
    theta = dict()
    for a in actions:
        theta[a] = np.zeros((f.num_features,))
    for episode in range(num_episodes):
        t = 0
        s = m.start()
        a = npr.choice(m.actions(s))
        q = 0
        while not m.is_terminal(s):
            s2, r2 = m.act(s, a)
            # if r2 < -1 or s2[0] > 5 and s2[1] < 5:
            #     print "wat", s2, r2
            qp = sum(theta[a] * f.features(s))
            # print a, s, s2, r2, [(a, r2 + gamma * qp) for a in m.actions(s)]
            actions = m.actions(s)
            random.shuffle(actions)
            a2, q2 = max([(a2, r2 + gamma * sum(theta[a2] * f.features(s2))) for a2 in actions], key=lambda x: x[1])
            delta = q2 - qp
            # if random.random() < 0.01:
            #     print delta
            # print a, delta, s, s2
            theta[a] += alpha * delta * (f.features(s))
            if npr.random() < epsilon:
                a2 = npr.choice(m.actions(s))
            q = q2
            s = s2
            a = a2
            t += 1
        print episode+1, t, s, r2


    pi = lambda s: max([(a, sum(theta[a] * f.features(s))) for a in m.actions(s)], key=lambda x: x[1])[0]
    f_exp = lambda s: max(sum(theta[a] * f.features(s)) for a in m.actions(s))
    return pi, f_exp, theta



def feature_estimate(m, s, a, f):
    theta = np.zeros((f.num_features,))
    n = 10
    for _ in range(n):
        s2, r2 = m.act(s, a)
        theta += f.features(s2)
    return theta / n


class LinearApprox:
    def __init__(self):
        pass

    @property
    def num_features(self):
        raise NotImplementedError

    def features(self, s):
        raise NotImplementedError


class TileEncoding(LinearApprox):
    def __init__(self, m, num_layers, resolution, num_tiles):
        self._num_layers = num_layers
        self._resolution = resolution
        self._num_tiles = num_tiles
        self._num_dimensions = m.num_dimensions
        self._widths = None
        self._offsets = None
        self.__construct_features(m)

    def __construct_features(self, m):
        dims = m.dimensions
        self._widths = [(1. * x2 - x1) / (self._num_tiles-1) for x1, x2 in dims]
        self._offsets = np.zeros((self._num_layers, self._num_dimensions))
        for i in range(self._num_layers):
            for j in range(self._num_dimensions):
                self._offsets[i, j] = npr.uniform(0, self._widths[j])

    @property
    def num_features(self):
        return np.prod((self._num_layers,) + ((self._num_tiles,) * self._num_dimensions))

    @property
    def _empty_feature_vector(self):
        return np.zeros((self._num_layers,) + ((self._num_tiles,) * self._num_dimensions))

    def get_feature(self, s, d):
        offsets = self._offsets[d]
        smap = tuple([max(min(math.floor((x + o) / w), self._num_tiles-1), 0)
                      for x, o, w in zip(s, offsets, self._widths)])
        # print smap, offsets, self._widths
        return (d,) + smap

    def features(self, s):
        phi = self._empty_feature_vector
        for d in range(self._num_layers):
            k = self.get_feature(s, d)
            # print s, k
            phi[k] = 1
        return phi.flatten() / np.sum(phi)


class RadialBasis(LinearApprox):
    def __init__(self, m, num_centers, radius):
        self._num_centers = num_centers
        self._radius = radius
        self.__construct_features(m)

    def __construct_features(self, m):
        self._u = [np.array([npr.uniform(d[0], d[1]) for d in m.dimensions]) for _ in range(self._num_centers)]
        self._r = npr.uniform(0, self._radius, self._num_centers)

    @property
    def num_features(self):
        return self._num_centers

    def features(self, s):
        phi = np.zeros((self.num_features,))
        for k in range(len(phi)):
            phi[k] = np.exp(- 0.5 * sum((self._u[k] - s)**2) / self._r[k])
        # print phi
        return phi / sum(phi)
