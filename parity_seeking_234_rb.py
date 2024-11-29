from utils import *
from parity_seeking_23_rb import RB23Tree, left_rotate23, right_rotate23, parity_seeking_fixup


class RB234Tree(RB23Tree):
    # Trida reprezentujici klasickou variantu cerveno-cerneho stromu,
    # misto standardni operace Delete se pouziva Parity-Seeking algoritmus.
    # Z duvodu odlisne operace Rotate (viz parity_seeking_23_rb.py) je 
    # potreba mirna modifikace insert, ktera spravne nastavi barvy uzlu
    pass


def rb234_insert(T: RB234Tree, key: int) -> None:
    # Vlozi do stromu T uzel s klicem key
    x = create_node(T, key)
    z = T.root
    y = T.NIL
    while z != T.NIL:
        y = z
        if x.key < z.key:
            z = z.left
        else:
            z = z.right
    x.p = y
    if y == T.NIL:
        T.root = x
    elif x.key < y.key:
        y.left = x
    else:
        y.right = x
    rb234_insert_fixup(T, x)


def rb234_insert_fixup(T: RB234Tree, x: RBNode) -> None:
    # Provadi korekci po vlozeni uzlu do stromu
    while x.p.color == RED:
        if x.p == x.p.p.left:
            y = x.p.p.right
            if y.color == RED:
                color_flip(T, x.p.p)        # pripad 1
                x = x.p.p                   # pripad 1
            else:
                if x == x.p.right:      
                    x = x.p                 # pripad 2
                    left_rotate23(T, x)     # pripad 2
                right_rotate23(T, x.p.p)    # pripad 3

        else:                               # symetricky vuci IF vetvi
            y = x.p.p.left
            if y.color == RED:
                color_flip(T, x.p.p)        # pripad 1
                x = x.p.p                   # pripad 1
            else:
                if x == x.p.left:      
                    x = x.p                 # pripad 2
                    right_rotate23(T, x)    # pripad 2
                left_rotate23(T, x.p.p)     # pripad 3
    T.root.color = BLACK


def rb234_delete(T: RB234Tree, key: int) -> None:
    # Smaze uzel s klicem key, predpokladame ze existuje
    z = search_node(T, key)
    y = z
    y_original_color = y.color
    if z.left == T.NIL:
        x = z.right
        rb_transplant(T, z, z.right)
    elif z.right == T.NIL:
        x = z.left
        rb_transplant(T, z, z.left)
    else:
        y = minimum(T, z.right)
        y_original_color = y.color
        x = y.right
        if y != z.right:
            rb_transplant(T, y, y.right)
            y.right = z.right
            y.right.p = y
        else:
            x.p = y
        rb_transplant(T, z, y)
        y.left = z.left
        y.left.p = y
        y.color = z.color
    if y_original_color == BLACK:
        parity_seeking_fixup(T, x)

     