class AvlNode:
    """Abstract base class for AVL nodes."""

    def __eq__(self, other):
        """Compare nodes by structure. Mostly used by unit tests."""
        if isinstance(other, AvlNode):
            return (self.item == other.item
                    and self.left == other.left
                    and self.right == other.right)
        else:
            return False

    def rotateRight(self):
        """Return the right rotation of this subtree."""
        newRight = ItemNode(
            self.item,
            self.left.right,
            self.right)
        newRoot = ItemNode(
            self.left.item,
            self.left.left,
            newRight)
        return newRoot

    def rotateLeft(self):
        """Return the left rotation of this subtree."""
        newLeft = ItemNode(
            self.item,
            self.left,
            self.right.left)
        newRoot = ItemNode(
            self.right.item,
            newLeft,
            self.right.right)
        return newRoot


class NullNode(AvlNode):
    """Placeholder used by nodes without children. Normally there will be only
    one of these that is reused (null object pattern.) """

    def __init__(self):
        self.item = None
        self.height = 0
        self.left = self
        self.right = self

    def isNull(self):
        return True

    def __eq__(self, other):
        if other.isNull():
            return True
        else:
            return other == self

    def insert(self, item):
        return ItemNode(item)

    def remove(self, item):
        raise KeyError("Item not found", item)

    def __repr__(self):
        return "nullNode"

    def __iter__(self):
        yield from []

nullNode = NullNode()


class ItemNode(AvlNode):

    def __init__(self, item, left=nullNode, right=nullNode):
        self.item = item
        self.left = left
        self.right = right
        self.height = 1 + max(left.height,
                              right.height)

    def isNull(self):
        return False

    def insert(self, item):
        """Insert a new item into this subtree (destructively)
        and return the new root after rebalancing."""
        if item < self.item:
            self.left = self.left.insert(item)
            self.height = max(self.height, self.left.height + 1)
            return self.rebalance()
        elif item > self.item:
            self.right = self.right.insert(item)
            self.height = max(self.height, self.right.height + 1)
            return self.rebalance()
        else:
            return self

    def remove(self, item):
        """Remove (destructively) an item from this subtree and return
        the new root after rebalancing."""
        if self.item == item:
            if self.left.isNull() and self.right.isNull():
                return nullNode
            elif self.left.isNull():
                return self.right
            elif self.right.isNull():
                return self.left
            else:
                # Pull up the in-order successor to the root.
                successor = next(iter(self.right))
                self.right = self.right.remove(successor)
                self.item = successor
                return self.rebalance()
        elif item < self.item:
            self.left = self.left.remove(item)
            return self.rebalance()
        elif item > self.item:
            self.right = self.right.remove(item)
            return self.rebalance()

    def rebalance(self):
        """Rebalance this node if necessary, and return the new root."""
        if self.balance <= -2:
            if self.right.balance > 0:
                self.right = self.right.rotateRight()
            return self.rotateLeft()
        elif self.balance >= 2:
            if self.left.balance < 0:
                self.left = self.left.rotateLeft()
            return self.rotateRight()
        else:
            return self

    @property
    def balance(self):
        return self.left.height - self.right.height

    def __repr__(self):
        return "ItemNode({!r}, {!r}, {!r})".format(
            self.item, self.left, self.right)

    def __iter__(self):
        yield from iter(self.left)
        yield self.item
        yield from iter(self.right)


class AvlTree:
    def __init__(self, seq=[]):
        self.root = NullNode()
        self.update(seq)

    def add(self, item):
        self.root = self.root.insert(item)

    def remove(self, item):
        self.root = self.root.remove(item)

    def update(self, seq):
        for i in seq:
            self.add(i)

    def __repr__(self):
        return "AvlTree({!r})".format(list(iter(self)))

    def __iter__(self):
        yield from iter(self.root)
