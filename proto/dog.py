import pyxel

from pyxelutils.pyxelutils import core, collider, text
from pyxelutils.pyxelutils.examples import dog_actor

import props


class DogPropsCollider(collider.Collider):

    def update(self):
        super().update()
        self.w = self.parent.action.current.w - 15
        self.h = self.parent.action.current.h
        if self.w <= 32:
            self._x = 16
            self._y = 0
            self.w = self.parent.action.current.w
        else:
            self._x = 7
            self._y = 4

    def logic(self, obj):
        if pyxel.frame_count > 0:
            print(f"Walk on Props : {obj.parent.name} {obj.parent.x}")
            obj.parent.launch_dialog()
            core.BaseGame.instance.run_at_end.add((self.overlap.remove, obj))
            # core.BaseGame.heroes[0].inventory_objects.add(obj.parent)
            # obj.parent.active = False
            obj.active = False

            self.parent.action.ctrl.direction = [0, 0]
            for k in core.BaseGame.instance.controllers:
                k.active = False


def Dog():
    dog = dog_actor.Dog()
    dog.x = 100
    dog.y = 100
    dog.inventory_objects = core.OrderedSet()
    dog_props_collider = DogPropsCollider(7, 4, 45, 24, debug=True)
    dog_props_collider.subtype = props.Props
    dog_props_collider.parent_to(dog)

    core.BaseGame.instance.controllers.add(dog.action.ctrl)

    return dog
