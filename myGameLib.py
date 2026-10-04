"""
sprites.py
-----------
This module contains the sprite classes for the platform game.
It includes the Player class and a utility class for handling spritesheets.
Dependencies: pygame, random, csv, os.path
"""

import pygame
import random
import os.path
import csv

# Initialize the game clock
clock = pygame.time.Clock()

# Title of the game
TITLE = "Space Jump"

# set up game screen
WIDTH = 700
HEIGHT = 800
FPS = 60
FONT_NAME = 'ariel'
SPRITESHEET = "spritesheet_jumper.png"
CHARACTERS = "sprites_characters.png"

# player movement properties. change for speed height etc
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8      # bigger value is a faster fall rate
JUMP_HEIGHT = -15      # change for jump height
JUMP_CUT_HEIGHT = - 3  # change for short jump height

# game properties
BOOST_POWER = 60   # jump boost
POW_SPAWN_PCT = 7  # spawn chance percent
MOB_FREQ = 5000    # frequency of mob spawn 5000 = 5 seconds
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DRED = (128, 0, 0)
GREEN = (0, 255, 0)
DGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
DBLUE = (0, 0, 128)
YELLOW = (255, 255, 0)
DYELLOW = (128, 128, 0)
ORANGE = (255, 126, 0)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)
TEAL = (0, 128, 128)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)
SILVER = (192, 192, 192)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
LIGHTBLUE = (0, 155, 166)
BGCOLOR = LIGHTBLUE  # bg colour
HS_BG =  (4, 19, 21)
HS_TITLE = (0, 255, 255)
HS_TOP = (0, 128, 128)
HS_REST = (192, 192, 192)


# returns a random colour that fits within the width of the screen
def rand():
    return random.randint(10, WIDTH-100)

# returns a random colour
def random_colour():
    cols = [WHITE, CYAN, PURPLE, BLUE, YELLOW, ORANGE]
    x = (random.randint(0, len(cols)-1))
    return cols[x]

#  Save a list of records to a CSV file.
def save(filename, values, num_fields):
    file = open(filename, "w")
    for record in range(len(values)):
        for field in range(num_fields):
            file.write(values[record][field])
            if field != num_fields - 1:
                file.write(",")
            else:
                file.write('\n') # new line
    file.close()

# Load the highscores from a CSV file into a list
# returns the data as a 2d list
def load(filename):

    values = []
    file = open(filename, "r")
    data = csv.reader(file)

    for row in data:
        value = []
        for field in row:
            value.append(field)
        values.append(value)
    file.close()
    return values

# sort scores, starting from 1 since the first element is sorted
def insertion_sort(values):
    for i in range(1, len(values)):
        currValue = values[i][1]
        currPosition = i
        while currPosition > 0 and int(values[currPosition - 1][1]) < int(currValue):
            # swap scores
            temp = values[currPosition][1]
            values[currPosition][1] = values[currPosition - 1][1]
            values[currPosition - 1][1] = temp
            # swap names
            temp = values[currPosition][0]
            values[currPosition][0] = values[currPosition - 1][0]
            values[currPosition - 1][0] = temp
            currPosition = currPosition - 1
    return values

# adds a new high score to the table.
# uses an insertion sort function to sort the table.
# uses the save function to save the sorted table.
def new_high_score(name, table, new_score, saveFile):
    table[4][0] = name
    table[4][1] = str(new_score)
    table = insertion_sort(table)           # sort the table
    save(saveFile, table, len(table[0]))    # save the table
    for i in range(len(table)):
        if int(table[i][1]) == new_score:
            return i + 1                    # return the position in the table

#  draws text on a given surface.
def draw_text(surf, text, size, x, y, colour):
    font_name = pygame.font.match_font('arial', 1, 0)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#draws a rectangle on a given surface.
def draw_rect(surf, x, y, width, height, colour):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surf, colour, rect)

