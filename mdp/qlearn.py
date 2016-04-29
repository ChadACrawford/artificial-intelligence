

def qlearn(m, alpha=0.3, gamma=0.999, epsilon=0.2, num_episodes=1000):
    q = dict()

    for s in m.states:
        q[s] = 0

    for episode in range(num_episodes):
        pass

