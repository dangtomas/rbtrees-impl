# LLRB varianta cerveno-cernych stromu prezentovana v kapitole 2.


# definice barev
RED = True
BLACK = False


class LLRBNode:
    # Trida reprezentujici uzel v cerveno-cernem strome.

    # Atributy:
    #   key   - hodnota klice uzlu
    #   color - barva uzlu, cervena nebo cerna
    #   left  - odkaz na leveho potomka (syna)
    #   right - odkaz na praveho potomka (syna)

    def __init__(self, key: int) -> None:
        self.key = key
        self.color = BLACK
        self.right: LLRBNode = self
        self.left: LLRBNode  = self


class LLRBTree:
    # Trida reprezentujici cerveno-cerny strom.

    # Atributy:
    #   NIL - cerny uzel s klicem None, reprezentujici vsechny listy stromu
    #   root - koren stromu

    def __init__(self) -> None:
        # NIL uzel nema zadnou hodnotu klice, z duvodu usnadneni typove kontroly 
        # pouzivame -1 misto None
        self.NIL = LLRBNode(-1) 
        self.root = self.NIL


def createNode(T: LLRBTree, key: int) -> LLRBNode:
    # Vytvori a vrati novy uzel, ktery se nasledne vlozi do stromu T
    new = LLRBNode(key)
    new.left = T.NIL
    new.right = T.NIL
    new.color = RED # narozdil od ostatnich variant se barva nastavuje zde
    return new


def searchNode(T: LLRBTree, key: int) -> LLRBNode:
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


def minimum(T, x) -> LLRBNode:
    # Najde minimalni uzel v podstrome s korenem x
    while x.left != T.NIL:
        x = x.left
    return x


def color_flip(T: LLRBTree, x: LLRBNode) -> None:
    # Prohodi barvy rodice s jeho potomky
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    x.color = not x.color
    x.left.color = not x.left.color
    x.right.color = not x.right.color


def llrb_left_rotate(T: LLRBTree, x: LLRBNode):
    # Provede levou rotaci kolem uzlu x
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    y = x.right
    x.right = y.left
    y.left = x
    y.color = x.color
    x.color = RED
    return y


def llrb_right_rotate(T: LLRBTree, x: LLRBNode):
    # Provede levou rotaci kolem uzlu x
    # Argument stromu neni potreba, pro jednotnost s pseudokodem je zde zahrnut
    y = x.left
    x.left = y.right
    y.right = x
    y.color = x.color
    x.color = RED
    return y


def llrb_insert(T: LLRBTree, key: int) -> None:
    # Vlozi do stromu T uzel s klicem key
    x = createNode(T, key)
    T.root = llrb_insert_rec(T, T.root, x)
    T.root.color = BLACK


def llrb_insert_rec(T: LLRBTree, h: LLRBNode, x: LLRBNode) -> LLRBNode:
    # Rekurzivni cast operace insert
    if h == T.NIL:
        return x
    if x.key < h.key:
        h.left = llrb_insert_rec(T, h.left, x)
    else:
        h.right = llrb_insert_rec(T, h.right, x)
    if h.left.color != RED and h.right.color == RED:
        h = llrb_left_rotate(T, h)
    if h.left.color == RED and h.left.left.color == RED:
        h = llrb_right_rotate(T, h)
    if h.left.color == RED and h.right.color == RED:
        color_flip(T, h)
    return h


def move_red_left(T: LLRBTree, h: LLRBNode) -> LLRBNode:
    # Zaridi, aby v levem podstrome existoval cerveny uzel
    color_flip(T, h)
    if h.right.left.color == RED:
        h.right = llrb_right_rotate(T, h.right)
        h = llrb_left_rotate(T, h)
        color_flip(T, h)
    return h


def move_red_right(T: LLRBTree, h: LLRBNode) -> LLRBNode:
    # Zaridi, aby v pravem podstrome existoval cerveny uzel
    color_flip(T, h)
    if h.left.left.color == RED:
        h = llrb_right_rotate(T, h)
        color_flip(T, h)
    return h


def llrb_delete_fixup(T: LLRBTree, h: LLRBNode) -> LLRBNode:
    # Provadi korekci po smazani uzlu, jedna se o stejne 3 podminky
    # jako na konci funkce llrb_insert_rec
    if h.left.color != RED and h.right.color == RED:
        h = llrb_left_rotate(T, h)
    if h.left.color == RED and h.left.left.color == RED:
        h = llrb_right_rotate(T, h)
    if h.left.color == RED and h.right.color == RED:
        color_flip(T, h)
    return h


def llrb_delete_min(T: LLRBTree, h: LLRBNode) -> LLRBNode:
    # Smaze minimalni uzel v podstrome s korenem x
    if h.left == T.NIL:
        return T.NIL
    if h.left.color != RED and h.left.left.color != RED:
        h = move_red_left(T, h)
    h.left = llrb_delete_min(T, h.left)
    return llrb_delete_fixup(T, h)


def llrb_delete(T: LLRBTree, key: int) -> None:
    # Smaze uzel s klicem key, predpokladame ze existuje
    T.root = llrb_delete_rec(T, T.root, key)
    T.root.color = BLACK


def llrb_delete_rec(T: LLRBTree, h: LLRBNode, key: int) -> LLRBNode:
    # Rekurzivni cast operace delete 
    if key < h.key:
        if h.left.color != RED and h.left.left.color != RED:
            h = move_red_left(T, h)
        h.left = llrb_delete_rec(T, h.left, key)
    else:
        if h.left.color == RED:
            h = llrb_right_rotate(T, h)
        if key == h.key and h.right == T.NIL:
            return T.NIL
        if h.right.color != RED and h.right.left.color != RED:
            h = move_red_right(T, h)
        if key == h.key:
            h.key = minimum(T, h.right).key
            h.right = llrb_delete_min(T, h.right)
        else:
            h.right = llrb_delete_rec(T, h.right, key)
    return llrb_delete_fixup(T, h)




