# Navigation MDP

import itertools
from mdp import MDP


class WumpusMDP(MDP):
    def __init__(self, w, h, cost):
        self.__w = w
        self.__h = h
        self.__cost = cost
        self.__pits = dict()
        self.__golds = dict()
        self.__immunes = dict()
        self.__goals = dict()
        self.__wumpus = dict()

    @property
    def vvidth(self):
        return self.__w

    @property
    def height(self):
        return self.__h

    def __is_valid_state(self, s):
        return True

    @property
    def states(self):
        return filter(lambda x: self.__is_valid_state(x),
                      itertools.product(range(1, self.__w+1), range(1, self.__h+1), range(2), range(2)))

    def actions(self, s):
        if self.is_gold(s) or self.is_immunity(s):
            return ["left", "right", "up", "down", "pick up"]
        else:
            return ["left", "right", "up", "down"]

    def is_terminal(self, s):
        if self.is_goal(s) and self.has_gold(s):
            return True
        elif self.is_wumpus(s) and not self.has_immunity(s):
            return True
        else:
            return False

    def r(self, s, a=None):
        if self.is_gold(s) and a == "pick up":
            return self.__golds[s[:2]]
        if self.is_pit(s):
            return self.__pits[s[:2]]
        if self.is_wumpus(s) and not self.has_immunity(s):
            return self.__wumpus[s[:2]]
        if self.is_goal(s) and self.has_gold(s):
            return self.__goals[s[:2]]
        # if self.is_immunity(s):
        #     return self.__immunes[s[:2]]
        return self.__cost

    def p(self, s1, a, s2):
        if a == "pick up" and s2 == self.move(s1, a):
            return 1
        else:
            s3s = self.umove(self, s1, a)
            if s2 in s3s:
                return \
                    (0.8 if s3s[0] == s2 else 0)\
                    + (0.1 if s3s[1] == s2 else 0)\
                    + (0.1 if s3s[2] == s2 else 0)
            else:
                return 0

    def ps(self, s1, a):
        if a == "pick up":
            return [(self.move(s1, a), 1)]
        else:
            s2s = self.umove(s1, a)
            return [(s2s[0], 0.8), (s2s[1], 0.1), (s2s[2], 0.1)]

    def is_pit(self, s):
        return s[:2] in self.__pits

    def add_pit(self, x, r):
        self.__pits[x] = r

    def is_gold(self, s):
        return not self.has_gold(s) and s[:2] in self.__golds

    def add_gold(self, x, r):
        self.__golds[x] = r

    def is_immunity(self, s):
        return not self.has_immunity(s) and s[:2] in self.__immunes

    def add_immunity(self, x):
        self.__immunes[x] = 1

    def is_goal(self, s):
        return s[:2] in self.__goals

    def add_goal(self, x, r):
        self.__goals[x] = r

    def is_wumpus(self, s):
        return s[:2] in self.__wumpus

    def add_wumpus(self, x, r):
        self.__wumpus[x] = r

    def has_gold(self, s):
        return s[2]

    def has_immunity(self, s):
        return s[3]

    def move(self, s, a):
        s2 = []
        if a == "pick up" and self.is_gold(s):
            s2 = (s[0], s[1], 1, s[3])
        elif a == "pick up" and self.is_immunity(s):
            s2 = (s[0], s[1], s[2], 1)
        elif a == "left" and s[0] > 1:
            s2 = (s[0]-1, s[1], s[2], s[3])
        elif a == "right" and s[0] < self.__w:
            s2 = (s[0]+1, s[1], s[2], s[3])
        elif a == "up" and s[1] < self.__h:
            s2 = (s[0], s[1]+1, s[2], s[3])
        elif a == "down" and s[1] > 1:
            s2 = (s[0], s[1]-1, s[2], s[3])
        if not s2:
            return s
        else:
            return s2

    def umove(self, s, a):
        # pu = ["pick up"] if self.is_gold(s) or self.is_immunity(s) else []
        if a == "left":
            return map(lambda a2: self.move(s, a2), ["left", "up", "down"])
        elif a == "right":
            return map(lambda a2: self.move(s, a2), ["right", "up", "down"])
        elif a == "up":
            return map(lambda a2: self.move(s, a2), ["up", "left", "right"])
        else:
            return map(lambda a2: self.move(s, a2), ["down", "left", "right"])


