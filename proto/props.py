import random

import pyxel

from pyxelutils.pyxelutils import core, collider


class PropsCollider(collider.Collider):
    def logic(self, obj):
        pass


class Props(core.BaseGameObject):
    def update(self):
        pass

    def draw(self):
        pass


class Rect(Props):
    def __init__(self):
        self.x = random.randint(10, core.BaseGame.instance.w - 10)
        self.y = random.randint(10, core.BaseGame.instance.h - 10)
        self.col = PropsCollider(0, 0, 7, 7, debug=True)
        self.col.parent_to(self)

    def draw(self):
        pyxel.rect(self.x, self.y, 5, 5, col=5)

    def update(self):
        pass


class Circle(Props):
    def __init__(self):
        self.x = random.randint(10, core.BaseGame.instance.w - 10)
        self.y = random.randint(10, core.BaseGame.instance.h - 10)
        self.col = PropsCollider(-5, -5, 11, 11, debug=True)
        self.col.parent_to(self)

    def draw(self):
        pyxel.circ(self.x, self.y, 4, col=7)

    def update(self):
        pass
