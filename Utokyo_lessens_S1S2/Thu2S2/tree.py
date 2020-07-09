class  Tree():
    def __init__(self, name):
        self.kind = "鳥類"
        self.name = name
 
    def whats_bird(self):
        print(self.name, self.kind)
 
duck = Bird("アヒル")
duck.whats_bird()
crow = Bird("カラス")
crow.whats_bird()


from graphviz import *
def export_graphviz_tree(tree, filename='tree'):
    """graphvizで木構造の画像を生成する
    Treeの属性
    ------------
    root: Node
        treeの根ノード
        
    Nodeの属性
    ------------
    num: int
        ノード番号
    child: Node
        子ノード
    brother: Node
        兄弟のノード(木構造で考えると右側のノード)
    parent: Node
        親ノード
    """

    # 有向グラフの初期化
    G = Digraph(format='png')
    G.attr('node', shape='circle')

    nodes = __gen_nodes(tree.root)

    for node in nodes:
        # ノードの生成
        G.node("node"+str(node.num))
        if node.parent is not None:
            # ノードとノードを繋げる
            G.edge("node"+str(node.parent.num), "node"+str(node.num))

    print(G)
    G.render(filename)

def __gen_nodes(root): # 全ノードを走査するジェネレータ
        if root is not None:
            yield root
            for node in __gen_nodes(root.brother):
                yield node
            for node in __gen_nodes(root.child):
                yield node