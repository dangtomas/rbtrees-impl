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
    #   p     - odkaz na rodice (otce), v LLRB strome neni potreba

    def __init__(self, key: int) -> None:
        self.key = key
        self.color = BLACK
        self.right: RBNode = self
        self.left: RBNode  = self
        self.p: RBNode = self


class RBTree:
    # Trida reprezentujici obecny cerveno-cerny strom.

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
    new.color = RED
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


def color_flip(T: RBTree, x: RBNode) -> None:
    # Prohodi barvy rodice s jeho potomky
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    x.color = not x.color
    x.left.color = not x.left.color
    x.right.color = not x.right.color


def rb_transplant(T: RBTree, u: RBNode, v: RBNode) -> None:
    # Nahradi ve strome T podstrom s korenem u podstromem s korenem v
    if u.p == T.NIL:
        T.root = v
    elif u == u.p.left:
        u.p.left = v
    else:
        u.p.right = v
    v.p = u.p