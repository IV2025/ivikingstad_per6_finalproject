import pygame as pg
from pygame.sprite import Sprite
from settingsfinal import *
from random import randint
import os
from os import path

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")


vec = pg.math.Vector2

# player class

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties
        self.game = game
        self.image_orig = pg.transform.scale(game.player_img, (200, 30))
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.pos = vec(405, 600)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.rot = 0
        self.rot_speed = 0
        self.last_update = pg.time.get_ticks()
        self.left_key = pg.K_a
        #Sprite.__init__(self)
        # these are the properties
        #self.game = game
        # sprite_image = pg.image.load("blob.gif").convert_alpha()       attempting to integrate blob.gif instead of the main sprite
        #self.image = pg.Surface((50,50))
        #self.image.fill(AQUAMARINE)
        #self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH/2, HEIGHT/2)
        #self.pos = vec(WIDTH/2, HEIGHT/2)
        #self.vel = vec(0,0)
        #self.acc = vec(0,0)
        #self.cofric = 0.1
        #self.canjump = False
    def input(self):
        keystate = pg.key.get_pressed()
        # if keystate[pg.K_w]:
        #     self.acc.y = -PLAYER_ACC
        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        # if keystate[pg.K_s]:
        #     self.acc.y = PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
        # if keystate[pg.K_p]:
        #     if PAUSED == False:
        #         PAUSED = True
        #         print(PAUSED)
        #     else:
        #         PAUSED = False
        #         print(PAUSED)
    # ...
    # def jump(self):
    #     print("jump")
    #     self.rect.x += 1
    #     hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    #     self.rect.x -= 1
    #     # if hits:
    #     self.vel.y = -PLAYER_JUMP
    
    def inbounds(self):
        print("inbounds")
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("i am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("i am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            print("i am off the bottom of the screen")
        if self.rect.y < 0:
            print("i am off the top of the screen...")
    def mob_collide(self):
            hits = pg.sprite.spritecollide(self, self.game.enemies, True)
            if hits:
                print("you collided with an enemy...")
                self.game.score += 1
                print(SCORE)
    def update(self):
        #self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Mob(Sprite):
    def __init__(self,width,height, color):
        Sprite.__init__(self)
        self.width = width
        self.height = height

        self.mob_img = pg.image.load(path.join(img_folder, "beachball.png")).convert()
        self.mob_img.set_alpha(128)
        # add these lines for using an image with the player...
        # if not rotating, change image_orig to just image...
        self.image_orig = pg.transform.scale(self.mob_img, (32, 32))
        colorkey = self.image_orig.get_at((0, 0))
        self.image_orig.set_colorkey(colorkey)
        # ignore these lines - just for rotating...
        self.image = self.image_orig.copy()
        # self.image = pg.Surface((self.width,self.height))
        # self.color = RED
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(150,400)
        self.vel = vec(5,5)
        self.acc = vec(1,1)
        self.cofric = 0.01
    
    # ...
    # ball bounces off the boundaries of the game
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
            print("off right")
            # self.acc = self.vel * -self.cofric
        if self.rect.x < 0:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y < 0:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
    def update(self):
        self.inbounds()
        # self.pos.x += self.vel.x
        # self.pos.y += self.vel.y
        self.pos += self.vel
        self.rect.center = self.pos

# create a new platform class...

class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.brick_img = pg.image.load(path.join(img_folder, "brick.png")).convert()
        self.image_orig = pg.transform.scale(self.brick_img, (80, 60))
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        #self.image.fill(self.color)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant