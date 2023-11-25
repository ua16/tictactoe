#!/usr/bin/env python3

import pygame, sys
import random

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

WINDOW_SIZE = (1280,720)
DISPLAY_SIZE = (256, 144)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # The actual Size of the window

display = pygame.Surface(DISPLAY_SIZE) # Where we blit our pixel art to

main_menu_img_red = pygame.image.load("ttt_red.png")
main_menu_img_green = pygame.image.load("ttt_green.png")
main_menu_img_yellow = pygame.image.load("ttt_yellow.png")

start_button_img = pygame.image.load("startbutton.png")

cursor_img = pygame.image.load("cursor.png")


def game():
    running = True

    click = False
    board = [ " " , " " , " " ,
              " " , " " , " " ,
              " " , " " , " " ]
    
    bot = "o"
    player = "x"

    def insert_letter(letter, pos):
        if board[pos] == " ":
            board[pos] = letter
        else:
            print(board)
            print("That space isn't free. exiting")
            pygame.quit()
            exit()

    def count_empty_squares():
        count = 0
        for i in board:
            if i == " ":
                count += 1
        return count
            

    def is_winner(letter):
        if (board[0] == letter and board[1] == letter and board[2] == letter):
            return True
        if (board[3] == letter and board[4] == letter and board[5] == letter):
            return True
        if (board[6] == letter and board[7] == letter and board[8] == letter):
            return True
        if (board[0] == letter and board[3] == letter and board[6] == letter):
            return True
        if (board[1] == letter and board[4] == letter and board[7] == letter):
            return True
        if (board[2] == letter and board[5] == letter and board[8] == letter):
            return True
        if (board[0] == letter and board[4] == letter and board[8] == letter):
            return True
        if (board[6] == letter and board[4] == letter and board[2] == letter):
            return True
        else:
            return False

    def is_draw():
        for i in board:
            if i == " ":
                return False
        return True

    def player_move(pos):
        insert_letter(pos)

    
    def minimax(board , depth , is_maximizing):
        if is_winner(bot):
            return (1 * count_empty_squares() + 1)
        elif is_winner(player):
            return (-1 * count_empty_squares() - 1)
        elif is_draw():
            return 0
    
        elif is_maximizing:
            best_score = -800
    
            for pos in range(0,9):
                if board[pos] == " ":
                    board[pos] = bot
                    score = minimax(board , depth + 1, False)
                    board[pos] = " "
                    if score > best_score:
                        best_score = score
    
            return best_score
        else:
            best_score = 800
    
            for pos in range(0,9):
                if board[pos] == " ":
                    board[pos] = player
                    score = minimax(board, depth +1 , True)
                    board[pos] = " "
                    if score < best_score:
                        best_score = score
    
            return best_score

    def bot_move():
        best_score = -800
        best_move = 0
    
        for pos in range(0,9):
            if board[pos] == " ":
                board[pos] = bot
                score = minimax(board, 0 , False)
                board[pos] = " "
                if score > best_score:
                    best_score = score
                    best_move = pos
    
        insert_letter(bot, best_move)

    # Load Images

    grid_img = pygame.image.load("grid.png")

    xo_imgs = {"x":pygame.image.load("square.png") , "o":pygame.image.load("circle.png")}

    back_button_img = pygame.image.load("back_button.png")

    particle_imgs = [ pygame.image.load("particle_1.png") , pygame.image.load("particle_2.png")]

    # Count to end the game
    final_countdown = 0

    # Making Particles
    particle_list = []

    frame_count = 0
    background_offset = 0

    cursor_img_rect = cursor_img.get_rect()
    pygame.mouse.set_visible(False)
    
    print("Entered Game Loop")
    while running:
        display.fill("#282828")
        background_offset = (background_offset + 0.25) % 30
        for i in range(9):
            pygame.draw.line(display, (5, 18, 24), (int(i * 32 + background_offset - 200) , int(i * 32 + background_offset + 50)), (276, int(i * 32 - 128 + background_offset)), 15)

        # Drawing the grid
        display.blit(grid_img , (DISPLAY_SIZE[0]//2 - 48, DISPLAY_SIZE[1]//2 -48))

        mx , my = pygame.mouse.get_pos()

        # Particles
        if frame_count%30 == 0:
            particle_list.append(
                [mx//5,
                 my//5,
                 random.randrange(0 ,20) / 10 - 1,
                 1,
                 random.choice(particle_imgs),
                 random.randrange(30,60)]
            )
        

        # Drawing the particles

        for i in particle_list:
            display.blit(i[4],(i[0] , i[1]))
        # Moving particles
            i[0] += i[2]
            i[1] += i[3]
            i[5] -= 1

        particle_iterator = 0
        while particle_iterator < len(particle_list):
            if particle_list[particle_iterator][5] <= 0:
                particle_list.pop(particle_iterator)
            else:
                particle_iterator += 1



        # Setting up the buttons

        back_button = back_button_img.get_rect(topleft=(8 , 8))
        display.blit(back_button_img, (8, 8))

        grid_buttons = [
            pygame.Rect(80 , 24 , 32, 32),
            pygame.Rect(112 , 24 , 32 , 32),
            pygame.Rect( 144 , 24 , 32 , 32),

            pygame.Rect(80, 56 , 32 , 32),
            pygame.Rect(112 , 56 , 32 , 32),
            pygame.Rect(144 , 56 , 32 , 32),

            pygame.Rect(80 , 88 , 32 , 32),
            pygame.Rect(112 , 88, 32 , 32),
            pygame.Rect(144, 88, 32 , 32),
            
        ]

        # Setting up the functions for the buttons


        if click:
            if back_button.collidepoint((mx//5,my//5)):
                print("Exiting Game Loop")
                running = False

            for i in range(0,9):
                if grid_buttons[i].collidepoint((mx//5,my//5)):
                    if board[i] == " ":
                        insert_letter(player , i)
                        if count_empty_squares() > 0:
                            bot_move()
                    else:
                        # Play error sound
                        pass


        # Filling the board with squares and circles according to the placements

        if board[0] != " ":
            display.blit(xo_imgs[board[0]] , (DISPLAY_SIZE[0]//2 - 48, DISPLAY_SIZE[1]//2 - 48))
        if board[1] != " ":
            display.blit(xo_imgs[board[1]] , (DISPLAY_SIZE[0]//2 - 16, DISPLAY_SIZE[1]//2 - 48))
        if board[2] != " ":
            display.blit(xo_imgs[board[2]] , (DISPLAY_SIZE[0]//2 + 16, DISPLAY_SIZE[1]//2 - 48))

        if board[3] != " ":
            display.blit(xo_imgs[board[3]] , (DISPLAY_SIZE[0]//2 - 48, DISPLAY_SIZE[1]//2 - 16))
        if board[4] != " ":
            display.blit(xo_imgs[board[4]] , (DISPLAY_SIZE[0]//2 - 16, DISPLAY_SIZE[1]//2 - 16))
        if board[5] != " ":
            display.blit(xo_imgs[board[5]] , (DISPLAY_SIZE[0]//2 + 16, DISPLAY_SIZE[1]//2 - 16))

        if board[6] != " ":
            display.blit(xo_imgs[board[6]] , (DISPLAY_SIZE[0]//2 - 48, DISPLAY_SIZE[1]//2 + 16))
        if board[7] != " ":
            display.blit(xo_imgs[board[7]] , (DISPLAY_SIZE[0]//2 - 16, DISPLAY_SIZE[1]//2 + 16))
        if board[8] != " ":
            display.blit(xo_imgs[board[8]] , (DISPLAY_SIZE[0]//2 + 16, DISPLAY_SIZE[1]//2 + 16))

        # End of drawing the pieces on the board

        if is_winner(player):
            final_countdown += 1
        elif is_winner(bot):
            final_countdown += 1
        elif is_draw():
            final_countdown += 1

        if final_countdown == 300:
            running = False
            

        
            
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if frame_count > 60:
            frame_count = 0
        else:
            frame_count += 1
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img , cursor_img_rect)
        pygame.display.update()
        clock.tick(60)

def main_menu():
    running = True
    frame_count = 0 # How many frames have been displayed or smthn

    click = False

    cursor_img_rect = cursor_img.get_rect()
    pygame.mouse.set_visible(False)


    print("Entered Loop")
    while running:
        display.fill("#282828")

        start_button = start_button_img.get_rect(topleft=(DISPLAY_SIZE[0]//2 -32 , DISPLAY_SIZE[1]//2 -8))
        display.blit(start_button_img,(DISPLAY_SIZE[0]//2 -32 , DISPLAY_SIZE[1]//2 -8))

        if frame_count == 60:
            frame_count = 0
        else:
            frame_count += 1

        if frame_count <= 15:
            display.blit(main_menu_img_red,(0,0))
        elif frame_count <= 30:
            display.blit(main_menu_img_yellow,(0,0))
        elif frame_count <= 45:
            display.blit(main_menu_img_green,(0,0))
        elif frame_count <= 60:
            display.blit(main_menu_img_yellow,(0,0))

        mx , my = pygame.mouse.get_pos()

        # We divide by 5 as the surface we blit the rect to is 5 times smaller before scaling
        if start_button.collidepoint((mx//5,my//5)) and click:
            game()

            
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img , cursor_img_rect)
        pygame.display.update()
        clock.tick(60)
            
main_menu()
