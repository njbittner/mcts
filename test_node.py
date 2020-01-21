import node
import pytest
import numpy as np
import gym

@pytest.fixture
def Node():
    action_space = gym.spaces.Discrete(2)
    reward_space = (-np.inf, np.inf)
    Node = node.NodeClassFactory(action_space, reward_space, node.confidence_upper_bound)
    return Node


@pytest.mark.parametrize("parent_visit, visit1, value1, visit2, value2, correct", [
    (1, 1, 10, 1, 12, 1),
    (1, 1, 10, 3, 12, 0),
])
def test_node_selection_children_expanded(Node, parent_visit, visit1, value1, visit2, value2, correct):
    parent = Node(None, None)
    parent.visit_count = parent_visit
    parent.child_idx = 2
    n1 = Node(parent, 0)
    n1.visit_count = visit1
    n1.reward_accumulation = value1

    n2 = Node(parent, 1)
    n2.visit_count = visit2
    n2.reward_accumulation = value2

    nodes = [n1, n2]

    parent.children = {0:n1, 1:n2}

    choice = parent.select_child()
    assert choice == nodes[correct]


def test_node_selection_children_unexpanded(Node):
   parent = Node(None, None)
   parent.visit_count = 1
   parent.child_idx = 1
   choice = parent.select_child()
   assert choice.action==1
   assert choice.visit_count == 0
   assert choice.reward_accumulation == 0
   assert choice.parent == parent
   assert parent.child_idx == 2
   assert parent.children[1] == choice

def test_node_leaf_neg(Node):
    n = Node(None, None)
    n.children = {0: 1, 1: 2}
    assert not n.is_leaf

def test_node_leaf_pos(Node):
    n = Node(None, None)
    assert n.is_leaf


def test_node_root_neg(Node):
    n = Node(None, None)
    assert n.is_root

def test_node_root_pos(Node):
    n = Node(42, None)
    assert not n.is_root


def test_node_expanded_pos(Node):
    n = Node(None, None)
    n.visit_count = 1
    assert n.is_expanded

def test_node_expanded_neg(Node):
    n = Node(None, None)
    assert not n.is_expanded
