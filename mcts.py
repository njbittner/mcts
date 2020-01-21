import node
import copy
import gym

DEFAULT_MAX_DEPTH = 10000
DEFAULT_SAMPLES = 100
DEFAULT_MAX_ROLLOUT_STEPS = 1000


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


def mcts_sample(node, env, default_policy=random_policy, max_depth=DEFAULT_MAX_DEPTH) -> None:
    """
    Generates a single action trajectory using MCTS.
    :param env:
    :return:
    """
    terminal_state = False
    trajectory_reward = 0
    depth = 0

    def _termination_criteria(terminal, depth) -> bool:
        return terminal or max_depth < depth

    # Find leaf node
    while node.is_expanded and not _termination_criteria(terminal_state, depth):
        _, reward, terminal_state, _ = env.step(node.action)
        node = node.select_child()
        trajectory_reward += reward
        depth += 1

    # Expand
    # Current node is either an unexpanded leaf or we have reached a termination criteria
    if not _termination_criteria(terminal_state, depth):
        default_rollout_reward = default_policy(env)
        trajectory_reward += default_rollout_reward

    # Backprop reward through tree
    node.backprop(trajectory_reward)



def run_search_battery(env_root, tree_root, n_samples:int = 1000):
    """
    Run a search battery. "Search battery" referrs to sampling many trajectories from the root node and updating the
    tree datastructure with the back-propagated reward values.
    :return:
    """
    tree_root.parent = None
    tree_root.action = None
    for i in range(n_samples):
        env = copy.deepcopy(env_root)
        mcts_sample(tree_root.select_child(), env)

    best_node = tree_root.select_child(exploration_weight=0)

    return best_node


def mcts_play(env:gym.Env, games=5, warmup_steps=0):
    action_space = env.action_space
    reward_space = env.reward_range
    Node = node.NodeClassFactory(action_space, reward_space, node.confidence_upper_bound)

    current_node = Node(None, None)

    for game_idx in range(games):
        print(f"Playing game {game_idx}")
        reward_acc = 0
        env.reset()
        terminal = False
        for _ in range(warmup_steps):
            _, reward, terminal, _ = env.step(action_space.sample())
            reward_acc += reward
        env.render()

        while not terminal:
            current_node = Node(None, None)
            current_node = run_search_battery(env, current_node)
            _, reward, terminal,_ = env.step(current_node.action)
            env.render()
            reward_acc += reward

if __name__ == "__main__":
    env = gym.make("Taxi-v3")
    mcts_play(env)
