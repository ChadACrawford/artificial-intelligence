import numpy as np
import numpy.random as npr
import itertools
import bayes_net
import math


def enumeration_ask(bn, x, z):
    q = dict()
    for xs in x.domain:
        q[xs] = 0

    for xs in x.domain:
        z2 = np.array(z)
        z2[x.i] = xs
        q[xs] = np.exp(math.fsum(_enumerate_all(bn, z2)))

    sum_w = math.fsum(q.itervalues())
    for xs in q.iterkeys():
        q[xs] /= sum_w

    return q


def _enumerate_all(bn, z, index=0):
    if index >= len(z):
        return [0]
    y = bn.var(index)
    if z[index] > 0:
        return [y.log_p_d(z[index], z)] + _enumerate_all(bn, z, index+1)
    else:
        a = []
        for yi in y.domain:
            z2 = np.array(z)
            z2[index] = yi
            a += [y.log_p_d(yi, z2)] + _enumerate_all(bn, z2, index+1)
        return [math.log(math.fsum(np.exp(a)))]

    
def likelihood_weighting(bn, x, z, n=2000):
    w = dict()
    for xj in x.domain:
        w[xj] = 0

    for _ in range(n):
        xj, wj = _weighted_sample(bn, z)
        xj = xj[x.i]
        w[xj] += wj

    sum_w = sum(w.itervalues())
    for xs in w.iterkeys():
        w[xs] /= sum_w
    return w


def _weighted_sample(bn, z):
    log_w = []
    x = np.array(z)
    for i, x_i in enumerate(bn.variables):
        if x[i]:
            log_w.append(x_i.log_p_d(x[i], x))
        else:
            x[i] = x_i.sample(x)
    return x, np.exp(math.fsum(log_w))


def gibbs(bn, x, z, n=2000):
    ys = [i for i, y in enumerate(z) if y <= 0]

    z = np.array(z)
    
    for yi in ys:
        y = bn.var(yi)
        z[yi] = npr.choice(y.domain)

    q = dict()
    for xs in x.domain:
        q[xs] = 0

    for _ in range(n):
        # # yi = npr.choice(ys)
        for yi in ys:
            y = bn.var(yi)
            z = _gibbs_sample(y, z)
        # print z
        # yi = npr.choice(ys)
        # y = bn.var(yi)
        # _gibbs_sample(bn, y, z)
        # _gibbs_sample(bn, x, z)

        q[z[x.i]] += 1

    for xs in q.iterkeys():
        q[xs] /= 1. * n
        
    return q


def _gibbs_sample(x, z):
    d = np.zeros(len(x.domain))
    for i, xs in enumerate(x.domain):
        z[x.i] = xs
        d[i] = x.p(z)
    d /= sum(d)

    xs = npr.choice(x.domain, p=d)
    # print x.dist(z)
    z[x.i] = xs
    return z