# draws the high score table on a given surface.
def draw_high_score_table(surf, font_size, pos, table_pos, width, values):

    # draw the background rectangle for the high score table
    draw_rect(surf, 0, pos + table_pos, WIDTH, font_size * 8, HS_BG)

    # draw the title of the high score table
    draw_text(surf, "High Score Table", font_size, width / 2, pos + table_pos, HS_TITLE)

    # draw the first high score entry with a larger font size
    text = values[0][0]
    text = text + "    " + values[0][1]
    draw_text(surf, text, font_size + 10, width / 2, pos + table_pos + font_size, HS_TOP)
    
    # iterate over the remaining high score entries and draw them
    for i in range(1, len(values)):  # print the high scores
        text = values[i][0]
        text = text + "    " + values[i][1]
        draw_text(surf, text, font_size, width / 2, pos + table_pos + font_size + i * 40, HS_REST)


######## start of functions for show_name_screen ########
# initialises window for the game start screen
def init_pygame(WIDTH, HEIGHT):
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))

# adds custom title to start screen
def draw_title(screen, WIDTH):
    draw_text(screen, TITLE, 48, WIDTH / 2, 10, RED)

# draws current username
def draw_current_name(screen, name, table_font_size, WIDTH, HEIGHT):
    draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, HEIGHT - 550, table_font_size * table_font_size / 2,
              table_font_size + 5, BLACK)
    draw_text(screen, name, table_font_size, WIDTH / 2, HEIGHT - 550, ORANGE)

# draws new username
def draw_new_name(screen, new_name, column, table_font_size, WIDTH, HEIGHT):
    draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, HEIGHT - 450, table_font_size * table_font_size / 2,
              table_font_size * 2 + 5, BLUE)
    draw_text(screen, new_name, table_font_size * 2, WIDTH / 2, HEIGHT - 450, ORANGE)
    draw_text(screen, chr(94), table_font_size * 2, WIDTH / 2 - table_font_size - 10 + (column * 35), HEIGHT - 400, RED)

# handle Pygame events such as changing a letter in a players username
def handle_key_presses(keystate, letter1, letter2, letter3, column):
    if keystate[pygame.K_DOWN]:
        if column == 0:
            letter1 = (letter1 + 1) % 26
        elif column == 1:
            letter2 = (letter2 + 1) % 26
        elif column == 2:
            letter3 = (letter3 + 1) % 26
        clock.tick(4)
    elif keystate[pygame.K_UP]:
        if column == 0:
            letter1 = (letter1 - 1) % 26
        elif column == 1:
            letter2 = (letter2 - 1) % 26
        elif column == 2:
            letter3 = (letter3 - 1) % 26
        clock.tick(4)
    elif keystate[pygame.K_RIGHT]:
        column = (column + 1) % 3
        clock.tick(4)
    elif keystate[pygame.K_LEFT]:
        column = (column - 1) % 3
        clock.tick(4)
    return letter1, letter2, letter3, column

# handle Pygame events such as quitting and key releases.
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
######## end of functions for show_name_screen ########


# method to set up start screen
def show_name_screen(name, min_size, max_size, colour, HEIGHT, WIDTH, background, background_rect):
    
    # Initialize Pygame
    screen = init_pygame(WIDTH, HEIGHT)

    # Initial user state
    have_name = False
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letter1 = 0   # A
    letter2 = 23  # X
    letter3 = 17  # R
    column = 0

    # Positions and sizes
    position = HEIGHT - (HEIGHT - 10)
    table_position = 250
    table_font_size = 30
    game_instruct_position = position + table_position + table_font_size * 9

    # Main loop
    while not have_name:
        # Draw title
        draw_title(screen, WIDTH)
        # Draw current name
        draw_current_name(screen, name, table_font_size, WIDTH, HEIGHT)
        draw_current_name(screen, "Click enter to continue", table_font_size, WIDTH, HEIGHT+400)
        # Draw new name
        new_name = alphabet[letter1] + alphabet[letter2] + alphabet[letter3]
        draw_new_name(screen, new_name, column, table_font_size, WIDTH, HEIGHT)
        # Handle key presses
        keystate = pygame.key.get_pressed()
        letter1, letter2, letter3, column = handle_key_presses(keystate, letter1, letter2, letter3, column)

        if keystate[pygame.K_RETURN]:
            have_name = True
            return new_name

        # Handle Pygame events such as quitting and key releases
        handle_events()
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        # Draw the background image on the screen
        screen.blit(background, background_rect)

