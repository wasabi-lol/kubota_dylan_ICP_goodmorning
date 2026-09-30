# this file was created by Dylan Kubota
# code inspired by game dev Chris Bradfield
# who was inspired by Notch

# import pygame and other files
import pygame as pg
from settings import *
from sprites import *
from utils import *

'''
Data types: boolean, string, int, etc.

Input/events: keyboard, mouse, voice, power button,
eye tracking, camera, gyroscoping, electrostatic,
location, volume, mic, etc.

Process: cursor position, player position, score,
enemy position, aim in FPS, etc.

Output: graphics - things are drawn, sound - , etc.
'''

# set properties, etc. for objects within Game
class Game:
    # initiate the game, characters, music, etc.
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("game initialized...")
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
    
    # load data from the level text files, images, files
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, "images")
        self.snd_dir = path.join(self.game_dir, "audio")
        self.map = Map(path.join(self.game_dir, map))

    # makes player
    def new(self):
        self.load_data("level1.txt")
        # print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # self.player = Player(self,0,0)
        # self.cactus = Wall(self,7,7)
        # self.enemy = Mob(self,5,5)

        # instantiates entities based on the level map
        # walls
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
        # mobs
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "M":
                    Mob(self, col, row)
        # player
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "P":
                    Player(self, col, row)


    # runs the game
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    # inputs
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    # animations
    def update(self):
        self.all_sprites.update()

    # puts stuff on the screen
    def draw(self):
        self.screen.fill(TAN)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


# makes it so that the game only runs in this file
if __name__ == "__main__":
    g = Game()

# keeps the game running instead of instantly crashing
while g.running:
    g.new()
    g.run()