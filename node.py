import typing



class Node(object):
    def __init__(self, parent: typing.Union[Node, None], action):
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

    @property
    def is_leaf(self) -> bool:
        return bool(self.children)

    @property
    def is_root(self) -> bool:
        """ If parent is None, then this is the root node."""
        return not self.parent

    @property
    def is_expanded(self) -> bool:
        return self.visit_count > 0

    def backpropagate_trajectory_reward(self, trajectory_reward) -> None:
        """
        Ripples the trajectory reward value up through parent nodes in the tree, until the root node.
        :return:
        """
        self.visit_count += 1
        self.reward_accumulation += trajectory_reward
        if self.parent:
            self.parent.backpopagate_trajectory_reward(trajectory_reward)