# displays the start screen with the given parameters
def show_start_screen(name, min_size, max_size, colour, HEIGHT, WIDTH, background, background_rect, player_score, scores):

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    position = HEIGHT - (HEIGHT - 10)
    table_position = 250
    table_font_size = 30
    game_instruct_position = position + table_position + table_font_size * (len(scores) + 4)

    def rnd_colour():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b
        # prints the game name one letter at a time

    for i in range(len(name)): # print name of the game
        screen.blit(background, background_rect)  # draw the background
        draw_text(screen, name[0:i], max_size, WIDTH / 2, position, colour)
        pygame.display.flip()
        clock.tick(4)
        draw_text(screen, name[0:i], max_size, WIDTH / 2, position, HS_BG)

    waiting = True  # set waiting to true while on the start screen
    size = max_size
    grow = True

    while waiting:   # repeat till key pressed
        pygame.event.clear()
        if grow == True:
            size = size + 1
        else:
            size = size - 1

        if size > max_size:   # change colour on every max size
            grow = False
            colour = rnd_colour()
        elif size < min_size:
            grow = True
            colour = rnd_colour()

        draw_text(screen, name, size, WIDTH / 2, position, colour)  # draw game name in a random colour

        text = "Arrow keys to move, space to jump"
        draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, game_instruct_position, table_font_size * table_font_size / 2, table_font_size + 5, BLACK)
        draw_text(screen, text, table_font_size-5, WIDTH / 2, game_instruct_position, YELLOW)

        text = "Press a key to begin"
        draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, HEIGHT - 50, table_font_size * table_font_size / 2, table_font_size + 5, BLACK)
        draw_text(screen, text, table_font_size, WIDTH / 2, HEIGHT - 50, GREEN)

        # prints the high score table
        draw_rect(screen, 0, 250, WIDTH, table_font_size * 8, HS_BG)

        draw_text(screen, "High Score Table", table_font_size, WIDTH / 2, position + table_position, HS_TITLE)
        text = scores[0][0]
        text = text + "    " + scores[0][1]
        draw_text(screen, text, table_font_size + 10, WIDTH / 2, position + table_position + table_font_size, HS_TOP)
        for i in range(1, len(scores)): # print the high scores
            text = scores[i][0]
            text = text + "    " + scores[i][1]
            draw_text(screen, text, table_font_size, WIDTH / 2, position + table_position + table_font_size + i * 40, HS_REST)

        pygame.display.flip()
        clock.tick(FPS)
        screen.blit(background, background_rect)  # draw the background

        # handle Pygame events such as quitting and key releases.
        for event in pygame.event.get():  # check for key press
            if event.type == pygame.QUIT:  # check if quit button pressed
                pygame.quit()
            if event.type == pygame.KEYUP:
                #print("start screen KEYUP", event.type)
                waiting = False

