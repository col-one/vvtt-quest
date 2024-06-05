import pyxel
import copy

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


class ObjectBrowserPushBtn(core.BaseGameObject):
    direction = 0
    def update(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.direction = -1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.direction = 1
        else:
            self.direction = 0

    def draw(self):
        pass


class ObjectBrowser(core.BaseGameObject):
    marge = 10
    display_max_objects = 5

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.active_id = 0
        self.last_active_id = -1
        self.cursor_x = 0
        self.cursor_y = 0

        self.cursor_h = 34
        self.cursor_w = 34

        self.browser_ctrl = ObjectBrowserPushBtn()

        self.objects = core.BaseGame.heroes[0].inventory_objects
        self.active_objects = core.OrderedSet()
        self.ready_to_display_copy = False
        self.active_object_for_view = None

    def reload(self):
        i = 0
        for o in self.objects:
            if o not in core.BaseGame.level_manager.levels['inventory'].register.all:
                core.BaseGame.level_manager.add_instance_object(o)
                self.ctrl.previous_lvl.register.remove(o)
            o.active = True
            o.size = 'middle'
            o.y = self.y
            o.x = self.x + i * (o.middle_w + self.marge)
            self.active_objects.add(o)
            # destroy collider
            core.BaseGame.destroy(o.children[0])
            i += 1
            if i == self.display_max_objects:
                break

    def prepare_view(self):
        print("prepare_view")
        obj = self.active_objects[self.active_id]
        core.BaseGame.copy(obj)
        self.ready_to_display_copy = True

    def active_view(self):
        obj2 = core.BaseGame.instance.get_last_copy()
        if obj2 is not None:
            self.active_object_for_view = obj2

    def update(self):
        if self.active_objects:
            self.active_id = (self.active_id + self.browser_ctrl.direction) % len(self.active_objects)
            self.cursor_x = self.active_objects[self.active_id].x - 1
            self.cursor_y = self.active_objects[self.active_id].y - 1
            if self.active_id != self.last_active_id:
                self.prepare_view()
            if self.ready_to_display_copy:
                self.active_view()
            self.last_active_id = self.active_id

    def draw(self):
        if self.active_objects:
            pyxel.rectb(self.cursor_x, self.cursor_y, self.cursor_w, self.cursor_h, col=1)


class Inventory(core.BaseGameObject):
    ui_marge = 10
    ui_font_h = 7
    ui_font_w = 3

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.desc_txt = text.Simple(core.BaseGame.instance.w / 2,
                               core.BaseGame.instance.h / 2 * 1.2,
                               "Ton sac est vide", col=1)
        self.desc_txt.active = False
        self.desc_txt.center = True
        self.desc_txt.parent_to(self)
        self.ui_frame_w = core.BaseGame.instance.w - self.ui_marge * 2
        self.ui_frame_h = core.BaseGame.instance.h - self.ui_marge * 2

        self.last_object_count = 0

        self.object_browser = ObjectBrowser(self.ctrl)
        self.object_browser.x = self.ui_marge * 2.6
        self.object_browser.y = core.BaseGame.instance.h * 0.72

    def update(self):
        if len(core.BaseGame.heroes[0].inventory_objects) == 0:
            self.desc_txt.active = True
        else:
            if len(core.BaseGame.heroes[0].inventory_objects) != self.last_object_count:
                print("update inventory")
                self.object_browser.reload()
                self.last_object_count = len(core.BaseGame.heroes[0].inventory_objects)
        if self.object_browser.active_object_for_view:
            obj = self.object_browser.active_object_for_view
            obj.x = (core.BaseGame.instance.w / 2) - (obj.big_w / 2)
            obj.y = (core.BaseGame.instance.h / 2) - obj.big_h * 1.1
            obj.size = 'big'
            self.desc_txt.txt = obj.desc_txt
            self.desc_txt.active = True

    def draw(self):
        pyxel.rect(self.x, self.y, core.BaseGame.instance.w, core.BaseGame.instance.h, col=0)
        pyxel.rectb(self.ui_marge, self.ui_marge, self.ui_frame_w, self.ui_frame_h, col=1)
        pyxel.rect(self.ui_marge + 6, self.ui_marge - 2, len('Sac a dos') * 5, 6, col=0)
        pyxel.text(self.ui_marge + 10, self.ui_marge - 2, 'Sac a dos ', col=1)
