# 2-3 varianta cerveno-cernych stromu prezentovana v kapitole 3.
# K implementaci Delete se pouziva Parity-Seeking algoritmus.


# definice barev
RED = True
BLACK = False


class RB23Node:
    # Trida reprezentujici uzel v 2-3 cerveno-cernem strome.

    # Atributy:
    #   key   - hodnota klice uzlu
    #   color - barva uzlu, cervena nebo cerna
    #   left  - odkaz na leveho potomka (syna)
    #   right - odkaz na praveho potomka (syna)
    #   p     - odkaz na rodice (otce)

    def __init__(self, key: int) -> None:
        self.key = key
        self.color = BLACK
        self.right: RB23Node = self
        self.left: RB23Node  = self
        self.p: RB23Node = self


class RB23Tree:
    # Trida reprezentujici 2-3 cerveno-cerny strom.

    # Atributy:
    #   NIL   - cerny uzel, nema zadnou hodnotu klice, reprezentuje vsechny listy stromu
    #   root  - koren stromu

    def __init__(self) -> None:
        # NIL uzel nema zadnou hodnotu klice, z duvodu usnadneni typove kontroly 
        # pouzivame -1 misto None
        self.NIL = RB23Node(-1) 
        self.root = self.NIL


def create_node(T: RB23Tree, key: int) -> RB23Node:
    # Vytvori a vrati novy uzel, ktery se nasledne vlozi do stromu T
    new = RB23Node(key)
    new.left = T.NIL
    new.right = T.NIL
    new.p = T.NIL
    return new


def search_node(T: RB23Tree, key: int) -> RB23Node:
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


def minimum(T: RB23Tree, x: RB23Node) -> RB23Node:
    # Najde ve strome T minimalni uzel v podstrome s korenem x
    while x.left != T.NIL:
        x = x.left
    return x


def left_rotate23(T: RB23Tree, x: RB23Node) -> None:
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


def right_rotate23(T: RB23Tree, x: RB23Node) -> None:
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


def color_flip(T: RB23Tree, x: RB23Node) -> None:
    # Prohodi barvy rodice s jeho potomky
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    x.color = not x.color
    x.left.color = not x.left.color
    x.right.color = not x.right.color


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
    x.color = RED
    rb23_insert_fixup(T, x)


def rb23_insert_fixup(T: RB23Tree, x: RB23Node) -> None:
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


def rb_transplant(T: RB23Tree, u: RB23Node, v: RB23Node) -> None:
    # Nahradi ve strome T podstrom s korenem u podstromem s korenem v
    if u.p == T.NIL:
        T.root = v
    elif u == u.p.left:
        u.p.left = v
    else:
        u.p.right = v
    v.p = u.p


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


def parity_seeking_fixup(T: RB23Tree, x: RB23Node) -> None:
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


def case2_fixup(T: RB23Tree, x: RB23Node, z: RB23Node) -> RB23Node:
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