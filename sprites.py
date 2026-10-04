"""
sprites.py
-----------
This module contains the sprite classes for the platform game.
It includes the Player class and a utility class for handling spritesheets.
Additionally contains the Platform, Mob, Powerup(Pow) classes.
Dependencies: pygame, settings, random, os.path
"""

import pygame as pg
from settings import *
import random
from random import choice, randrange
from os import path

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):

        # Set the layer for the sprite
        self._layer = PLAYER_LAYER
    
        # Initialize the sprite groups
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
    
        # Initialize movement flags and frame counters
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
    
        # Load and transform the player image
        player_img = pygame.image.load(os.path.join('img', 'player.png'))
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (90, 110))
    
        # Create a surface for the player image and blit the scaled image onto it
        player_img = pg.Surface((140, 200))
        player_img.blit(self.image, (0, 0), (584, 0, 121, 201))
        self.rect = self.image.get_rect()
    
        # Set the initial position, velocity, and acceleration of the player
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)


    class Spritesheet:

        # utility class for loading and parsing spreadsheets
        def __init__(self, filename):
            self.spritesheet = pg.image.load(filename).convert()

        def get_image(self, x, y, width, height):
            # grab an image out of a larger spritesheet
            image = pg.Surface((width, height))
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            image = pg.transform.scale(image, (width // 2, height // 2))
            return image

    # jumps only if standing on a platform
    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    # checks for player and mob collsions
    def collide(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
        colli = pg.sprite.spritecollide(self, self.game.Mob, False)
        if colli:
            pg.quit()

    def update(self):

        # Initialize acceleration with gravity
        self.acc = vec(0, PLAYER_GRAV)
        
        # Get the current state of the keyboard
        keys = pg.key.get_pressed()
        
        # Adjust acceleration based on key presses
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Apply friction to the acceleration
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Update velocity and position using equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # Wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # Update the rectangle's position
        self.rect.midbottom = self.pos

    # implements frames for sprite!
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):

        # Set the layer for the sprite
        self._layer = PLATFORM_LAYER

        # Initialize all the sprite groups
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Store the game instance
        self.game = game
 
        # Load the platform image 
        platform_img = pygame.image.load(os.path.join('img', 'ground_wood.png'))

        # Create a surface for the platform
        self.image = pg.Surface((w,h))
        self.image = platform_img
        platform_img = pg.Surface((14, 2))
        platform_img.blit(self.image, (0, 0), (5, 0, 1, 2))
        platform_img = pg.transform.scale(platform_img, (6, 2))

        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Randomly spawn a power-up on the platform
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)


class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):

        # Set the layer for the sprite
        self._layer = POW_LAYER

        # Initialize the all the sprite groups
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self,self.groups)

        # Store the game instance and platform reference
        self.game = game
        self.plat = plat

        # Randomly choose the type of power-up
        self.type = random.choice(['boost','gold'])

        # Load the appropriate image based on the type
        if self.type == 'boost':
            self.image = pygame.image.load(os.path.join('img', 'star_gold.png'))
        elif self.type == 'gold':
            self.image = pygame.image.load(os.path.join('img', 'gold.png'))

        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    # Update the position of the power-up
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
         # Remove the power-up if the platform is no longer in the game
        if not self.game.platforms.has(self.plat):
            self.kill()


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        
        # Set the layer for the sprite
        self._layer = MOB_LAYER

        # Initialize all the sprite groups
        self.groups = game.all_sprites, game.mobs
        self.current_frame = 0  
        self.last_update = 0    
        pg.sprite.Sprite.__init__(self, self.groups)

        # Store the game instance
        self.game = game

        # Load the mob image
        mob_img = pygame.image.load(os.path.join('img', 'zzmonster.png'))
        self.image = mob_img
        self.image.set_colorkey(BLACK)

        # Get the rectangle for positioning
        self.rect = self.image.get_rect()

        # Randomly place the mob off-screen to the left or right
        self.rect.centerx = choice([-100, WIDTH + 100])

        # Set horizontal velocity
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1

        # Randomly place the mob vertically within the top half of the screen
        self.rect.y = randrange(0, int(HEIGHT / 2))
        self.vy = 0    # y velocity to 0
        self.dy = 0.5  # direction y

    def update(self):

        # Update horizontal position
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1

        # Preserve the center position while updating the rectangle
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy

         # Remove the mob if it moves off-screen
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()