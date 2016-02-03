from nav import NavigationMDP


def value_iteration(m, y, e):
    u = dict()
    for s in m.states:
        if m.is_terminal(s):
            u[s] = m.r(s)
        else:
            u[s] = 0
    delta = 100
    t = 0
    while delta > e * (1 - y) / y:
        t += 1
        delta = 0
        u2 = dict()
        for s in m.states:
            if m.is_terminal(s):
                u2[s] = m.r(s)
            else:
                u2[s] = max([m.r(s, a) + sum([y * ps2_sa * u[s2] for s2, ps2_sa in m.ps(s, a)])
                             for a in m.actions(s)])
                # if s == (3, 4, 0, 0):
                #     print [(a, sum([m.r(s, a) + y * ps2_sa * u[s2] for s2, ps2_sa in m.ps(s, a)]))
                #            for a in m.actions(s)]
            delta = max(delta, abs(u2[s]-u[s]))
        #print delta
        u = u2

    print "Number of iterations: %d" % (t,)
    pi = dict()
    for s in m.states:
        pi[s] = max(
            [(a, m.r(s, a) + sum([y * ps2_sa * u[s2] for s2, ps2_sa in m.ps(s, a)]))
             for a in m.actions(s)], key=lambda x: x[1])[0]
    return pi, u

# print "Running..."
# m = NavigationMDP(8, 8, -0.5)
# m.add_goal((8, 8), 1)
# m.add_goal((1, 1), -1)
# m.add_goal((8, 1), 2)
# m.add_goal((1, 8), -2)
# m.add_hole((5, 5))
# m = NavigationMDP(4, 3, -2)
# m.add_hole((2, 2))
# m.add_goal((4, 2), -1)
# m.add_goal((4, 3), 1)
#
# pi, u = value_iteration(m, 1, 1e-20)


def to_arrow(a):
    if a == "left":
        return "<<"
    elif a == "right":
        return ">>"
    elif a == "up":
        return "^^"
    elif a == "down":
        return "vv"


def draw_grid(m, pi, u, costs=False):
    w = m.vvidth
    h = m.height
    print '-' * 14 * w
    for y in range(h, 0, -1):
        s = ""
        for x in range(1, w+1):
            if m.is_hole((x,y)):
                s += " | ******** | "
            elif m.is_terminal((x,y)):
                s += " |   %4d   | " % (m.r((x, y)))
            else:
                if costs:
                    s += " | %8.3f | " % (u[(x,y)],)
                else:
                    s += " |    %2s    | " % (to_arrow(pi[(x, y)]),)
        print s
        print '-' * 14 * w

# draw_grid(m, pi, u)
# print
# draw_grid(m, pi, u, costs=True)