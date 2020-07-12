# Bill Wang
# 2020-07-10


class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0


class AVLTree(object):
    def __init__(self):
        self.root = None

    def pre_order_T(self, root):
        if root != None:
            print(root.key, end='')
            print(' ', end='')
            self.pre_order_T(root.left)
            self.pre_order_T(root.right)
        else:
            return 0

    def in_order_T(self, root):
        if root != None:
            self.in_order_T(root.left)
            print(root.key, end='')
            print(' ', end='')
            self.in_order_T(root.right)
        else:
            return 0

    def post_order_T(self, root):
        if root != None:
            self.post_order_T(root.left)
            self.post_order_T(root.right)
            print(root.key, end='')
            print(' ', end='')
        else:
            return 0

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    def update_height(self, node):
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def unbalance(self, node):
        return abs(self.height(node.left) - self.height(node.right)) >= 2

    """LL"""
    def right_rotate(self, node):
        node_right = node
        node = node.left
        node_right.left = node.right
        node.right = node_right

        self.update_height(node_right)
        self.update_height(node)

        return node

    """RR"""
    def left_rotate(self, node):
        node_left = node
        node = node.right
        node_left.right = node.left
        node.left = node_left

        self.update_height(node_left)
        self.update_height(node)

        return node

    """LR"""
    def left_right_rotate(self, node):
        node.left = self.left_rotate(node.left)
        return self.right_rotate(node)

    """RL"""
    def right_left_rotate(self, node):
        node.right = self.right_rotate(node.right)
        return self.left_rotate(node)

    def _insert(self, key, node):
        if node is None:
            node = Node(key)

        elif key < node.key:  # left insert
            node.left = self._insert(key, node.left)
            if self.unbalance(node):
                if key < node.left.key:  # LL
                    node = self.right_rotate(node)
                else:  # LR
                    node = self.left_right_rotate(node)

        elif key > node.key:  # right insert
            node.right = self._insert(key, node.right)
            if self.unbalance(node):
                if key < node.right.key:  # LR
                    node = self.right_left_rotate(node)
                else:  # RR
                    node = self.left_rotate(node)

        self.update_height(node)

        return node

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self.root = self._insert(key, self.root)

    def _delete(self, key, node):
        if node == None:
            print("Can't find %d" % key)
            return node

        elif key < node.key:
            node.left = self._delete(key, node.left)  # find in the left subtree
            if self.unbalance(node):  # if right - left > 1
                if self.height(node.right.left) > self.height(node.right.right):
                    node = self.right_left_rotate(node)
                else:
                    node = self.left_rotate(node)
            self.update_height(node)

        elif key > node.key:
            node.right = self._delete(key, node.right)  # find in the right subtree
            if self.unbalance(node):  # if left - right > 1
                if self.height(node.left.right) > self.height(node.left.left):
                    node = self.left_right_rotate(node)
                else:
                    node = self.right_rotate(node)
            self.update_height(node)

        elif node.key == key:
            if node.left and node.right:  # if both right/left nodes exist
                if self.height(node.left) >= self.height(node.right):  # if left height >= right
                    # find the very right node, return and delete it
                    max_node = node.left
                    while max_node.right != None:
                        max_node = max_node.right
                    node.key = max_node.key
                    node.left = self._delete(node.key, node.left)
                else:  # if right height > left
                    # find the very left node, return and delete it
                    min_node = node.right
                    while min_node.left != None:
                        min_node = min_node.left
                    node.key = min_node.key
                    node.right = self._delete(node.key, node.right)
                self.update_height(node)
            else:
                if node.left:  # if only has left, copy it
                    node = node.left
                elif node.right:  # if only has right, copy it
                    node = node.right
                else:
                    node = None

        return node

    def delete(self, key):
        self.root = self._delete(key, self.root)

    def print_by_layer(self, t):
        n = len(t) - 1
        for i in range(1, n - 1):
            for j in range(2 * i):
                if t[i][j] == '.':
                    t[i + 1].insert(j + 1, '.')
                    t[i + 1].insert(j + 1, '.')
        result = []
        result.append('       {}       '.format(t[0][0]))
        result.append('    /     \\    ')
        result.append('   {}       {}   '.format(t[1][0], t[1][1]))
        result.append('  / \\     / \\  ')
        result.append(' {}   {}   {}   {} '.format(*t[2]))
        result.append('/ \\ / \\ / \\ / \\')
        result.append(' '.join([str(i) for i in t[3]]))
        for i in result[:2 * n - 1]:
            print(i)

    def layer_order_T(self, root):
        if not root:
            return []
        result_list = []
        cur_layer = [root]
        while cur_layer:
            cur_print = []
            next_layer = []
            for node in cur_layer:
                if node == '.':
                    cur_print.append('.')
                else:
                    cur_print.append(node.key)
                    if node.left:
                        next_layer.append(node.left)
                    else:
                        next_layer.append('.')
                    if node.right:
                        next_layer.append(node.right)
                    else:
                        next_layer.append('.')
            result_list.append(cur_print)
            cur_layer = next_layer
        return result_list

    def printTree(self):
        layer_order_arr = self.layer_order_T(self.root)
        self.print_by_layer(layer_order_arr)


def main():

    Tree = AVLTree()
    input = [12, 4, 1, 3, 7, 8, 10, 9, 2, 11, 6, 5]

    for i in input:
        Tree.insert(i)
        # Tree.in_order_T(Tree.root)
        # print('\n')

    Tree.printTree()
    Tree.delete(10)
    # Tree.delete(4)
    # Tree.delete(7)
    Tree.printTree()


if __name__ == '__main__':
    main()
