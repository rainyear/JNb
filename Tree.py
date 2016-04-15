from graphviz import Graph, Digraph
import sys
from uuid import uuid1

__all__ = ['Tree2', 'visit', 'draw_edges']

class Tree(object):
    """二叉树，定义递归遍历方法
    """
    _visit = lambda node: sys.stdout.write("{} ".format(node.data))
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        
        # _nid as node id 
        self._nid = str(id(self))
    def pre_order_recursive(self, visit=None):
        if not visit:
            visit = type(self)._visit
        if self:
            visit(self)
        if self.left:
            self.left.pre_order_recursive(visit)
        if self.right:
            self.right.pre_order_recursive(visit)
    def in_order_recursive(self, visit=None):
        if not visit:
            visit = type(self)._visit
        if self.left:
            self.left.in_order_recursive(visit)
        if self:
            visit(self)
        if self.right:
            self.right.in_order_recursive(visit)
    def post_order_recursive(self, visit=None):
        if not visit:
            visit = type(self)._visit
        if self.left:
            self.left.post_order_recursive(visit)
        if self.right:
            self.right.post_order_recursive(visit)
        if self:
            visit(self)
def build_tree(lst, leaf="@", klass=Tree):
    """从列表生成树，按照前序遍历的顺序，其中以 leaf 标记为叶子
    """
    if len(lst) == 0:
        return None
    data = lst.pop(0)
    if data == leaf:
        return None
    root = klass(data = data)
    root.left = build_tree(lst, klass=klass)
    root.right = build_tree(lst, klass=klass)
    return root 
class Tree2(Tree):
    def __init__(self, data=None, left=None, right=None):
        super().__init__(data=data, left=left, right=right)
    def draw(self):
        def mk_node(node):
            graph.node(node._nid, str(node.data))
        # 绘制空节点
        def mk_leaf(nid):
            leaf = str(uuid1())
            graph.node(leaf, '@', style='invis')
            graph.edge(nid, leaf, style='invis')
        # 绘制边
        def draw_edges(parent):
            if parent.left:
                graph.edge(parent._nid, parent.left._nid)
                draw_edges(parent.left)
            else:
                mk_leaf(parent._nid)
            if parent.right:
                graph.edge(parent._nid, parent.right._nid)
                draw_edges(parent.right)
            else:
                mk_leaf(parent._nid)
        graph = Digraph(
                      comment="Tree",
                      name="Tree",
                      graph_attr=dict(size='8,8', nodesep='0.5', ranksep='0.5'),
                      node_attr=dict(shape='circle',
                                     style='filled',
                                     color='none',
                                     fontname='Courier',
                                     fontcolor='white',
                                     fontsize='16',
                                     fillcolor='#3A76A7'),
                      edge_attr=dict(color='#3A76A7', arrowsize='0.4'))

        # 通过递归前序遍历创建树的所有节点
        self.pre_order_recursive(mk_node)
        
        draw_edges(self)
        return graph
def visit(queue):
    return lambda node: queue.append(node)
def draw_edges(root, queue, graph = None, **edge_attr):
    if len(queue) == 0:
        return
    if not graph:
        graph = root.draw()
    root = queue.pop(0)
    
    # hide original edges
    graph.edge_attr['style'] = 'invis'
    step = 0
    while len(queue):
        node = queue.pop(0)
        attr = dict(arrowhead='vee',
                    arrowsize='0.8',
                        style='dashed',
                        color='#F37626',
                        label=' {}'.format(step),
                        constraint="false")
        attr.update(edge_attr)
        graph.edge(root._nid, node._nid, **attr)
        root = node
        step += 1
    return graph