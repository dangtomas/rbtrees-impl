# Klasicka varianta cerveno-cernych stromu, misto klasicke procedury Delete se pouziva 
# Parity-Seeking algoritmus.


# definice barev
RED = True
BLACK = False


class RB234Node:
    # Trida reprezentujici uzel v klasickem 2-3-4 cerveno-cernem strome.

    # Atributy:
    #   key   - hodnota klice uzlu
    #   color - barva uzlu, cervena nebo cerna
    #   left  - odkaz na leveho potomka (syna)
    #   right - odkaz na praveho potomka (syna)
    #   p     - odkaz na rodice (otce)

    def __init__(self, key: int) -> None:
        self.key = key
        self.color = BLACK
        self.right: RB234Node = self
        self.left: RB234Node  = self
        self.p: RB234Node = self


class RB234Tree:
    # Trida reprezentujici 2-3 cerveno-cerny strom.

    # Atributy:
    #   NIL   - cerny uzel, nema zadnou hodnotu klice, reprezentuje vsechny listy stromu
    #   root  - koren stromu

    def __init__(self) -> None:
        # NIL uzel nema zadnou hodnotu klice, z duvodu usnadneni typove kontroly 
        # pouzivame -1 misto None
        self.NIL = RB234Node(-1) 
        self.root = self.NIL


def create_node(T: RB234Tree, key: int) -> RB234Node:
    # Vytvori a vrati novy uzel, ktery se nasledne vlozi do stromu T
    new = RB234Node(key)
    new.left = T.NIL
    new.right = T.NIL
    new.p = T.NIL
    return new


def search_node(T: RB234Tree, key: int) -> RB234Node:
    # Vrati uzel s klicem key ve strome T pokud existuje, jinak vrati T.NIL
    x = T.root
    while x != T.NIL:
        if key == x.key:
            return x
        elif key < x.key:
            x = x.left
        else:
            x = x.right
    return T.NIL


def minimum(T: RB234Tree, x: RB234Node) -> RB234Node:
    # Najde ve strome T minimalni uzel v podstrome s korenem x
    while x.left != T.NIL:
        x = x.left
    return x


def left_rotate234(T: RB234Tree, x: RB234Node) -> None:
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


def right_rotate234(T: RB234Tree, x: RB234Node) -> None:
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


def color_flip(T: RB234Tree, x: RB234Node) -> None:
    # Prohodi barvy rodice s jeho potomky
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    x.color = not x.color
    x.left.color = not x.left.color
    x.right.color = not x.right.color


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
    x.color = RED
    rb234_insert_fixup(T, x)


def rb234_insert_fixup(T: RB234Tree, x: RB234Node) -> None:
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
                    left_rotate234(T, x)    # pripad 2
                right_rotate234(T, x.p.p)   # pripad 3

        else:                               # symetricky vuci IF vetvi
            y = x.p.p.left
            if y.color == RED:
                color_flip(T, x.p.p)        # pripad 1
                x = x.p.p                   # pripad 1
            else:
                if x == x.p.left:      
                    x = x.p                 # pripad 2
                    right_rotate234(T, x)   # pripad 2
                left_rotate234(T, x.p.p)    # pripad 3
    T.root.color = BLACK


def rb_transplant(T: RB234Tree, u: RB234Node, v: RB234Node) -> None:
    # Nahradi ve strome T podstrom s korenem u podstromem s korenem v
    if u.p == T.NIL:
        T.root = v
    elif u == u.p.left:
        u.p.left = v
    else:
        u.p.right = v
    v.p = u.p


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


def parity_seeking_fixup(T: RB234Tree, x: RB234Node) -> None:
    # Provadi korekci po smazani uzlu
    while x != T.root and x.color == BLACK:
        if x == x.p.left:
            y = x.p.right
        else:
            y = x.p.left
        if y.color == RED:
            if x == x.p.left:
                left_rotate234(T, x.p)          # pripad 3
            else:
                right_rotate234(T, x.p)         # pripad 3
        else:
            y.color = RED                       # pripad 2
            x = x.p                             # pripad 2
            x = case2_fixup(T, x, y)            # pripad 2
    x.color = BLACK                             # pripad 1


def case2_fixup(T: RB234Tree, x: RB234Node, z: RB234Node) -> RB234Node:
    # Provadi korekci po provedeni pripadu 2
    if (z.left.color == RED or z.right.color == RED):
        if z == x.left:
            if z.left.color == BLACK:
                left_rotate234(T, z)
            right_rotate234(T, x)
            x = x.p
        else:
            if z.right.color == BLACK:
                right_rotate234(T, z)
            left_rotate234(T, x)
            x = x.p
        x.left.color = BLACK
        x.right.color = BLACK
        x = T.root
    return x