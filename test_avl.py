import unittest
from avl import AvlTree, ItemNode, nullNode


class AvlTreeTest(unittest.TestCase):
    def test_rotate_right(self):
        T1 = ItemNode("T1")
        T2 = ItemNode("T2")
        T3 = ItemNode("T3")
        start = ItemNode("B",
                         ItemNode("A",
                                  T1,
                                  T2),
                         T3)
        want = ItemNode("A",
                        T1,
                        ItemNode("B",
                                 T2,
                                 T3))
        self.assertEqual(start.rotateRight(), want)

    def test_rotate_left(self):
        T1 = ItemNode("T1")
        T2 = ItemNode("T2")
        T3 = ItemNode("T3")
        start = ItemNode("B",
                         T3,
                         ItemNode("A",
                                  T2,
                                  T1))
        want = ItemNode("A",
                        ItemNode("B",
                                 T3,
                                 T2),
                        T1)
        self.assertEqual(start.rotateLeft(), want)

    def test_rotate_twice(self):
        start = ItemNode("B",
                         ItemNode("A",
                                  ItemNode("T1"),
                                  ItemNode("C",
                                           ItemNode("T2"),
                                           ItemNode("T3"))),
                         ItemNode("T4"))
        after_a_left = ItemNode("B",
                                ItemNode("C",
                                         ItemNode("A",
                                                  ItemNode("T1"),
                                                  ItemNode("T2")),
                                         ItemNode("T3")),
                                ItemNode("T4"))
        after_b_right = ItemNode("C",
                                 ItemNode("A",
                                          ItemNode("T1"),
                                          ItemNode("T2")),
                                 ItemNode("B",
                                          ItemNode("T3"),
                                          ItemNode("T4")))
        start.left = start.left.rotateLeft()
        self.assertEqual(start, after_a_left)
        self.assertEqual(start.rotateRight(), after_b_right)

    def test_plain_insert(self):
        """Test membership operations that don't require rebalancing. """
        t = AvlTree([10, 3, 18, 2, 4, 13, 40])
        for (i, j) in zip(t, [2, 3, 4, 10, 13, 18, 40]):
            self.assertEqual(i, j)
        self.assertEqual(t.root,
                         ItemNode(10,
                                  ItemNode(3,
                                           ItemNode(2),
                                           ItemNode(4)),
                                  ItemNode(18,
                                           ItemNode(13),
                                           ItemNode(40))))
        # We are not testing height because the final implementation might not
        # use it.
        self.assertEqual(t.root.balance, 0)
        self.assertTrue(10 in t)
        self.assertTrue(14 not in t)
        t.add(14)
        self.assertTrue(14 in t)
        self.assertEqual(t.root.balance, -1)

    def test_rebalance(self):
        """Test all four cases of rebalancing."""
        left_right = ItemNode(5,
                              ItemNode(3,
                                       nullNode,
                                       ItemNode(4)))
        left_left = ItemNode(5,
                             ItemNode(4,
                                      ItemNode(3)))
        right_left = ItemNode(3,
                              nullNode,
                              ItemNode(5,
                                       ItemNode(4),
                                       nullNode))
        right_right = ItemNode(3,
                               nullNode,
                               ItemNode(4,
                                        nullNode,
                                        ItemNode(5)))
        goal = ItemNode(4,
                        ItemNode(3),
                        ItemNode(5))
        for (key, val) in [("left_left", left_left),
                           ("left_right", left_right),
                           ("right_left", right_left),
                           ("right_right", right_right)]:
            self.assertEqual(val.rebalance(), goal, key)
        self.assertEqual(goal.rebalance(), goal)

    def test_remove_leaf(self):
        n = ItemNode(4,
                     ItemNode(3),
                     ItemNode(5))
        n = n.remove(5)
        self.assertEqual(n, ItemNode(4,
                                     ItemNode(3)))
        n = n.remove(4)
        self.assertEqual(n, ItemNode(3))
        with self.assertRaises(KeyError):
            n.remove(6)
        n = ItemNode(4,
                     ItemNode(3),
                     ItemNode(5))
        n = n.remove(3)
        self.assertEqual(n, ItemNode(4,
                                     nullNode,
                                     ItemNode(5)))
        n = n.remove(4)
        self.assertEqual(n, ItemNode(5))
        n = n.remove(5)
        self.assertEqual(n, nullNode)
        with self.assertRaises(KeyError):
            n.remove(6)

    def test_remove_root(self):
        n = ItemNode(4,
                     ItemNode(3),
                     ItemNode(5))
        n = n.remove(4)
        self.assertTrue(n == ItemNode(3, nullNode, ItemNode(5))
                        or n == ItemNode(5, ItemNode(3), nullNode))

    def test_remove(self):
        t = AvlTree([10, 48, 29, 21])
        self.assertEqual(list(iter(t)), [10, 21, 29, 48])
        t.remove(29)
        self.assertEqual(list(iter(t)), [10, 21, 48])
        t.remove(10)
        with self.assertRaises(KeyError):
            t.remove(20)
        self.assertEqual(list(iter(t)), [21, 48])
        t.remove(21)
        t.remove(48)
        self.assertEqual(list(iter(t)), [])

if __name__ == "__main__":
    unittest.main()
