from utils import *
from parity_seeking_234_rb import RB234Tree


class RB23Tree(RBTree):
    # Trida reprezentujici 2-3 variantu cerveno-cerneho stromu prezentovanou v 
    # kapitole 3. Operace Delete je implementovana pomoci Parity-Seeking algoritmu.
    pass
    

def left_rotate23(T: RB23Tree | RB234Tree, x: RBNode) -> None:
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


def right_rotate23(T: RB23Tree | RB234Tree, x: RBNode) -> None:
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
    y.color = x.color # je potreba nastavit barvy uzlu
    x.color = RED     # je potreba nastavit barvy uzlu


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


def rb23_delete(T: RB23Tree, key: int) -> None:
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


def parity_seeking_fixup(T: RB23Tree | RB234Tree, x: RBNode) -> None:
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


def case2_fixup(T: RB23Tree | RB234Tree, x: RBNode, z: RBNode) -> RBNode:
    # Provadi korekci po provedeni pripadu 2
    if (z.left.color == RED or z.right.color == RED):
        if z == x.left:
            if z.left.color == BLACK:
                left_rotate23(T, z)
            right_rotate23(T, x)
            x = x.p
        else:
            if z.right.color == BLACK:
                right_rotate23(T, z)
            left_rotate23(T, x)
            x = x.p
        x.left.color = BLACK
        x.right.color = BLACK
        x = T.root
    return x