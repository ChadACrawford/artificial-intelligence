# Use modified policy iteration page 656
# Estimate utility: U^{(i+1)}\gets R(s) + \sum_{s'} p(s'|s,a)u^{(i)}(s')
import random
# from nav import NavigationMDP
import nav


def estimate_utilities(m, pi, T=100):
    u = dict()
    for s in m.states:
        u[s] = m.r(s) if m.is_terminal(s) else 0

    for t in range(T):
        u2 = dict()
        for s in m.states:
            u2[s] = m.r(s) if m.is_terminal(s) else m.r(s) + sum([ps2_sa * u[s2] for s2, ps2_sa in m.ps(s, pi[s])])
        u = u2

    return u


def modified_policy_iteration(m):
    pi = dict()
    for s in m.states:
        if not m.is_terminal(s):
            pi[s] = random.choice(m.actions(s))
        else:
            pi[s] = m.actions(s)[0]

    changes = 1
    t = 0
    while changes:
        t += 1
        pi2 = dict()
        changes = 0
        u = estimate_utilities(m, pi)
        for s in m.states:
            if m.is_terminal(s):
                pi2[s] = pi[s]
            else:
                pi2[s] = max([(a, sum([ps2_sa * u[s2] for s2, ps2_sa in m.ps(s, a)])) for a in m.actions(s)],\
                             key=lambda x: x[1])[0]
            if not pi[s] == pi2[s]:
                changes += 1
        pi = pi2
        # nav.draw_grid_pi(m, pi)
        # print "Iteration %d" % (t,)
        # print "  # Changes: %d" % (changes,)

    print "Number of iterations: %d" % (t,)
    return pi, estimate_utilities(m, pi)

# print "Running..."
# # m = NavigationMDP(8, 8, -0.5)
# # m.add_goal((8, 8), 1)
# # m.add_goal((1, 1), -1)
# # m.add_goal((8, 1), 2)
# # m.add_goal((1, 8), -2)
# # m.add_hole((5, 5))
# m = nav.NavigationMDP(7, 7, 0)
# m.add_hole((2, 2))
# m.add_hole((6, 2))
# m.add_hole((3, 3))
# m.add_goal((4, 2), -1)
# m.add_goal((4, 4), -1)
# m.add_goal((4, 3), 1)
#
# pi = modified_policy_iteration(m)
#
#
# nav.draw_grid_pi(m, pi)
# print
