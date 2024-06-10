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
        self.post_function = None
        self.post_args = core.OrderedSet(weak=False)

    def pop(self, txt):
        print("Pop dialog")
        self.active = True
        if self.dialog:
            self.dialog = None
        self.dialog = text.InRect(self.x, self.y, self.w, self.h, txt, col=0)

    def ask(self, question):
        print("Pop Ask dialog ?")
        self.ask_dialog.reset()
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
            self.waiting_for_ask = False
        if self.ask_dialog.answer is not None:
            print("Answer is ", self.ask_dialog.answer)
            self.dialog.active = False
            self.ask_dialog.active = False
            self.post_args.add(self.ask_dialog.answer)
            core.BaseGame.instance.run_at_end.add((self.post_function, self.post_args))
            self.active = False

    def draw(self):
        pass


class DialogYesNoCtrl(core.BaseGameObject):
    direction = 0
    validate = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.direction = 0
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.direction = 1
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.validate = True

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
        self.cursor_x = 0
        self.cursor_y = 0

        self.ctrl = DialogYesNoCtrl()
        self.ctrl.parent_to(self)

        self.answer = None

    def reset(self):
        self.answer = None
        self.ctrl.direction = 0
        self.ctrl.validate = None

    def update(self):
        self.cursor_x = self.x + self.parent.w - self.w + 4 + (self.ctrl.direction * 23)
        if self.ctrl.validate:
            if self.ctrl.direction == 0:
                self.answer = True
            else:
                self.answer = False

    def draw(self):
        pyxel.rectb(self.x + self.parent.w - self.w, self.y - self.h, self.w, self.h, col=0)
        pyxel.text(self.x + self.parent.w - self.w + 5, self.y - self.h + 5, self.txt, col=0)
        pyxel.text(self.x + self.parent.w - self.w + 7, self.y - self.h + 17, self.yes_txt, col=0)
        pyxel.text(self.x + self.parent.w - self.w + 30, self.y - self.h + 17, self.no_txt, col=0)
        pyxel.rectb(self.cursor_x, self.y - self.h + 16, 1, 8, col=0)