def show_game_over_screen(name, min_size, max_size, colour, HEIGHT, WIDTH, background, background_rect, player_score, scores, pname, saveFile):

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    position = HEIGHT - (HEIGHT - 10)
    table_position = 250
    table_font_size = 30
    game_instruct_position = position + table_position + table_font_size * (len(scores) + 4)

    def rnd_colour():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    disp_scores = True
    waiting = True  # set waiting to true while on the start screen
    size = max_size
    grow = True
    while waiting:   # repeat till key pressed

        colour = rnd_colour()

        draw_text(screen, name, size, WIDTH / 2, position, colour) # draw game name in a random colour

        pygame.display.flip()
        screen.blit(background, background_rect)  # draw the background
        clock.tick(5)

        text = "Arrow keys to move, space to jump"
        draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, game_instruct_position, table_font_size * table_font_size / 2, table_font_size + 5, BLACK)
        draw_text(screen, text, table_font_size-5, WIDTH / 2, game_instruct_position, YELLOW)

        text = "Press a key to begin"
        draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, HEIGHT - 50, table_font_size * table_font_size / 2, table_font_size + 5, BLACK)
        draw_text(screen, text, table_font_size, WIDTH / 2, HEIGHT - 50, GREEN)

        high_score = False
        if player_score > int(scores[len(scores) - 1][1]):
            high_score = True
            place_in_table = new_high_score(pname, scores, player_score, saveFile)
            # check position of new high score here for use later to highlight the name
            score_on_table = player_score
            player_score = 0

        while disp_scores:
            screen.blit(background, background_rect)

            if high_score:
                draw_rect(screen, 0, position + table_position - (table_font_size * 3), WIDTH, table_font_size + 5, HS_BG)
                high_text = f"Score: {score_on_table} - High Score Pos: {place_in_table}"


                draw_text(screen, high_text, table_font_size, WIDTH / 2,
                          position + table_position - (table_font_size * 3), RED)
                draw_rect(screen, 0, 250, WIDTH, table_font_size * 8, HS_BG)

                draw_text(screen, "High Score Table", table_font_size, WIDTH / 2, position + table_position, HS_TITLE)
                text = scores[0][0]
                text = text + "    " + scores[0][1]
                draw_text(screen, text, table_font_size + 10, WIDTH / 2, position + table_position + table_font_size,
                          HS_TOP)
                for i in range(1, len(scores)):  # print the high scores
                    text = scores[i][0]
                    text = text + "    " + scores[i][1]
                    draw_text(screen, text, table_font_size, WIDTH / 2,
                              position + table_position + table_font_size + i * 40, HS_REST)

                text = "Press a key to go to game menu"
                draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, HEIGHT - 250, table_font_size * table_font_size / 2, table_font_size + 5, BLACK)
                draw_text(screen, text, table_font_size-5, WIDTH / 2, HEIGHT - 250, GREEN)

            elif player_score > 0:
                draw_rect(screen, 0, position + table_position - (table_font_size * 3), WIDTH, table_font_size + 5,
                          BLACK)
                high_text = "You Score was " + str(player_score) + " you needed over " + (
                    scores[len(scores) - 1][1])
                draw_text(screen, high_text, table_font_size, WIDTH / 2,
                          position + table_position - (table_font_size * 3), HS_TOP)

                draw_high_score_table(screen, table_font_size, position, table_position, WIDTH, scores)

                text = "Press a key to go to game menu"
                draw_rect(screen, (WIDTH / 2) - (table_font_size / 2) * 15, HEIGHT - 250, table_font_size * table_font_size / 2, table_font_size + 5, BLACK)
                draw_text(screen, text, table_font_size, WIDTH / 2, HEIGHT - 250, GREEN)

            else:
                disp_scores = False
            pygame.display.flip()

            # handle Pygame events such as quitting and key releases.
            for event in pygame.event.get():   # check for key press
                if event.type == pygame.QUIT:  # check if quit button pressed
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    disp_scores = False

        # prints the high score table
        draw_rect(screen, 0, position + table_position, WIDTH, table_font_size * 8, HS_BG)

        draw_text(screen, "High Score Table", table_font_size, WIDTH / 2, position + table_position, HS_TITLE)
        text = scores[0][0]
        text = text + "    " + scores[0][1]
        draw_text(screen, text, table_font_size + 10, WIDTH / 2, position + table_position + table_font_size, HS_TOP)
        for i in range(1, len(scores)):  # print the high scores
            text = scores[i][0]
            text = text + "    " + scores[i][1]
            draw_text(screen, text, table_font_size, WIDTH / 2, position + table_position + table_font_size + i * 40, HS_REST)

        # handle Pygame events such as quitting and key releases.
        for event in pygame.event.get():   # check for key press
            if event.type == pygame.QUIT:  # check if quit button pressed
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False



