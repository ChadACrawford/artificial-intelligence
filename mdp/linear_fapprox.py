import numpy as np
import numpy.random as npr
import math


def qlearn1(m, f, lmbda=0.8, alpha=0.1, gamma=0.999, epsilon=0.2, num_episodes=100):
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
            theta += alpha * delta * e
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
        self._widths = [(x2 - x1) / self._num_tiles for x1, x2 in dims]
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
        smap = tuple([math.floor((x + o) / w) % self._num_tiles for x, o, w in zip(s, offsets, self._widths)])
        # print smap, offsets, self._widths
        return (d,) + smap

    def features(self, s):
        phi = self._empty_feature_vector
        for d in range(self._num_dimensions):
            k = self.get_feature(s, d)
            phi[k] = 1
        return phi.flatten()


class RadialBasis(LinearApprox):
    def __init__(self, num_centers):
        pass

    def num_features(self):
        raise NotImplementedError

    def features(self, s):
        pass
