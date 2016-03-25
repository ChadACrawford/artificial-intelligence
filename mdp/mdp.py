

class MDP:
    @property
    def states(self):
        pass

    def actions(self, s):
        pass
    
    def r(self, s1, s2):
        pass

    def is_terminal(self, s):
        pass

    def p(self, s1, a, s2):
        pass

    def ps(self, s1, a):
        """Return a list of state transitions and probabilities associated
        with performing action a at state s1.

        """
        pass


class ContinuousStateMDP:
    def __init__(self):
        pass

    @property
    def num_dimensions(self):
        return len(self.dimensions)

    @property
    def dimensions(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def actions(self, s):
        raise NotImplementedError

    def is_terminal(self, s):
        raise NotImplementedError

    def r(self, s1, s2):
        raise NotImplementedError

    def act(self, s, a):
        pass
