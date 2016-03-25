
import numpy as np
import numpy.random as npr
import math
import bayes_net
import multinomial
import inference


bn = bayes_net.BayesNetwork(
    [
     (multinomial.MultinomialVariable, [],
      [2, [([], [0.5, 0.5])]]),
     (
         multinomial.MultinomialVariable, [0],
         (2, [([1], [0.6, 0.4]), ([2], [0.1, 0.9])])
     )
    ]
)

z = np.array([0, 1])

print inference.enumeration_ask(bn, bn.var(0), z)
