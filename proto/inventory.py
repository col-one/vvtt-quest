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
        self.object_id = 0
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
        self.need_update = False

        self.clone_object = None
        self.active_range = [0, 5]

    def populate(self):
        self.active_objects = self.objects[self.active_range[0]: self.active_range[1]]
        i = 0
        for o in self.active_objects:
            if o not in core.BaseGame.level_manager.levels['inventory'].register.all:
                # destroy collider
                core.BaseGame.destroy(o.children[0])
                core.BaseGame.level_manager.add_instance_object(o)
                self.ctrl.previous_lvl.register.remove(o)

    def draw_active_object(self):
        i = 0
        for o in self.active_objects:
            o.active = True
            o.size = 'middle'
            o.y = self.y
            o.x = self.x + i * (o.middle_w + self.marge)
            i += 1

    def prepare_view(self):
        obj = self.active_objects[self.active_id]
        core.BaseGame.copy(obj)
        self.ready_to_display_copy = True

    def active_view(self):
        obj2 = core.BaseGame.instance.get_last_copy()
        if obj2 is not None:
            if self.clone_object:
                core.BaseGame.destroy(self.clone_object)
            self.active_object_for_view = obj2
            self.clone_object = obj2

    def manage_active_queue(self):
        new_id = self.active_id + self.browser_ctrl.direction
        if 0 <= new_id < len(self.active_objects):
            self.active_id = new_id
        if len(self.active_objects) <= new_id < len(self.objects):
            if self.active_range[1] + 1 > len(self.objects):
                return
            for o in self.active_objects:
                o.active = False
            self.active_range[0] += 1
            self.active_range[1] += 1
            self.active_id = len(self.active_objects) - 1
            self.populate()
            self.draw_active_object()
            self.need_update = True
        if new_id < 0:
            if self.active_range[0] - 1 < 0:
                return
            self.active_range[0] -= 1
            self.active_range[1] -= 1
            self.active_id = 0
            self.populate()
            self.draw_active_object()
            self.need_update = True

    def update(self):
        if self.active_objects:
            self.manage_active_queue()
            self.cursor_x = self.active_objects[self.active_id].x - 1
            self.cursor_y = self.active_objects[self.active_id].y - 1
            if self.active_id != self.last_active_id or self.need_update:
                self.prepare_view()
            if self.ready_to_display_copy:
                self.active_view()
            self.last_active_id = self.active_id
            self.need_update = False

    def draw(self):
        if self.active_objects:
            pyxel.rectb(self.cursor_x, self.cursor_y, self.cursor_w, self.cursor_h, col=1)
            if self.active_range[1] < len(self.objects):
                pyxel.rectb(self.active_objects[-1].x + 32 + 8, self.active_objects[-1].y + 13, 5, 5, col=1)
            if self.active_range[0] != 0:
                pyxel.rectb(self.active_objects[0].x - 12, self.active_objects[0].y + 13, 5, 5, col=1)


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
        self.object_browser.x = self.ui_marge * 2.8
        self.object_browser.y = core.BaseGame.instance.h * 0.72

    def update(self):
        if len(core.BaseGame.heroes[0].inventory_objects) == 0:
            self.desc_txt.active = True
        else:
            if len(core.BaseGame.heroes[0].inventory_objects) != self.last_object_count:
                print("update inventory")
                self.object_browser.populate()
                self.object_browser.draw_active_object()
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