def to_arrow(a):
    if a == "left":
        return "<=="
    if a == "right":
        return "==>"
    if a == "up":
        return "^^^"
    if a == "down":
        return "vvv"
    if a == "pick up":
        return "get"


def draw_board(m, pi=None):
    for has_gold in [0,1]:
        for has_immunity in [0,1]:
            print
            print
            print ("has" if has_gold else "no") + " gold, " + ("has" if has_immunity else "no") + " immunity"
            for y in range(m.height, 0, -1):
                for x in range(1, m.vvidth+1):
                    s = (x,y,has_gold,has_immunity)
                    if m.is_pit(s):
                        print "( PPP )",
                    elif m.is_gold(s):
                        print "( GGG )",
                    elif m.is_wumpus(s):
                        print "( WWW )",
                    elif m.is_immunity(s):
                        print "( III )",
                    elif m.is_goal(s):
                        print "( SSS )",
                    else:
                        print "(     )",
                print
                if pi:
                    for x in range(1, m.vvidth+1):
                        print "  %3s  " % (to_arrow(pi[(x, y, has_gold, has_immunity)])),
                print


def latex_board(m, pi, u):
    for has_gold, has_immunity in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        print """\\begin{subtable}{1.0\\textwidth}\n\\centering\n \\begin{tabular}{|%s}\\hline""" % ('l|' * (m.vvidth+1),),
        for y in range(m.height, 0, -1):
            msg = []
            for x in range(1, m.vvidth+1):
                s = (x, y, has_gold, has_immunity)
                b = "P" if m.is_pit(s) else\
                    "G" if m.is_gold(s) else\
                    "W" if m.is_wumpus(s) else\
                    "I" if m.is_immunity(s) else\
                    "S" if m.is_goal(s) else\
                    ""
                ir = m.r(s, pi[s])
                a = "$\\Leftarrow$" if pi[s] == "left" else\
                    "$\\Rightarrow$" if pi[s] == "right" else\
                    "$\\Uparrow$" if pi[s] == "up" else\
                    "$\\Downarrow$" if pi[s] == "down" else\
                    "$\\grab$"
                msg.append("\\wumpusblock{%s}{%2.2f}{%s}{%2.2f}" % (b, ir, a, u[s]))
            print "&".join(msg) + "\\\\\\hline",
        print """\\end{tabular}\n\\caption{%s gold, %s immunity}\n\\end{subtable}""" % ("Has" if has_gold else "No",
                                                                                    "has" if has_immunity else "no")

from policy_iteration import modified_policy_iteration
from value_iteration import value_iteration


def create_wumpus_world():
    m = WumpusMDP(4, 4, -0.04)
    m.add_goal((1, 1), 10)
    m.add_gold((3, 4), 10)
    m.add_immunity((2, 4))
    m.add_pit((3, 1), -20)
    m.add_pit((3, 3), -1)
    m.add_pit((2, 3), -600)
    m.add_wumpus((1, 3), -50)
    return m


def test_value_iteration():
    m = create_wumpus_world()
    pi, u = value_iteration(m, 1, 1e-6)
    # print pi
    draw_board(m, pi)
    latex_board(m, pi, u)


def test_policy_iteration():
    m = create_wumpus_world()
    pi, u = modified_policy_iteration(m)
    # print pi
    draw_board(m, pi)
    latex_board(m, pi, u)

if __name__ == "__main__":
    print "#" * 80
    print
    test_value_iteration()
    # print
    # print "#" * 80
    # print
    # test_policy_iteration()