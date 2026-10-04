""" 
main.py
-------
This module initializes and runs the main game loop for the platform game.
It includes the Game class and handles game states, events, and rendering.
Dependencies: pygame, random, myGameLib, settings, sprites, os

author: ami 
version: 3.2
last updated: 12.10.24

bg music from: 
    https://opengameart.org/content/space-music-2
pixel art from: 
    https://opengameart.org/content/space-shooter-redux

to get started run
    pip install pygame

"""

import pygame as pg
import random
from settings import *
import os
from os import path
from myGameLib import *
from settings import *
from sprites import *

# Initialize Pygame
pg.init()
pg.font.init()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "../img")
scores = insertion_sort(load("highscore.txt"))  # load high sccores and sort them

class Game:
    # initialize game window and it's attributes
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.score = 0

    # load high score data
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, "highscore.txt"), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load sounds
        self.dir = path.join(self.dir, 'music')
        self.jump_sound = pg.mixer.Sound(path.join(self.dir, 'jump.wav'))

    #  initialize a new game.
    def new(self):

        # reset game state variables
        self.score = 0
        self.distance_traveled = 0
        self.level = 1
        self.next_level = 100

        # initialize sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        # create the player object and add it to the sprite groups
        self.player = Player(self)
        player = self.player
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.mobs)

        # initialize power-ups group
        self.pows = pg.sprite.Group()

        # create and add platforms to the platforms group
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
 
        # initialize the mob timer
        self.mob_timer = 0
        # load background music
        pg.mixer.music.load(path.join(self.dir, 'Space_Music.ogg'))
        # start the game loop
        self.run()

    # game Loop
    def run(self):
        pg.mixer.music.play(loops=-1) # loop infintely when -1
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500) #fadeout instead of stop, 500mm

    # update all game objects and check for events.
    # this method is called every frame to update the game state.
    def update(self):
        self.all_sprites.update() # update all sprites

        # spawn new mobs periodically
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
           self.mob_timer = now
           Mob(self)

        # check for collisions between the player and mobs
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask) ## pg.sprite.collide_mask = better acuracy of collisions
        if mob_hits:
            self.playing = False

        # check if player hits a platform - only if falling
        # when self.playing = False, game ends as player is touching plat illegally
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen, scroll the screen 
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
                    self.distance_traveled += 10

        # check for collisions between the player and power-ups
        # increase score based on power-up value
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
                self.draw_text("Power up", 100, WHITE, 20,15)
            elif pow.type == 'gold':
                self.score += 50
                self.draw_text("Level up",100,RED,HEIGHT,WIDTH/2)

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= int(max(self.player.vel.y, 10))
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)

         # check if the player has reached the next level
        if self.distance_traveled == self.next_level:
            self.level += 1
            print(self.next_level)
            self.next_level *= 2 # increase the threshold for the next level

    # Game Loop - events
    def events(self):
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    # game loop - draw the current game state
    def draw(self):

        # Clear the screen with black
        self.screen.fill(BLACK) 
        # Draw your background image (if applicable)
        self.screen.blit(image, (0, 0))
        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # prints score to page
        self.draw_text(str("Score: "), 22, WHITE, 500 / 2, 15)
        self.draw_text(str(self.score), 22, WHITE, 600 / 2, 15)
        
        # print height to page
        self.draw_text(str(" Height:"), 22, WHITE, 50, 15)
        self.draw_text(str(self.distance_traveled), 22, WHITE, 120, 15)
        
        # prints level to page
        self.draw_text(str(" Level:"), 22, WHITE, 450 , 15)
        self.draw_text(str(self.level), 22, WHITE, 520, 15)

        # *after* drawing everything, flip the display
        pg.display.flip()

    # game splash/start screen
    def show_start_screen(self):
        self.pname = show_name_screen("Enter a name", 20, 100, RED, HEIGHT, WIDTH, image, background_rect)
        show_start_screen(TITLE, 10, 70, RED, HEIGHT, WIDTH, image, background_rect, self.score, scores)

    # game over/continue
    def show_go_screen(self):
        if not self.running:
            return

        show_game_over_screen(TITLE, 20, 90, RED, HEIGHT, WIDTH, image, background_rect, self.score, scores,
                              self.pname, "highscore.txt") 
        self.screen.fill(BGCOLOR)

    # handle Pygame events such as quitting and key releases
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    # draw text on the screen
    def draw_text(self, text, size, color, x, y):
        # Initialize Pygame font
        pg.font.init()
        
        font_name = pygame.font.match_font('arial', 1, 0)
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


#loads game graphics
image_path = os.path.join('img', 'starfield600-800.png')
image = pg.image.load(image_path)  # may need to move as already in game loop
background_rect = image.get_rect() # get rectangle of background

# Initialize and run the game
g = Game()
g.show_start_screen()
g.running = True
while g.running == True:
    g.new()
    g.show_go_screen()
pg.quit()