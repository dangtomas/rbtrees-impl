from utils import *


class LLRBTree(RBTree):
    # Trida reprezentujici LLRB variantu 2-3 cerveno-cernych stromu
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


def llrb_insert(T: LLRBTree, key: int) -> None:
    # Vlozi do stromu T uzel s klicem key
    x = create_node(T, key)
    T.root = llrb_insert_rec(T, T.root, x)
    T.root.color = BLACK


def llrb_insert_rec(T: LLRBTree, h: RBNode, x: RBNode) -> RBNode:
    # Rekurzivni cast operace insert
    if h == T.NIL:
        return x
    if x.key < h.key:
        h.left = llrb_insert_rec(T, h.left, x)
    else:
        h.right = llrb_insert_rec(T, h.right, x)
    if h.left.color != RED and h.right.color == RED:
        h = llrb_left_rotate(T, h)
    if h.left.color == RED and h.left.left.color == RED:
        h = llrb_right_rotate(T, h)
    if h.left.color == RED and h.right.color == RED:
        color_flip(T, h)
    return h


def move_red_left(T: LLRBTree, h: RBNode) -> RBNode:
    # Zaridi, aby v levem podstrome existoval cerveny uzel
    color_flip(T, h)
    if h.right.left.color == RED:
        h.right = llrb_right_rotate(T, h.right)
        h = llrb_left_rotate(T, h)
        color_flip(T, h)
    return h


def move_red_right(T: LLRBTree, h: RBNode) -> RBNode:
    # Zaridi, aby v pravem podstrome existoval cerveny uzel
    color_flip(T, h)
    if h.left.left.color == RED:
        h = llrb_right_rotate(T, h)
        color_flip(T, h)
    return h


def llrb_delete_fixup(T: LLRBTree, h: RBNode) -> RBNode:
    # Provadi korekci po smazani uzlu, jedna se o stejne 3 podminky
    # jako na konci funkce llrb_insert_rec
    if h.left.color != RED and h.right.color == RED:
        h = llrb_left_rotate(T, h)
    if h.left.color == RED and h.left.left.color == RED:
        h = llrb_right_rotate(T, h)
    if h.left.color == RED and h.right.color == RED:
        color_flip(T, h)
    return h


def llrb_delete_min(T: LLRBTree, h: RBNode) -> RBNode:
    # Smaze minimalni uzel v podstrome s korenem x
    if h.left == T.NIL:
        return T.NIL
    if h.left.color != RED and h.left.left.color != RED:
        h = move_red_left(T, h)
    h.left = llrb_delete_min(T, h.left)
    return llrb_delete_fixup(T, h)


def llrb_delete(T: LLRBTree, key: int) -> None:
    # Smaze uzel s klicem key, predpokladame ze existuje
    T.root = llrb_delete_rec(T, T.root, key)
    T.root.color = BLACK


def llrb_delete_rec(T: LLRBTree, h: RBNode, key: int) -> RBNode:
    # Rekurzivni cast operace delete 
    if key < h.key:
        if h.left.color != RED and h.left.left.color != RED:
            h = move_red_left(T, h)
        h.left = llrb_delete_rec(T, h.left, key)
    else:
        if h.left.color == RED:
            h = llrb_right_rotate(T, h)
        if key == h.key and h.right == T.NIL:
            return T.NIL
        if h.right.color != RED and h.right.left.color != RED:
            h = move_red_right(T, h)
        if key == h.key:
            h.key = minimum(T, h.right).key
            h.right = llrb_delete_min(T, h.right)
        else:
            h.right = llrb_delete_rec(T, h.right, key)
    return llrb_delete_fixup(T, h)




