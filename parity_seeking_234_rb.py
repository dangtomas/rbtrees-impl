from utils import RED, BLACK, RBNode, create_node, color_flip
from parity_seeking_delete import \
    ParitySeekingRBTree, left_rotate23, right_rotate23


class RB234Tree(ParitySeekingRBTree):
    # Trida reprezentujici klasickou variantu cerveno-cerneho stromu,
    # misto standardni operace Delete se pouziva Parity-Seeking algoritmus.
    # Z duvodu odlisne operace Rotate (viz parity_seeking_delete.py) je
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
