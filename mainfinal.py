# File created by: Ivan Vikingstad
# Agenda:
# Creat github 
# Create platforms and images
# Create libraries
#
# Source: https://www.geeksforgeeks.org/getting-started-with-pygame/#
# Source: https://www.geeksforgeeks.org/how-to-add-moving-platforms-in-pygame/
# Source: https://opensource.com/article/18/7/put-platforms-python-game
# Source: https://creazilla.com/nodes/1555445-brick-wall-clipart
# Source: http://clipart-library.com/clipart/fireball-clipart_8.htm
# Source: https://www.pinterest.com/pin/platform-clipart-hd-png-podium-stone-and-grass-platform-podium-platform-stone-png-image-for-free-download--13018286414851365/
# Source: Dad helped with some bugs and things I was stumped on
# Source: Idea came from the original Atari Breakout


# Goals:
# 1. Make a game similar to Atari Breakout
# 2. Integrate pygame efficiently
# 3. Make images and duplicate (DONE)
# 4. Calculate where the images would have to be positioned
# 5. Make a Player sprite (another platform)
# 6. Make a ball 
# 7. Make it so that once the ball collides with the platform it bounces off in a certain direction based on where it hit the platform
# 8. Make it so that once the ball collides with the images the images dissapear
# 9. Make a score 
# 10. Make the score change +1 once one image dissapears
# 11. Make lives for the player so that if the ball goes below the platform you get -1 life
# 12. Make some space above and below the image pile for the ball to go to

# import libs
import pygame as pg
import os
# import settings 
from settingsfinal import *
from platformsimages import *
from os import path
# from pg.sprite import Sprite

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")

# create game class in order to pass properties to the sprites file
class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
        print(self.screen)

        self.font=pg.freetype.SysFont(None, 34)
        self.font.origin=True

        self.clock_running = True
        self.won = False
        self.lost = False

        # to add images sounds etc copy below...
        # still working on how to get an image to replace the normal controlled square sprite
    def load_data(self):
        self.player_img = pg.image.load(path.join(img_folder, "platform.png")).convert()

    # this is where the game gets created and loads all the bricks, the player, and ball        
    def new(self):
        # starts a new game
        self.score = 0
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        #self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        # self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        #0o[ -7self.all_sprites.add(self.plat1)

        #self.platforms.add(self.plat1)
        
        self.all_sprites.add(self.player)
        #for plat in PLATFORM_LIST:
        self.brick_x = 0
        # Loaded 30 bricks into pygame
        for i in range(0,10):
            plat = (self.brick_x, 120, 80, 60, (PURPLE), "normal")
            self.brick_x = self.brick_x + 80

            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.brick_x = 0
        for i in range(0,10):
            plat = (self.brick_x, 180, 80, 60, (WHITE), "normal")
            self.brick_x = self.brick_x + 80

            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.brick_x = 0
        for i in range(0,10):
            plat = (self.brick_x, 240, 80, 60, (BLUE), "normal")
            self.brick_x = self.brick_x + 80

            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        
        m = Mob(20,20,(0,255,0))
        self.all_sprites.add(m)
        self.enemies.add(m)

        self.mob = m
        print(self.platforms)
        self.run()
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
           # if event.type == pg.KEYDOWN:
               # if event.key == pg.K_SPACE:
               #     self.player.jump()
    def update(self):
        self.all_sprites.update()

       # self.screen.fill(pg.Color('grey12'))

        # collision detection for collisions with the player
        hits_enemies = pg.sprite.spritecollide(self.player, self.enemies, False)
        if hits_enemies:
            print("hit paddle")
            self.mob.vel.y *= -1
            #self.clock_running = False

        # collision detecion for collisions with the bricks
        hits_platforms = pg.sprite.spritecollide(self.mob, self.platforms, False)
        if hits_platforms:
            print("hit platform")
            self.mob.vel.y *= -1
            self.platforms.remove(hits_platforms[0])
            self.all_sprites.remove(hits_platforms[0])
            print(self.platforms)
            if not self.platforms:
                self.won = True
            #self.clock_running = False

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #print("hit!!!!!")
                
                if hits[0].variant == "disappearing":
                    #print("disappearing")
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    #print("bouncey")
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    #print("else")
                    #print(hits)
                    self.player.pos.y = hits[0].rect.top
        if self.mob.rect.y > HEIGHT:
            self.clock_running = False
            self.lost = True

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # is this a method or a function?
        if self.clock_running == True:
            self.last_tick = pg.time.get_ticks()
            
        ticks=self.last_tick
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 24)
        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        self.font.render_to(self.screen, (50, 50), out, pg.Color(WHITE))

        # winning the game
        if self.won == True:
            print("won")
            self.font.render_to(self.screen, (340, 300), "YOU WIN!", pg.Color(BLUE))

        # losing the game
        if self.lost == True:
            self.font.render_to(self.screen, (320, 400), "YOU LOST!", pg.Color(RED))
            self.all_sprites.remove(self.mob)

        #pg.display.flip()
        # self.clock.tick(60)

        pg.display.flip()
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)

# instantiate the game class...
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()