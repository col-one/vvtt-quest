import pyxel

from pyxelutils.pyxelutils import core, text


class SwitchInventoryPushBtn(core.BaseGameObject):
    previous_lvl = None

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if core.BaseGame.level_manager.active_level.name != 'inventory':
                self.previous_lvl = core.BaseGame.level_manager.active_level
                core.BaseGame.level_manager.active_level = core.BaseGame.level_manager.levels['inventory']
                print("Show inventory")
            else:
                core.BaseGame.level_manager.active_level = self.previous_lvl
                self.previous_lvl = None
                print("Hide inventory")

    def draw(self):
        pass


class Inventory(core.BaseGameObject):
    objects = core.OrderedSet()
    ui_marge = 10
    ui_font_h = 7
    ui_font_w = 3

    def __init__(self):
        self.empty_txt = text.Simple(core.BaseGame.instance.w / 2,
                               core.BaseGame.instance.h / 2,
                               "Ton sac est vide", col=1)
        self.empty_txt.active = False
        self.empty_txt.center = True
        self.empty_txt.parent_to(self)
        # core.BaseGame.level_manager.active_level.register.change_layer(self, core.Layer.FOREGROUND)

    def update(self):
        if len(self.objects) == 0:
            self.empty_txt.active = True

    def draw(self):
        pyxel.rect(self.x, self.y, core.BaseGame.instance.w, core.BaseGame.instance.h, col=0)
        pyxel.rectb(self.ui_marge, self.ui_marge,
                    core.BaseGame.instance.w - self.ui_marge * 2,
                    core.BaseGame.instance.h - self.ui_marge * 2, col=1)



