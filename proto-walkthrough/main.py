
from pathlib import Path
import pyxel

from pyxelutils.pyxelutils import core, color
from pyxelutils.pyxelutils.examples import dog_actor


class Background(core.BaseGameObject):
    def update(self):
        pass

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 464, 256, 0)


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()
        pyxel.images[0] = pyxel.Image.from_image(f'{Path(__file__).parent}/resources/urban_rpg.png', incl_colors=True)
        pyxel.tilemaps[0] = pyxel.Tilemap.from_tmx(f'{Path(__file__).parent}/resources/urban_rpg.tmx', 0)

        color.add_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[1].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        Background()
        dog_actor.Dog(img_bank=1)


        self.run_game()

#
# class Game:
#     def __init__(self):
#         pyxel.init(256, 224, title="Tiled Map File")
#         pyxel.images[0] = pyxel.Image.from_image(
#             "/Users/colin/Downloads/urban_rpg.png", incl_colors=True
#         )
#         pyxel.tilemaps[0] = pyxel.Tilemap.from_tmx("/Users/colin/Downloads/urban_rpg.tmx", 0)
#         self.x = 0
#         pyxel.run(self.update, self.draw)
#
#     def update(self):
#         pass
#
#     def draw(self):
#         pyxel.cls(1)
#         pyxel.bltm(0, 0, 0, 0, 0, 464, 256, 0)
#         # pyxel.bltm(0, 0, 1, 0, 0, pyxel.width, pyxel.height, 0)
#         self.x += 1
#         pyxel.camera(self.x, 0)


if __name__ == '__main__':
    Game()

