import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *

from os import path

# vector for collisions
vec = pg.math.Vector2
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    # check for x collision
    if dir == "x":
        # checks to see if we've collided with hit_rects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # actually checks if we are to the left or right of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                # reposition player/sprite to left of the wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            elif hits[0].rect.centerx < sprite.hit_rect.centerx:
                # reposition to right of the wall
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    # check for y collision
    if dir == "y":
        # checks to see if we've collided with hit_rects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # actually checks if we are on top or bottom of the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                # reposition player/sprite to top of the wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            elif hits[0].rect.centery < sprite.hit_rect.centery:
                # reposition to bottom of the wall
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y):
        # properties of player
        # image, size, hitbox, position
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.last_update = 0
        self.current_frame = 0
        print("player initialized...")
    
    def get_keys(self):
        # reset velocity to zero
        # listen for events specific to keys
        # change velocity based on which key is pressed
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # check if player is diagonal
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def animate(self):
        now = pg.time.get_ticks()
        # waits 350 ms to show next frame/image
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        
    def load_images(self):
        # cycles through images in the spritesheet to animate
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE,TILESIZE)]

    def update(self):
        # updates everything, letting you move
        # as well as show animations
        self.get_keys()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center



class Wall(Sprite):
    def __init__(self, game, x, y):
        # properties of walls
        # size, position, color/image
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # print("wall initialized...")


class Mob(Sprite):
    def __init__(self, game, x, y):
        # properties of mobs
        # size, color/image, position
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.vel.x = MOB_SPEED
        self.last_update = 0
        self.current_frame = 0
        print("Mob initialized...")

    def animate(self):
        now = pg.time.get_ticks()
        # waits 350 ms to show next frame/image
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        
    def load_images(self):
        # cycles through images in the spritesheet to animate
        self.idle_frames = [self.spritesheet.get_image(0,TILESIZE,TILESIZE,TILESIZE),
                            self.spritesheet.get_image(TILESIZE,TILESIZE,TILESIZE,TILESIZE)]
    
    def update(self):
        # makes the mob move and animates it
        # if self.rect.y > HEIGHT - TILESIZE or self.rect.y < 0:
        #     print("mob hit the edge")
        #     self.speed *= -1
        #     self.x += TILESIZE
        self.animate()
        if self.pos.x > WIDTH - TILESIZE or self.pos.x < 0:
        # if collide_with_walls:
            # print("mob hit the edge")
            self.vel.x *= -1
            self.pos.y += TILESIZE
        # self.x += self.vx * self.game.dt * self.speed
        # self.rect.x = self.x
        # self.y += self.vy * self.game.dt * self.speed
        # self.rect.y = self.y

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        # collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        # collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center