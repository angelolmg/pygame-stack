import pygame, sys
from random import randint
from pygame.locals import *

def move_last_rect():
    global speed
    n = len(rect_list)
    
    if n > 0:
        rect_list[n - 1].move_ip(speed, 0)
        if rect_list[n - 1].left > (screen_w - rect_w) or rect_list[n - 1].left < 0:
            speed *= -1
        
def draw_game(screen):
    screen.fill(white_color)

    for i in range(len(rect_list)):
        pygame.draw.rect(screen, color_list[i], rect_list[i])
    
    if len(game_message) > 0:
        if game_message == WIN_MESSAGE:
            text = font.render(game_message, True, (0,255,0))
            screen.blit(text, ((screen_w - text.get_width())/2, (screen_h - text.get_height())/2))
        if game_message == LOSE_MESSAGE:
            text = font.render(game_message, True, (255,0,0))
            screen.blit(text, ((screen_w - text.get_width())/2, (screen_h - text.get_height())/2))

    pygame.display.update()

def get_next_rect():

    global total_stacked
    global rect_w, rect_h
    global rect_list, color_list
    
    px = (screen_w - rect_w)/2
    py = screen_h - total_stacked * rect_h

    color_list.append((randint(0, 200), randint(0, 200), randint(0, 200)))
    rect_list.append(pygame.Rect(px, py, rect_w, rect_h))

    if (total_stacked > total_stacks_to_win) and (game_state == RUN_STATE):
        win_game()

    total_stacked += 1
    
def win_game():
    global game_message, game_state
    game_message = WIN_MESSAGE
    game_state = PAUSE_STATE

def lose_game():
    print("lost")
    global game_message, game_state
    game_message = LOSE_MESSAGE
    game_state = PAUSE_STATE

def adjust_width():

    if len(rect_list) > 1:
        global rect_w
        last_index = len(rect_list) - 1

        last_rect = rect_list[last_index]
        before_last_rect = rect_list[last_index - 1]

        # LOST STATE
        if (last_rect.left >= before_last_rect.right or
            last_rect.right <= before_last_rect.left):
            lose_game()
        
        # LEFT WING SUPER-POSITION
        if (last_rect.left < before_last_rect.left and
            last_rect.right < before_last_rect.right):
            rect_w = last_rect.right - before_last_rect.left

        # RIGHT WING SUPER-POSITION
        elif (last_rect.left > before_last_rect.left and
            last_rect.right > before_last_rect.right):
            rect_w = before_last_rect.right - last_rect.left 

        if (rect_w > last_rect.width):
            rect_w = last_rect.width

def reset_game():
    global rect_list, color_list
    global speed, total_stacked
    global game_message 
    global rect_w, rect_h
    
    rect_list = []
    color_list = []
    speed = base_speed
    total_stacked = 1
    game_message = ""
    rect_w, rect_h = base_rect_proportions

    get_next_rect()
    get_next_rect()

# MAIN
pygame.init()
pygame.display.set_caption("Stack It Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 240)

LOSE_MESSAGE = "FAIL"
WIN_MESSAGE = "WIN"

RUN_STATE = "RUNNING"
PAUSE_STATE = "PAUSED"

screen_w, screen_h = (500, 550)
base_rect_proportions = (300, 40)
rect_w, rect_h = base_rect_proportions

base_speed = 2
speed = base_speed
speed_increase_multiplier = 1.3

total_stacked = 1
total_stacks_to_win = int(screen_h/rect_h) + 1

screen = pygame.display.set_mode((screen_w, screen_h))

white_color = (255, 255, 255)
blue_color = (0, 0, 255)
game_message = ""
game_state = RUN_STATE

rect_list = []
color_list = []

screen.fill(white_color)
get_next_rect()
get_next_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if(game_state == RUN_STATE):
                    adjust_width()
                    get_next_rect()
                    speed *= speed_increase_multiplier
                elif(game_state == PAUSE_STATE):
                    reset_game()
                    game_state = RUN_STATE
                
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw_game(screen)
    move_last_rect()
     
    clock.tick(60)
    