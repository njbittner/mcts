import typing
import gym
import numpy as np


def confidence_upper_bound(node, exploration_weight):
    exploration_term = exploration_weight * np.sqrt(np.log(node.parent.visit_count) / node.visit_count)
    avg_traj_reward_term = node.reward_accumulation / node.visit_count
    return avg_traj_reward_term + exploration_term

def NodeClassFactory(action_space, reward_space, node_score_metric):
    class Node(object):
        def __init__(self, parent, action):
            """
            MCTS tree node
            Nodes in MCTS are an action in a sequence of actions (action trajectory) explored from a starting state, x
            :param parent: Parent Node
            :param action: action taken from parent node to reach this node.
            """
            self.parent = parent
            self.action = action
            self.visit_count = 0  # the number of times this node has been visited within a search battery
            self.reward_accumulation = 0  # Stores the total reward for this node accumulated over a search battery
            self.children = {}  # a map from actions to children.
            self.child_idx = 0
            self.action_space = action_space
            self.rewad_space = reward_space

        @property
        def is_leaf(self) -> bool:
            return not self.children

        @property
        def is_root(self) -> bool:
            """ If parent is None, then this is the root node."""
            return not self.parent

        @property
        def is_expanded(self) -> bool:
            return self.visit_count > 0

        def backprop(self, trajectory_reward) -> None:
            """
            Ripples the trajectory reward value up through parent nodes in the tree, until the root node.
            :return:
            """
            self.visit_count += 1
            self.reward_accumulation += trajectory_reward
            if self.parent:
                self.parent.backprop(trajectory_reward)

        def select_child(self, exploration_weight = 1):
            """
            Select a child based on some defined metric. In this case we're going to use confidence upper bound, and
            the condition that if not all children have been tried to pick a new child.

            Since for now we're just handling discrete actions, it is sufficient to keep a list of which actions we have
            tried
            """
            # We haven't tried all actions from this point
            if self.child_idx < self.action_space.n:
                action = self.child_idx
                child = Node(self, action)
                self.children[action] = child
                self.child_idx += 1

            # Pick the max child
            else:
                child = max(self.children.values(), key=lambda x: node_score_metric(x, exploration_weight))
            return child

        def __str__(self):
            node = self
            chain = []
            while node.parent:
                chain.append(node.action)
                node = node.parent
            chain.append("root")
            return str(chain[::-1])


        def __repr__(self):
            return self.__str__()

    return Node



