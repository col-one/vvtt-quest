from pathlib import Path

import pyxel

from pyxelutils.pyxelutils import core, color, collider
from pyxelutils.pyxelutils.examples import dog_actor

import inventory, props


class DogPropsCollider(collider.Collider):
    def logic(self, obj):
        print(f"Walk on Props : {obj.name}")
        core.BaseGame.destroy(obj.parent)


def Dog():
    dog = dog_actor.Dog()
    dog.x = 100
    dog.y = 100
    dog_props_collider = DogPropsCollider(8, 5, 50, 24, debug=True)
    dog_props_collider.subtype = props.Props
    dog_props_collider.parent_to(dog)

    return dog


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        swt = inventory.SwitchInventoryPushBtn(self)

        with self.level_manager.new_level('rt1'):
            self.level_manager.add_instance_object(swt)
            dog = Dog()

            for i in range(0, 4):
                props.Rect()
                props.Circle()

        with self.level_manager.new_level('inventory'):
            self.level_manager.add_instance_object(swt)
            inv = inventory.Inventory()

        self.level_manager.active_level = self.level_manager.levels['rt1']
        self.run_game()


if __name__ == '__main__':
    Game()
