class Node:
    def __init__(self,left,right):
        self.left = left
        self.right = right

class Leaf:
    def __init__(self,data):
        self.data = data
    def get(self):
        return self.data
def go_around(tree):
    if isinstance(tree, Leaf):
        return [tree.get()]
    else:
        return go_around(tree.left) + go_around(tree.right)

a = Node(Leaf('hello'), Node(Leaf(','), Leaf('world')))
print(go_around(a))
