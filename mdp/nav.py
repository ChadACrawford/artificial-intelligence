# Navigation MDP

import itertools
from mdp import MDP

class NavigationMDP(MDP):
    def __init__(self, w, h, cost):
        self.__w = w
        self.__h = h
        self.__cost = cost
        self.__holes = []
        self.__goals = dict()

    @property
    def vvidth(self):
        return self.__w

    @property
    def height(self):
        return self.__h

    @property
    def states(self):
        return filter(lambda s: not self.is_hole(s), itertools.product(range(1,self.__w+1), range(1,self.__h+1)))

    def actions(self, s):
        return ["left", "right", "up", "down"]

    def add_hole(self, s):
        self.__holes.append(s)

    def is_hole(self, s):
        return s in self.__holes

    def add_goal(self, s, r):
        self.__goals[s] = r;

    def is_terminal(self, s):
        return s in self.__goals
    
    def r(self, s):
        if s in self.__goals:
            return self.__goals[s]
        else:
            return self.__cost
    
    def move(self, s, a):
        s2 = []
        if a == "left" and s[0] > 1:
            s2 = (s[0]-1, s[1])
        elif a == "right" and s[0] < self.__w:
            s2 = (s[0]+1, s[1])
        elif a == "up" and s[1] < self.__h:
            s2 = (s[0], s[1]+1)
        elif a == "down" and s[1] > 1:
            s2 = (s[0], s[1]-1)
        if not s2 or self.is_hole(s2):
            return s
        else:
            return s2

    def can_move(self, s, a):
        lst = []
        if a == "left":
            return map(lambda a2: self.move(s, a2), ["left", "up", "down"])
        elif a == "right":
            return map(lambda a2: self.move(s, a2), ["right", "up", "down"])
        elif a == "up":
            return map(lambda a2: self.move(s, a2), ["up", "left", "right"])
        else:
            return map(lambda a2: self.move(s, a2), ["down", "left", "right"])
    
    def p(self, s1, a, s2):
        s3s = self.can_move(s1, a)
        if s2 in s3s:
            return (0.8 if s3s[0] == s2 else 0)\
                + (0.1 if s3s[1] == s2 else 0)\
                + (0.1 if s3s[2] == s2 else 0)
        else:
            return 0

    def ps(self, s1, a):
        s2s = self.can_move(s1, a)
        #print s1, a, s2s
        return [(s2s[0], 0.8), (s2s[1], 0.1), (s2s[2], 0.1)]

def to_arrow(a):
    if a == "left":
        return "<<"
    elif a == "right":
        return ">>"
    elif a == "up":
        return "^^"
    elif a == "down":
        return "vv"


def draw_grid_pi(m, pi):
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
                s += " |    %2s    | " % (to_arrow(pi[(x, y)]),)
        print s
        print '-' * 14 * w


def draw_grid_u(m, pi):
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
                s += " | %8.3f | " % (u[(x,y)],)
        print s
        print '-' * 14 * w