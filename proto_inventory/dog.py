import pyxel

from pyxelutils.pyxelutils import core, collider, text
from pyxelutils.pyxelutils.examples import dog_actor

import props, dialog


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

    def logic(self, prop_c):
        if pyxel.frame_count > 0:
            print(f"Walk on Props : {prop_c.parent.name} {prop_c.parent.x}")
            prop_c.active = False
            core.BaseGame.instance.dialog.post_function = self.post_function
            core.BaseGame.instance.run_at_end.add((core.BaseGame.instance.dialog.pop, prop_c.parent.pickup_txt))
            core.BaseGame.instance.run_at_end.add((core.BaseGame.instance.dialog.ask, "Prendre ?"))
            core.BaseGame.instance.dialog.post_args.add(prop_c)

            self.parent.action.ctrl.direction = [0, 0]
            core.BaseGame.instance.pause()

    @staticmethod
    def post_function(args):
        prop_c, answer = args
        print("Calling post function")
        core.BaseGame.instance.pause()
        if answer is True:
            core.BaseGame.heroes[0].inventory_objects.add(prop_c.parent)
            prop_c.parent.active = False
        else:
            core.BaseGame.run_at_end_with_delay((prop_c.activate, True), delay=10)
        core.BaseGame.instance.dialog.post_args.clear()


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
