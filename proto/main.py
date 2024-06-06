from pathlib import Path

import pyxel

import inventory
import props
import dog
from pyxelutils.pyxelutils import core, color


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        core.BaseGame.instance.controllers = core.OrderedSet()

        swt = inventory.SwitchInventoryPushBtn(self)
        core.BaseGame.instance.controllers.add(swt)

        with self.level_manager.new_level('rt1'):
            self.level_manager.add_instance_object(swt)
            dog.Dog()

            for i in range(0, 8):
                a = props.Rect()
                a.name = f'rec-{i}'

        with self.level_manager.new_level('inventory'):
            self.level_manager.add_instance_object(swt)
            inv = inventory.Inventory(swt)

        self.level_manager.active_level = self.level_manager.levels['rt1']
        self.run_game()


if __name__ == '__main__':
    Game()
