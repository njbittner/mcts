from node import Node
import copy

DEFAULT_MAX_DEPTH = 1000
DEFAULT_SAMPLES = 100
DEFAULT_MAX_ROLLOUT_STEPS = 10000


def random_policy(env, max_steps:int = DEFAULT_MAX_ROLLOUT_STEPS) -> float:
    """
    """
    total_reward = 0
    terminal = False
    step = 0
    while not terminal and step<max_steps:
        _, reward, terminal, _ = env.step(env.action_space.sample())
        total_reward += reward
    return float(total_reward)


def mcts_sample(root_node, env, default_policy=random_policy, max_depth=DEFAULT_MAX_DEPTH) -> None:
    """
    Generates a single action trajectory using MCTS.
    :param env:
    :return:
    """
    terminal_state = False
    node = root_node
    trajectory_reward = 0
    depth = 0

    def _termination_criteria(terminal, depth) -> bool: return terminal or depth < max_depth

    # Find leaf node
    while not node.is_leaf and not node.is_expanded and not _termination_criteria(terminal_state, depth):
        node = node.select_child()
        _, reward, terminal_state, _ = env.step(node.action)
        trajectory_reward += reward
        depth += 1

    # Expand
    # Current node is either an unexpanded leaf or we have reached a termination criteria
    if not _termination_criteria(terminal_state, depth):
        default_rollout_reward = default_policy(env)
        trajectory_reward += default_rollout_reward

    # Backprop reward through tree
    node.backpropagate_trajectory_reward(trajectory_reward)



def run_search_battery(env_root, tree_root = None, n_samples:int = 1000):
    """
    Run a search battery. "Search battery" referrs to sampling many trajectories from the root node and updating the
    tree datastructure with the back-propagated reward values.
    :return:
    """
    if not tree_root:
        tree_root = Node(None, None)

    for i in range(n_samples):
        env = copy.deepcopy(env)
        mcts_sample(tree_root, env)

    best_node = None.

    return best_node

def mcts_play(env):
    env.reset()

def mcts():
    pass
    # Run a search battery. "Search battery" referrs to sampling many trajectories from the root node and updating the
    # tree datastructure with the back-propagated reward values.
