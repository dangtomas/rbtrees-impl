from utils import RED, BLACK, RBNode, RBTree, bst_delete, bst_insert


class ClassicRBTree(RBTree):
    # Trida reprezentujici klasickou variantu cerveno-cerneho stromu
    # prezentovanou v kapitole 1.
    pass


def left_rotate(T: ClassicRBTree, x: RBNode) -> None:
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


def right_rotate(T: ClassicRBTree, x: RBNode) -> None:
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


def rb_insert(T: ClassicRBTree, key: int) -> None:
    # Vlozi do stromu T uzel s klicem key
    z = bst_insert(T, key)
    rb_insert_fixup(T, z)


def rb_insert_fixup(T: ClassicRBTree, x: RBNode) -> None:
    # Provadi korekci po vlozeni uzlu do stromu
    while x.p.color == RED:
        if x.p == x.p.p.left:
            y = x.p.p.right
            if y.color == RED:
                x.p.color = BLACK       # pripad 1
                y.color = BLACK         # pripad 1
                x.p.p.color = RED       # pripad 1
                x = x.p.p               # pripad 1
            else:
                if x == x.p.right:
                    x = x.p             # pripad 2
                    left_rotate(T, x)   # pripad 2

                x.p.color = BLACK       # pripad 3
                x.p.p.color = RED       # pripad 3
                right_rotate(T, x.p.p)  # pripad 3

        else:                           # symetricky vuci IF vetvi
            y = x.p.p.left
            if y.color == RED:
                x.p.color = BLACK       # pripad 1
                y.color = BLACK         # pripad 1
                x.p.p.color = RED       # pripad 1
                x = x.p.p               # pripad 1
            else:
                if x == x.p.left:
                    x = x.p             # pripad 2
                    right_rotate(T, x)  # pripad 2

                x.p.color = BLACK       # pripad 3
                x.p.p.color = RED       # pripad 3
                left_rotate(T, x.p.p)   # pripad 3
    T.root.color = BLACK


def rb_delete(T: ClassicRBTree, key: int) -> None:
    # Smaze ze stromu T uzel s klicem key, predpokladame ze existuje
    y_original_color, x = bst_delete(T, key)
    if y_original_color == BLACK:
        rb_delete_fixup(T, x)


def rb_delete_fixup(T: ClassicRBTree, x: RBNode) -> None:
    # Provadi korekci po smazani uzlu
    while x != T.root and x.color == BLACK:
        if x == x.p.left:
            w = x.p.right
            if w.color == RED:
                w.color = BLACK             # pripad 1
                x.p.color = RED             # pripad 1
                left_rotate(T, x.p)         # pripad 1
                w = x.p.right               # pripad 1
            if w.left.color == BLACK and w.right.color == BLACK:
                w.color = RED               # pripad 2
                x = x.p                     # pripad 2
            else:
                if w.right.color == BLACK:
                    w.left.color = BLACK    # pripad 3
                    w.color = RED           # pripad 3
                    right_rotate(T, w)      # pripad 3
                    w = x.p.right           # pripad 3

                w.color = x.p.color         # pripad 4
                x.p.color = BLACK           # pripad 4
                w.right.color = BLACK       # pripad 4
                left_rotate(T, x.p)         # pripad 4
                x = T.root                  # pripad 4, ukonceni procedury

        else:                               # symetricky vuci IF vetvi
            w = x.p.left
            if w.color == RED:
                w.color = BLACK             # pripad 1
                x.p.color = RED             # pripad 1
                right_rotate(T, x.p)        # pripad 1
                w = x.p.left                # pripad 1
            if w.right.color == BLACK and w.left.color == BLACK:
                w.color = RED               # pripad 2
                x = x.p                     # pripad 2
            else:
                if w.left.color == BLACK:
                    w.right.color = BLACK   # pripad 3
                    w.color = RED           # pripad 3
                    left_rotate(T, w)       # pripad 3
                    w = x.p.left            # pripad 3

                w.color = x.p.color         # pripad 4
                x.p.color = BLACK           # pripad 4
                w.left.color = BLACK        # pripad 4
                right_rotate(T, x.p)        # pripad 4
                x = T.root                  # pripad 4, ukonceni procedury
    x.color = BLACK
