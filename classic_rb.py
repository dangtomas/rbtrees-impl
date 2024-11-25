# Standardni varianta cerveno-cernych stromu prezentovana v kapitole 1.


# definice barev
RED = True
BLACK = False


class RBNode:
    # Trida reprezentujici uzel v cerveno-cernem strome.

    # Atributy:
    #   key   - hodnota klice uzlu
    #   color - barva uzlu, cervena nebo cerna
    #   left  - odkaz na leveho potomka (syna)
    #   right - odkaz na praveho potomka (syna)
    #   p     - odkaz na rodice (otce)

    def __init__(self, key: int) -> None:
        self.key = key
        self.color = BLACK
        self.right: RBNode = self
        self.left: RBNode  = self
        self.p: RBNode = self


class RBTree:
    # Trida reprezentujici cerveno-cerny strom.

    # Atributy:
    #   NIL   - cerny uzel s klicem None, reprezentujici vsechny listy stromu
    #   root  - koren stromu

    def __init__(self) -> None:
        # NIL uzel nema zadnou hodnotu klice, z duvodu usnadneni typove kontroly 
        # pouzivame -1 misto None
        self.NIL = RBNode(-1) 
        self.root = self.NIL


def create_node(T: RBTree, key: int) -> RBNode:
    # Vytvori a vrati novy uzel, ktery se nasledne vlozi do stromu T
    new = RBNode(key)
    new.left = T.NIL
    new.right = T.NIL
    new.p = T.NIL
    return new


def search_node(T: RBTree, key: int) -> RBNode:
    # Vrati uzel s klicem key ve strome T pokud existuje, jinak vrati T.NIL
    x = T.root
    while x != T.NIL:
        if key == x.key:
            return x
        elif key < x.key:
            x = x.left
        else:
            x = x.right
    return x


def minimum(T: RBTree, x: RBNode) -> RBNode:
    # Najde ve strome T minimalni uzel v podstrome s korenem x
    while x.left != T.NIL:
        x = x.left
    return x


def left_rotate(T: RBTree, x: RBNode) -> None:
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


def right_rotate(T: RBTree, x: RBNode) -> None:
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
        

def rb_insert(T: RBTree, key: int) -> None:
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
    x.color = RED
    rb_insert_fixup(T, x)


def rb_insert_fixup(T: RBTree, x: RBNode) -> None:
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


def rb_transplant(T: RBTree, u: RBNode, v: RBNode) -> None:
    # Nahradi ve strome T podstrom s korenem u podstromem s korenem v
    if u.p == T.NIL:
        T.root = v
    elif u == u.p.left:
        u.p.left = v
    else:
        u.p.right = v
    v.p = u.p


def rb_delete(T: RBTree, key: int) -> None:
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
        rb_delete_fixup(T, x)


def rb_delete_fixup(T: RBTree, x: RBNode) -> None:
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


