# Project 2

import numpy as np
import numpy.random as npr
import math
import bayes_net
import multinomial
import inference


# bnet = multinomial.random_network(10, 3, polytree=True)


# def burglary():
#     return bayes_net.BayesNetwork(
#         (multinomial.MultinomialVariable, (),
#          (2,
#           ((), (0.1, 0.9))
#           )
#          )
#
#     )


def random_var(num_vars, num_values, num_missing=0):
    z = npr.choice(num_values, num_vars) + 1
    missing = npr.choice(num_vars, size=num_missing, replace=False)
    z[missing] = 0
    return z, missing

# z, missing = random_var(10, 3, 2)
# z[0] = 0

# Testing

# print z
#
# print inference.enumeration_ask(bnet, bnet.var(0), z)
#
# print inference.likelihood_weighting(bnet, bnet.var(0), z)
#
# print inference.gibbs(bnet, bnet.var(0), z)

import matplotlib.pyplot as plt


def likelihood_ratio(d1, d2):
    """
    The value E_D[\frac{P(X|D)}{P(X|D')}]; that is, how well does the distribution D' predict the distribution D?
    :param d1: The source distribution D
    :param d2: The predicted distribution D'
    :return: The expectation value
    """
    X = list(d1.iterkeys())
    q = []
    for x in X:
        q += [np.exp(2 * np.log(d1[x]) - np.log(d2[x]))]
    return 1/math.fsum(q)


def run(num_vars, num_values, num_missing, polytree, p):
    bn = multinomial.random_network(num_vars, num_values, polytree=polytree, p=p)
    z, missing = random_var(num_vars, num_values, num_missing=num_missing)
    x = bn.var(npr.choice(missing))
    # if len(missing) == 1:
    #     print bn
    #     print x.dist(z)
    print "exact",
    i_exact = inference.enumeration_ask(bn, x, np.array(z))
    print "likelihood",
    i_likel = inference.likelihood_weighting(bn, x, np.array(z))
    lr1 = likelihood_ratio(i_exact, i_likel)
    print "%6.4f" % (lr1,),
    print "gibbs",
    i_gibbs = inference.gibbs(bn, x, np.array(z))
    lr2 = likelihood_ratio(i_exact, i_gibbs)
    print "%6.4f" % (lr2,)
    return lr1, lr2


def figure_1():
    """
    Comparison of likelihood ratios for varying numbers of variables
    :return:
    """
    NUM_TRIALS = 10
    MIN_VARS = 2
    MAX_VARS = 30
    NUM_VALUES = 2
    P_MISSING = 0.5
    # llikel = np.zeros((MAX_VARS-MIN_VARS, NUM_TRIALS))
    # lgibbs = np.zeros((MAX_VARS-MIN_VARS, NUM_TRIALS))
    data_x = []
    data_yl = []
    data_yg = []
    var_range = range(MIN_VARS, MAX_VARS+1)
    for num_vars in var_range:
        print "v:", num_vars
        i = num_vars - MIN_VARS
        for t in range(NUM_TRIALS):
            print "t:", t+1
            data_x += [num_vars]
            y1, y2 = run(num_vars, NUM_VALUES, int(P_MISSING * NUM_VALUES) + 1, False, 0.3)
            data_yl.append(y1)
            data_yg.append(y2)

    scatter1 = plt.scatter(data_x, data_yl, c="b", label="Likelihood weighting")
    plt.plot(data_x, np.poly1d(np.polyfit(data_x, data_yl, 1))(data_x))
    scatter2 = plt.scatter(data_x, data_yg, c="g", label="Gibbs sampling")
    plt.plot(data_x, np.poly1d(np.polyfit(data_x, data_yg, 1))(data_x))

    plt.legend([scatter1, scatter2])
    plt.xlabel("Number of Variables")
    plt.ylabel("Likelihood ratio")

    plt.savefig("figure_1.pdf")
    plt.show()
    plt.clf()


def figure_2():
    """
    Comparison of likelihood ratios for varying numbers of variables
    :return:
    """
    NUM_TRIALS = 10
    NUM_VARS = 20
    NUM_VALUES = 2
    MIN_MISSING = 1
    MAX_MISSING = NUM_VARS
    data_x = []
    data_yl = []
    data_yg = []
    miss_range = range(MIN_MISSING, MAX_MISSING+1)
    for num_missing in miss_range:
        print "m:", num_missing
        for t in range(NUM_TRIALS):
            print "t:", t+1
            data_x += [num_missing]
            y1, y2 = run(NUM_VARS, NUM_VALUES, num_missing, False, 0.3)
            data_yl.append(y1)
            data_yg.append(y2)

    scatter1 = plt.scatter(data_x, data_yl, c="b", label="Likelihood weighting")
    plt.plot(data_x, np.poly1d(np.polyfit(data_x, data_yl, 1))(data_x))
    scatter2 = plt.scatter(data_x, data_yg, c="g", label="Gibbs sampling")
    plt.plot(data_x, np.poly1d(np.polyfit(data_x, data_yg, 1))(data_x))

    plt.legend([scatter1, scatter2])

    plt.savefig("figure_2.pdf")
    plt.show()
    plt.clf()


if __name__ == "__main__":
    figure_1()
    figure_2()
