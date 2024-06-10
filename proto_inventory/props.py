import random

import pyxel

from pyxelutils.pyxelutils import core, collider, text


class PropsCollider(collider.Collider):
    def logic(self, obj):
        pass


class Props(core.BaseGameObject):
    def update(self):
        pass

    def draw(self):
        pass

    @staticmethod
    def text(txt):
        text.InRect(10, core.BaseGame.instance.h - 50, core.BaseGame.instance.w - 20, 40, txt, col=0)

    def launch_dialog(self):
        core.BaseGame.instance.run_at_end.add((self.text, self.pickup_txt))


class Rect(Props):
    def __init__(self):
        self.x = random.randint(10, core.BaseGame.instance.w - 10)
        self.y = random.randint(10, core.BaseGame.instance.h - 50)
        self.col = PropsCollider(0, 0, 7, 7, debug=False)
        self.col.parent_to(self)
        self.small_w = 5
        self.small_h = 5
        self.middle_w = 32
        self.middle_h = 32
        self.big_w = 64
        self.big_h = 64
        self.color = random.randint(2, 9)

        self.size = 'small'
        self.w = self.small_w
        self.h = self.small_h

        self.desc_txt = f'Un carre {self.color} qui servira surement a caller une table'
        self.pickup_txt = f'Hum... on dirait un simple carre {self.color}'

    def draw(self):
            pyxel.rect(self.x, self.y, self.w, self.h, col=self.color)

    def update(self):
        if self.size == 'small':
            self.w = self.small_w
            self.h = self.small_h
        elif self.size == 'middle':
            self.w = self.middle_w
            self.h = self.middle_h
        elif self.size == 'big':
            self.w = self.big_w
            self.h = self.big_h

class Circle(Props):
    def __init__(self):
        self.x = random.randint(10, core.BaseGame.instance.w - 10)
        self.y = random.randint(10, core.BaseGame.instance.h - 10)
        self.col = PropsCollider(-5, -5, 11, 11, debug=True)
        self.col.parent_to(self)

        self.small_r = 5
        self.middle_r = 16
        self.big_r = 32

        self.size = 'small'

        self.desc_txt = 'Un simple cercle qui trainait par terre'

    def draw(self):
        if self.size == 'small':
            pyxel.circ(self.x, self.y, self.small_r, col=5)
        elif self.size == 'middle':
            pyxel.circ(self.x, self.y, self.middle_r, col=5)
        elif self.size == 'big':
            pyxel.circ(self.x, self.y, self.big_r, col=5)

    def update(self):
        pass
