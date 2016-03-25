import numpy as np
import numpy.random as npr
import math
import random
import itertools
from bayes_net import BayesVariable, BayesNetwork


class MultinomialVariable(BayesVariable):
    def __init__(self, bn, index, parents, params):
        super(MultinomialVariable, self).__init__(bn, index, parents)
        num_values, p = params
        self._domain = np.array(range(1, num_values+1))
        self._p = dict()
        for pk, pd in p:
            if len(pk) != len(parents):
                raise AttributeError("Length of parameters must match the number of parents the variable has.")

            if len(pd) != num_values:
                raise AttributeError("Length of results must match number of values for variable.")

            for j, pkj in enumerate(pk):
                ps = bn.var(self._parents[j])
                if pkj not in ps.domain:
                    raise AttributeError("Parameter value not in domain of parent")

            self._p[tuple(pk)] = np.array(pd)

    @property
    def domain(self):
        return self._domain

    def dist(self, z):
        p = z[self._parents]
        d = np.zeros(len(self.domain))
        # print z, p
        d[:] = self._p[tuple(p)]
        # d[-1] = 1 - np.sum(d)
        return d
    
    def sample(self, z):
        return npr.choice(self.domain, p=self.dist(z))

    def log_p_d(self, x, z):
        # p = tuple(z[self._parents])
        # print x, z, p
        return np.log(self.p_d(x, z))

    def p_d(self, x, z):
        p = tuple(z[self._parents])
        return self._p[p][x-1]
    
    def log_p(self, z):
        lp = [self.log_p_d(z[self.i], z)]
        for c in self._bn.children(self):
            lp += [c.log_p_d(z[c.i], z)]
        return math.fsum(lp)

    def p(self, z):
        return np.exp(self.log_p(z))


def rand_dist(num_values):
    x = npr.rand(num_values)
    x /= sum(x)
    return x


def _is_child(xs, x, y):
    for p in xs[x]:
        if y == p or _is_child(xs, p, y):
            return True

    return False


def _all_parents(xs, x):
    ps = []
    for p in range(x):
        if _is_child(xs, x, p):
            ps.append(p)
    return set(ps)


def _is_connected(xs, x, y):
    p1 = _all_parents(xs, x)
    p2 = _all_parents(xs, y)

    return len(p1.intersection(p2)) > 0


def random_network(num_vars, num_values, polytree=False, p=0.1):
    args = []

    nodes = []
    for x in range(num_vars):
        parents = np.where(npr.rand(x) < p)[0]
        random.shuffle(parents)
        nodes += [[]]
        if polytree:
            for p in parents:
                if not _is_connected(nodes, x, p):
                    nodes[-1] += [p]

        # print parents
        params_p = []
        if parents.size:
            for xp in itertools.product(*([range(1, num_values+1)] * len(parents))):
                params_p += [(xp, rand_dist(num_values))]
        else:
            params_p += [([], rand_dist(num_values))]
        args += [(MultinomialVariable, parents, (num_values, params_p))]

    return BayesNetwork(args)
