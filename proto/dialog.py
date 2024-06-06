import random

import pyxel

from pyxelutils.pyxelutils import core, collider, text


class DialogBox(core.BaseGameObject):
    def __init__(self, x=0, y=0, w=230, h=50):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dialog = None
        self.ask_dialog = DialogYesNo(0, 0, 50, 30, yes='Oui', no='Non')
        self.ask_dialog.parent_to(self)
        self.ask_dialog.active = False
        self.waiting_for_ask = False

    def pop(self, txt):
        print("Pop dialog")
        if self.dialog:
            core.BaseGame.destroy(self.dialog)
            self.dialog = None
        self.dialog = text.InRect(self.x, self.y, self.w, self.h, txt, col=0)

    def ask(self, question):
        print("Pop Ask dialog ?")
        self.ask_dialog.txt = question
        if self.dialog and not self.dialog.finished:
            self.waiting_for_ask = True
            print("Waiting finishing dialog box")
            self.ask_dialog.active = False
        else:
            self.ask_dialog.active = True

    def update(self):
        if self.dialog and self.dialog.finished and self.waiting_for_ask:
            print("active ask")
            self.ask_dialog.active = True
            g = core.BaseGame.level_manager
            self.waiting_for_ask = False

    def draw(self):
        pass


class DialogYesNo(core.BaseGameObject):
    def __init__(self, x=0, y=0, w=230, h=50, question_txt='Answer :', yes='Yes', no='No'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.yes_txt = yes
        self.no_txt = no
        self.txt = question_txt

    def update(self):
        pass

    def draw(self):
        pyxel.rectb(self.x + self.parent.w - self.w, self.y - self.h, self.w, self.h, col=0)
        pyxel.text(self.x + self.parent.w - self.w + 5, self.y - self.h + 5, self.txt, col=0)
        pyxel.text(self.x + self.parent.w - self.w + 7, self.y - self.h + 17, self.yes_txt, col=0)
        pyxel.text(self.x + self.parent.w - self.w + 30, self.y - self.h + 17, self.no_txt, col=0)

