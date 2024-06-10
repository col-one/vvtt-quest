from pathlib import Path

import pyxel

import inventory
import props
import dog
import dialog
from pyxelutils.pyxelutils import core, color


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        # init global game var
        core.BaseGame.instance.dialog = None
        core.BaseGame.instance.controllers = core.OrderedSet()

        swt = inventory.SwitchInventoryPushBtn(self)
        core.BaseGame.instance.controllers.add(swt)
        dialog_obj = dialog.DialogBox(10, core.BaseGame.instance.h - 50, core.BaseGame.instance.w - 20, 40)
        core.BaseGame.instance.dialog = dialog_obj

        with self.level_manager.new_level('rt1'):
            self.level_manager.add_instance_object(swt)
            self.level_manager.add_instance_object(dialog_obj)
            dog.Dog()

            for i in range(0, 8):
                a = props.Rect()
                a.name = f'rec-{i}'

        with self.level_manager.new_level('inventory'):
            self.level_manager.add_instance_object(swt)
            inv = inventory.Inventory(swt)

        self.level_manager.active_level = self.level_manager.levels['rt1']

        self.instance.run_at_end_with_delay((print, "CCACACACA DELAYED"), delay=10)

        self.run_game()

    @staticmethod
    def pause():
        for k in core.BaseGame.instance.controllers:
            print(f"Ctrl : {not k.active}")
            k.active = not k.active


if __name__ == '__main__':
    Game()
