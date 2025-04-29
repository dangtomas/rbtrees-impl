from utils import (
    RED, BLACK, RBNode, RBTree,
    create_node, minimum, color_flip
)


class LLRBTree(RBTree):
    # Trida reprezentujici (2-3) LLRB variantu cerveno-cernych stromu
    # prezentovanou v kapitole 2.
    pass


def llrb_left_rotate(T: LLRBTree, x: RBNode):
    # Provede levou rotaci kolem uzlu x
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    y = x.right
    x.right = y.left
    y.left = x
    y.color = x.color
    x.color = RED
    return y


def llrb_right_rotate(T: LLRBTree, x: RBNode):
    # Provede levou rotaci kolem uzlu x
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    y = x.left
    x.left = y.right
    y.right = x
    y.color = x.color
    x.color = RED
    return y


def llrb_fixup(T: LLRBTree, x: RBNode) -> RBNode:
    # Provadi korekci pri vynorovani nahoru
    if x.left.color != RED and x.right.color == RED:
        x = llrb_left_rotate(T, x)
    if x.left.color == RED and x.left.left.color == RED:
        x = llrb_right_rotate(T, x)
    if x.left.color == RED and x.right.color == RED:
        color_flip(T, x)
    return x


def llrb_insert(T: LLRBTree, key: int) -> None:
    # Vlozi do stromu T uzel s klicem key
    z = create_node(T, key)
    T.root = llrb_insert_rec(T, T.root, z)
    T.root.color = BLACK


def llrb_insert_rec(T: LLRBTree, x: RBNode, z: RBNode) -> RBNode:
    # Rekurzivni cast operace Insert
    if x == T.NIL:
        return z
    if z.key < x.key:
        x.left = llrb_insert_rec(T, x.left, z)
    else:
        x.right = llrb_insert_rec(T, x.right, z)
    return llrb_fixup(T, x)


def move_red_left(T: LLRBTree, x: RBNode) -> RBNode:
    # Zaridi, aby v levem podstrome existoval cerveny uzel
    color_flip(T, x)
    if x.right.left.color == RED:
        x.right = llrb_right_rotate(T, x.right)
        x = llrb_left_rotate(T, x)
        color_flip(T, x)
    return x


def move_red_right(T: LLRBTree, x: RBNode) -> RBNode:
    # Zaridi, aby v pravem podstrome existoval cerveny uzel
    color_flip(T, x)
    if x.left.left.color == RED:
        x = llrb_right_rotate(T, x)
        color_flip(T, x)
    return x


def llrb_delete_min(T: LLRBTree, x: RBNode) -> RBNode:
    # Smaze minimalni uzel v podstrome s korenem x
    if x.left == T.NIL:
        return T.NIL
    if x.left.color != RED and x.left.left.color != RED:
        x = move_red_left(T, x)
    x.left = llrb_delete_min(T, x.left)
    return llrb_fixup(T, x)


def llrb_delete(T: LLRBTree, key: int) -> None:
    # Smaze uzel s klicem key, predpokladame ze existuje
    T.root = llrb_delete_rec(T, T.root, key)
    T.root.color = BLACK


def llrb_delete_rec(T: LLRBTree, x: RBNode, key: int) -> RBNode:
    # Rekurzivni cast operace delete
    if key < x.key:
        if x.left.color != RED and x.left.left.color != RED:
            x = move_red_left(T, x)
        x.left = llrb_delete_rec(T, x.left, key)
    else:
        if x.left.color == RED:
            x = llrb_right_rotate(T, x)
        if key == x.key and x.right == T.NIL:
            return T.NIL
        if x.right.color != RED and x.right.left.color != RED:
            x = move_red_right(T, x)
        if key == x.key:
            x.key = minimum(T, x.right).key
            x.right = llrb_delete_min(T, x.right)
        else:
            x.right = llrb_delete_rec(T, x.right, key)
    return llrb_fixup(T, x)
