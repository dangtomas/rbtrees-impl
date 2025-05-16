from utils import RED, BLACK, RBTree, RBNode, bst_delete


class ParitySeekingRBTree(RBTree):
    # Predstavuje obecnou variantu cerveno-cernych stromu, ktere
    # pro operaci Delete vyuzivaji Parity-Seeking algoritmus
    pass


# Tyto rotace jsou popsany v kapitole 3
# Vyuzivaji se jak pro 2-3, tak 2-3-4 cerveno-cerne stromy, ktere pro
# operaci Delete pouzivaji Parity-Seeking algoritmus

def left_rotate23(T: ParitySeekingRBTree, x: RBNode) -> None:
    # Provede rotaci doleva kolem uzlu x
    y = x.right
    x.right = y.left
    if y.left != T.NIL:
        y.left.p = x
    y.p = x.p
    if x.p == T.NIL:
        T.root = y
    elif x == x.p.left:
        x.p.left = y
    else:
        x.p.right = y
    y.left = x
    x.p = y
    y.color = x.color   # je potreba nastavit barvy uzlu
    x.color = RED       # je potreba nastavit barvy uzlu


def right_rotate23(T: ParitySeekingRBTree, x: RBNode) -> None:
    # Provede rotaci doprava kolem uzlu x
    y = x.left
    x.left = y.right
    if y.right != T.NIL:
        y.right.p = x
    y.p = x.p
    if x.p == T.NIL:
        T.root = y
    elif x == x.p.left:
        x.p.left = y
    else:
        x.p.right = y
    y.right = x
    x.p = y
    y.color = x.color  # je potreba nastavit barvy uzlu
    x.color = RED      # je potreba nastavit barvy uzlu


def parity_seeking_delete(T: ParitySeekingRBTree, key: int) -> None:
    # Smaze ze stromu T uzel s klicem key, predpokladame ze existuje
    y_original_color, x = bst_delete(T, key)
    if y_original_color == BLACK:
        parity_seeking_fixup(T, x)


def parity_seeking_fixup(T: ParitySeekingRBTree, x: RBNode) -> None:
    # Provadi korekci po smazani uzlu
    while x != T.root and x.color == BLACK:
        if x == x.p.left:
            y = x.p.right
        else:
            y = x.p.left
        if y.color == RED:
            if x == x.p.left:
                left_rotate23(T, x.p)       # pripad 3
            else:
                right_rotate23(T, x.p)      # pripad 3
        else:
            y.color = RED                   # pripad 2
            x = x.p                         # pripad 2
            x = case2_fixup(T, x, y)        # pripad 2
    x.color = BLACK                         # pripad 1


def case2_fixup(T: ParitySeekingRBTree, x: RBNode, z: RBNode) -> RBNode:
    # Provadi korekci po provedeni pripadu 2
    if (z.left.color == RED or z.right.color == RED):
        if z == x.left:
            if z.left.color == BLACK:
                left_rotate23(T, z)
            right_rotate23(T, x)
        else:
            if z.right.color == BLACK:
                right_rotate23(T, z)
            left_rotate23(T, x)
        x = x.p
        x.left.color = BLACK
        x.right.color = BLACK
        x = T.root
    return x
