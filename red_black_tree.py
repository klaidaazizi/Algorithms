"""
Implementation of a red black tree
Tree properties:
1. Every node is either red or black
2. The root is always black
3. Every leaf is black
4. If a node is red, then both its children are black
5. All paths from a node to descendant nodes contain the same number of black nodes
"""
import math
import time
from random import randint

class RBNode:
    # constructor of an individual node in RBT
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.parent = None
        self.red = False

    def __str__(self):
        return f'{self.key}'  # returns key of RBT node


class RBTree:
    def __init__(self):
        self.nil = RBNode(0)
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
        self.nil.red = False

    # search tree starting from starting node
    def search_helper(self, node, key):
        while node != self.nil and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if node == self.nil:
            print("Couldn't find given key.")
        else:
            print(f"Found node with key {node}")
        return node

    def search(self, key):
        '''
        Searches for a given key in the tree
        :param key: given key
        :return: node with key or None
        '''
        return self.search_helper(self.root, key)

    def minimum(self, node):
        '''
        Determines the minimum value in the RB tree
        :param node: starting node
        :return: minimum node
        '''
        while node.left != self.nil:
            node = node.left
        return node

    def maximum(self, node):
        '''
        Determines the maximum value in the RB tree
        :param node: starting node
        :return: maximum node
        '''
        while node.right != self.nil:
            node = node.right
        return node

    def successor(self, node):
        '''
        Determines the successor of given node, that is the node with smallest key greater than node.key
        :param node: given node
        :return: successor node
        '''
        if node.right != self.nil:
            return self.minimum(node.right)
        parent = node.parent
        while parent != self.nil and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    def predecessor(self, node):
        '''
        Determines the predecessor of given node, that is the node with largest key smaller than node.key
        :param node: given node
        :return: predecessor node
        '''
        if node.left != self.nil:
            return self.maximum(node.left)

        parent = node.parent
        while parent != self.nil and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    def sort(self, node):
        '''
        Returns a sorted array of tree keys
        :param node: starting node
        :return: array of sorted keys
        '''
        sorted_list = []
        if node == self.nil:
            return
        self.sort(node.left)
        print(node.key)
        self.sort(node.right)
        # print(sorted_list)
        return sorted_list

    def rotate_left(self, x):
        '''
        Pivots around the link from x to y
        :param x:
        :return: rotated subtree
        '''
        y = x.right
        x.right = y.left  # turn y's left subtree into x's right subtree
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent  # link x's parent to y
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x  # put x on y's left
        x.parent = y

    def rotate_right(self, x):
        '''
        Pivots around the link from y to x
        :param x:
        :return: rotated subtree
        '''
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def insert(self, key):
        '''
        Inserts a new RBNode into the RBTree and then calls fix_insert to fix the tree and return a balanced tree
        :param key: new key
        :return: balanced RBTree
        '''
        node = RBNode(key)
        node.left = self.nil
        node.right = self.nil
        node.key = key
        node.parent = None
        node.red = True  # new node is always red

        current = self.root
        parent = None

        while current != self.nil:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        if node.parent is None:
            node.red = False
            return

        if node.parent.parent is None:
            return

        # fix tree after inserting new node
        self.fix_insert(node)

    def fix_insert(self, z):
        '''
        Balances the tree after inserting a new node
        :param node: given new node
        :return: balanced RBTree
        '''
        while z.parent.red:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                # Case 1
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                # Case 2
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.rotate_left(z)
                    # Case 3
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                # Case 1
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                # Case 2
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rotate_right(z)
                    # Case 3
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.rotate_left(z.parent.parent)
            if z == self.root:
                break
        self.root.red = False

    def height(self, node):
        if node == self.nil:
            return -1
        return max(self.height(node.left), self.height(node.right)) + 1

    def display(self):
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root.
        Credit: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        """

        # No child.
        if node.right is self.nil and node.left is self.nil:
            line = '%s' % node.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is self.nil:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s' % node.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is self.nil:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s' % node.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s' % node.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

# returns a list of numbers from a given file
def get_nums(file):
    with open(file, "r") as numbers:
        return numbers.readline().split(",")

# Main for testing (Creates rbt from file with numbers and asks user for choice)
def main():
    bst = RBTree()
    numbers = get_nums("numbers.txt")
    size = len(numbers)
    option = ""
    size = 1000
    for i in range(size):
        bst.insert(randint(1, 1000))
    print("Height of tree: ", bst.height(bst.root))
    print("Height should be at most: 2log(n+1) :", 2 * math.log2(size + 1))
    bst.display()
    option = ""
    while option != "Q":
        option = input("Choose an option: \n A: Search value \n B: Sort \n C: Find minimum \n D: Find maximum"
                       " \n E: Insert value \n  F: Print tree \n Q: Quit \n")
        if option == "A":
            value = input("What value are you searching for? \n")
            bst.search(int(value))
        elif option == "B":
            print(bst.sort(bst.root))
        elif option == "C":
            print(bst.minimum(bst.root))
        elif option == "D":
            print(bst.maximum(bst.root))
        elif option == "E":
            value = input("What value would you like to insert? \n")
            bst.insert(int(value))
            print(bst.height(bst.root))
        elif option == "F":
            print(bst)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
