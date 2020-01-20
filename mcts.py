import copy
import numpy as np
import random
import gym

ACTION_REPEAT = 1


def mcts_traversal_factory(action_space, score_metric):
    class Node:
        def __init__(self, parent):
            self.untried_actions = [x for x in range(action_space.n)]  # type: list
            self.n = 0
            self.q = 0
            self.children = {}
            self.parent = parent

        def pick_random_action(self):
            # Picks an action at random from the list of untried actions
            random_idx = random.randint(0, len(self.untried_actions)-1)
            return self.untried_actions.pop(random_idx)

        def select_child(self):
            # If this function is called, it means that this node has been visited at least once (its already done
            # a default policy expand)

            # If there are any actions we haven't tried, start with those. Will create a new node.
            if self.untried_actions:
                a = self.pick_random_action()
                next_node = Node(self)
                self.children[a] = next_node
                return a, next_node

            # No actions we haven't tried, just pick the action with the highest score. Nodes already exist
            else:
                max_a = None
                max_score = -1
                for a in self.children.keys():
                    current_score = score_metric(self.children[a])
                    if current_score > max_score:
                        max_a = a
                        max_score = current_score
                return max_a, self.children[max_a]

        def backprop(self):
            if self.parent:
                self.parent.q += self.q
                self.parent.backprop()

        def __str__(self):
            return ""

        def __repr__(self):
            return self.__str__()

    def recurse(cur_state, node: Node, reward_so_far):
        print()
        if node.n == 0 and node.parent is not None:
            """ first time we've ever seen this node """
            node.n = 1
            reward_acc = 0
            for _ in range(100):
                a = action_space.sample()
                for _ in range(ACTION_REPEAT):
                    _, reward, _, _ = cur_state.step(a)
                reward_acc += reward
            node.q = reward_so_far + reward_acc
            node.backprop()
        else:
            # revisting a perviously seen node or the root node.
            node.n += 1
            a, next_node = node.select_child()
            _, reward, _, _ = cur_state.step(a)
            recurse(cur_state, next_node, reward_so_far + reward)

    return Node, recurse


def MCTS(env_root_original, action_space, score_metric, sample_budget):
    NodeCls, recurse_fn = mcts_traversal_factory(action_space, score_metric)
    root = NodeCls(None)
    for _ in range(sample_budget):
        env_root = copy.deepcopy(env_root_original)
        recurse_fn(env_root, root, 0)
    a, _ = root.select_child()
    return a



def UCB_score_metric(node):
    return node.q / node.n + 2*C * np.sqrt(2 * np.log(node.parent.n) / node.n)

if __name__ == "__main__":
    C = 1
    WARM_START = 40
    sample_budget = 50
    env = gym.make("Breakout-v0")
    action_space = env.action_space
    env.reset()
    for i in range(WARM_START):
        env.step(env.action_space.sample())
        env.render()

    for _ in range(1000):
        a = MCTS(env, action_space, UCB_score_metric, sample_budget)
        for _ in range(ACTION_REPEAT):
            env.step(a)
        env.render()

