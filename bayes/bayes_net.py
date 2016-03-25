import numpy as np


class BayesVariable(object):
    def __init__(self, bn, index, parents):
        self._bn = bn
        self._index = index
        self._parents = parents

    @property
    def i(self):
        return self._index

    @property
    def parents(self):
        return map(lambda x: self._bn.var(x), self._parents)

    def sample(self, z):
        return NotImplementedError

    def log_p_d(self, x, z):
        return NotImplementedError

    def p_d(self, x, z):
        return NotImplementedError

    def log_p(self, x, z):
        return NotImplementedError

    def p(self, x, z):
        return NotImplementedError

    def __repr__(self):
        return "BayesVariable [index=%d,parents={%s}]" % (self._index, ','.join([str(p) for p in self._parents]),)


class BayesNetwork(object):
    def __init__(self, x):
        self._x = np.empty(len(x), dtype=np.object)
        self.__children = [None] * len(x)
        for i, (xi_obj, xi_parents, xi_params) in enumerate(x):
            self._x[i] = xi_obj(self, i, xi_parents, xi_params)

    @property
    def size(self):
        return len(self._x)

    def var(self, i):
        return self._x[i]

    @property
    def variables(self):
        return self._x

    def sample(self, size=1):
        z = np.array( (size, self.size) )
        for i in range(size):
            for j in range(self.size):
                z[i,j] = self._x[j].sample(z[i])
        return z

    def children(self, x):
        if not self.__children[x.i]:
            self.__children[x.i] = [y for y in self._x if x in y.parents]
        return self.__children[x.i]

    def __repr__(self):
        return 'BayesNetwork [\n   ' + \
            '\n   '.join([str(v) for v in self._x]) +\
            '\n]'
