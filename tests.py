from typing import TextIO
from utils import RED, BLACK, RBTree, RBNode
from classic_rb import ClassicRBTree, rb_insert, rb_delete
from llrb import LLRBTree, llrb_insert, llrb_delete
from parity_seeking_23_rb import RB23Tree, rb23_insert, rb23_delete
from parity_seeking_234_rb import RB234Tree, rb234_insert, rb234_delete


def rb_test() -> None:
    # test klasicke varianty cerveno-cernych stromu
    T = ClassicRBTree()

    rb_insert(T, 77)
    assert T.root.key == 77
    assert T.root.color == BLACK

    rb_insert(T, 24)
    assert T.root.left.key == 24
    assert T.root.left.color == RED

    rb_insert(T, 49)
    assert T.root.key == 49
    assert T.root.color == BLACK
    assert T.root.left.key == 24
    assert T.root.left.color == RED
    assert T.root.right.key == 77
    assert T.root.right.color == RED

    rb_insert(T, 9)
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    rb_insert(T, 36)
    rb_insert(T, 25)
    assert T.root.left.key == 24
    assert T.root.left.color == RED
    assert T.root.left.left.color == BLACK
    assert T.root.left.right.color == BLACK

    rb_delete(T, 77)
    assert T.root.right.key == 36
    assert T.root.right.color == RED
    assert T.root.left.color == BLACK
    assert T.root.color == BLACK

    rb_delete(T, 25)
    assert T.root.right.color == BLACK
    assert T.root.right.right.color == RED

    rb_delete(T, 9)
    assert T.root.key == 36
    assert T.root.color == BLACK
    assert T.root.left.key == 24
    assert T.root.left.color == BLACK
    assert T.root.right.key == 49
    assert T.root.right.color == BLACK

    print("RBTree - OK")


def llrb_test() -> None:
    T = LLRBTree()

    llrb_insert(T, 25)
    assert T.root.key == 25
    assert T.root.color == BLACK

    llrb_insert(T, 99)
    assert T.root.key == 99
    assert T.root.color == BLACK
    assert T.root.left.color == RED

    llrb_insert(T, 12)
    assert T.root.key == 25
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    llrb_insert(T, 7)
    llrb_insert(T, 20)
    assert T.root.left.color == RED

    llrb_insert(T, 69)
    llrb_insert(T, 40)
    assert T.root.key == 25
    assert T.root.color == BLACK
    assert T.root.right.key == 69
    assert T.root.right.color == BLACK
    assert T.root.left.color == BLACK

    llrb_delete(T, 25)
    assert T.root.key == 40
    assert T.root.color == BLACK
    assert T.root.left.color == RED
    assert T.root.right.key == 99
    assert T.root.right.left.color == RED

    llrb_delete(T, 20)
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.left.left.color == RED

    llrb_delete(T, 40)
    assert T.root.color == BLACK
    assert T.root.key == 69
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    llrb_delete(T, 99)
    assert T.root.key == 12
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    llrb_delete(T, 7)
    assert T.root.key == 69
    assert T.root.right == T.NIL
    assert T.root.left.key == 12
    assert T.root.left.color == RED

    llrb_delete(T, 69)
    assert T.root.key == 12
    assert T.root.color == BLACK

    print("LLRBTree - OK")


def rb23_test() -> None:
    # test 2-3 varianty cerveno-cernych stromu
    T = RB23Tree()

    rb23_insert(T, 69)
    assert T.root.key == 69
    assert T.root.color == BLACK
    assert T.root.left == T.NIL

    rb23_insert(T, 44)
    assert T.root.color == BLACK
    assert T.root.left.color == RED

    rb23_insert(T, 52)
    assert T.root.key == 52
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    rb23_insert(T, 99)
    rb23_insert(T, 77)
    assert T.root.right.key == 77
    assert T.root.right.color == RED
    assert T.root.right.left.color == BLACK
    assert T.root.right.right.color == BLACK

    rb23_insert(T, 20)
    rb23_insert(T, 48)
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    rb23_delete(T, 52)
    assert T.root.key == 69
    assert T.root.color == BLACK
    assert T.root.right.color == BLACK
    assert T.root.right.right.color == RED
    assert T.root.left.color == RED

    rb23_delete(T, 77)
    assert T.root.key == 69
    assert T.root.color == BLACK
    assert T.root.right.color == BLACK
    assert T.root.left.color == RED

    rb23_delete(T, 48)
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.left.left.color == RED

    rb23_delete(T, 99)
    assert T.root.key == 44
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    rb23_delete(T, 69)
    assert T.root.left.color == RED

    print("2-3 RBTree - OK")


def rb234_test() -> None:
    # test klasicke varianty cerveno-cernych stromu s Parity-Seeking
    # Delete algoritmem
    T = RB234Tree()

    rb234_insert(T, 77)
    assert T.root.key == 77
    assert T.root.color == BLACK

    rb234_insert(T, 24)
    assert T.root.left.key == 24
    assert T.root.left.color == RED

    rb234_insert(T, 49)
    assert T.root.key == 49
    assert T.root.color == BLACK
    assert T.root.left.key == 24
    assert T.root.left.color == RED
    assert T.root.right.key == 77
    assert T.root.right.color == RED

    rb234_insert(T, 9)
    assert T.root.color == BLACK
    assert T.root.left.color == BLACK
    assert T.root.right.color == BLACK

    rb234_insert(T, 36)
    rb234_insert(T, 25)
    assert T.root.left.key == 24
    assert T.root.left.color == RED
    assert T.root.left.left.color == BLACK
    assert T.root.left.right.color == BLACK

    rb234_delete(T, 77)
    assert T.root.right.key == 36
    assert T.root.right.color == RED
    assert T.root.left.color == BLACK
    assert T.root.color == BLACK

    rb234_delete(T, 25)
    assert T.root.right.color == BLACK
    assert T.root.right.right.color == RED

    rb234_delete(T, 9)
    assert T.root.key == 36
    assert T.root.color == BLACK
    assert T.root.left.key == 24
    assert T.root.left.color == BLACK
    assert T.root.right.key == 49
    assert T.root.right.color == BLACK

    print("RB234Tree - OK")


# Nasledujici sekvence kodu byla vypujcena ze studijnich materialu predmetu
# IB002 a byla vyuzita pro ladici ucely. Cerveno-cerny strom se pretvori do
# .dot souboru, ktery lze nasledne zobrazit napriklad zde:
# https://dreampuf.github.io/GraphvizOnline

def make_graph(T: RBTree, filename: str) -> None:
    with open(filename, 'w') as dot_file:
        dot_file.write("digraph RBTree {\n")
        dot_file.write("node [style=filled];\n")
        make_graphviz(T.root, dot_file)
        dot_file.write("}\n")


def make_graphviz(node: RBNode, dot_file: TextIO) -> None:
    if node is None or node.key == -1:
        return

    if node.color == RED:
        color = "color=red"
    else:
        color = "color=black,fontcolor=white"

    dot_file.write('"{}" [{},label="{}"]\n'.format(id(node), color, node.key))

    for child, side in (node.left, 'L'), (node.right, 'R'):
        if child is not None and child.key != -1:
            dot_file.write('"{}" -> "{}"\n'.format(id(node), id(child)))
            make_graphviz(child, dot_file)
        else:
            dot_file.write('{nil} [label="",color=white]\n{node} -> {nil}\n'
                           .format(node=id(node), nil=side + str(id(node))))


if __name__ == "__main__":
    rb_test()
    llrb_test()
    rb23_test()
    rb234_test()
    print("---------------")
    print("Vsechny testy OK")
