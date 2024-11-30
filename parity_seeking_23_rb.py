from utils import RED, BLACK, RBNode, create_node, color_flip
from parity_seeking_delete import \
    ParitySeekingRBTree, left_rotate23, right_rotate23


class RB23Tree(ParitySeekingRBTree):
    # Trida reprezentujici 2-3 variantu cerveno-cerneho stromu
    # prezentovanou v kapitole 3. Operace Delete je implementovana
    # pomoci Parity-Seeking algoritmu.
    pass


def rb23_insert(T: RB23Tree, key: int) -> None:
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
    rb23_insert_fixup(T, x)


def rb23_insert_fixup(T: RB23Tree, x: RBNode) -> None:
    # Provadi korekci po vlozeni uzlu do stromu
    while True:
        if x.p.left.color == RED and x.p.right.color == RED:
            color_flip(T, x.p)                  # case (c)
            x = x.p                             # case (c)
        elif x.p.color == RED:
            if x.p == x.p.p.left:
                if x == x.p.right:
                    x = x.p                     # case (a)
                    left_rotate23(T, x)         # case (a)
                right_rotate23(T, x.p.p)        # case (b)
            else:
                if x.p == x.p.p.right:
                    if x == x.p.left:
                        x = x.p                 # case (a)
                        right_rotate23(T, x)    # case (a)
                    left_rotate23(T, x.p.p)     # case (b)
        else:
            break
    T.root.color = BLACK
