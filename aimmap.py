import pygame
import time
import random
import keyboard
import os
import win32gui
import win32api
import win32con

os.environ['SDL_VIDEO_CENTERED'] = "1"
 
pygame.init()
 
display_width = 1344
display_height = 756
 
black = (0,0,0)
white = (255,255,255)

green = (0, 200, 0)
bright_green = (0, 255, 0)

red = (200,0,0)
bright_red = (255,0,0)
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Aim map')
clock = pygame.time.Clock()

def text_objects(text, font):
    
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def click(x,y):
    x1, y1 = 0, 0
    fg_win = win32gui.GetForegroundWindow()
    x1, y1 = win32gui.ClientToScreen(fg_win, (x, y))
    x1 += 1
    y1 += 1
    win32api.SetCursorPos((x1,y1))
    

def normal_button(x, y):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+150 > mouse[0] > x and y+75 > mouse[1] > y:
        pygame.draw.rect(gameDisplay, bright_green,(x, y, 150,75))
        return True
    else:
        pygame.draw.rect(gameDisplay, green,(x, y,150,75))
    return False

def button(x, y):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+20 > mouse[0] > x and y+20 > mouse[1] > y:
        pygame.draw.rect(gameDisplay, bright_red,(x, y,20,20))
        return True
    else:
        pygame.draw.rect(gameDisplay, red,(x, y,20,20))
    return False
    

def game_intro():
        
        intro = True
        x = random.randint(96, 1248)
        y = random.randint(54, 702)
        store = False
        points = 0
        counter = 30
        green_button = False

        timesup  = True
        font = pygame.font.SysFont(None, 25)
        timer = font.render("Timer: "+str(counter), True, black)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if green_button:
                        counter = 30
                        points = 0
                        green_button = False
                        timesup = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if store:
                        x = random.randint(96, 1248)
                        y = random.randint(100, 700)
                        points += 1
                    
                        
                if event.type == pygame.USEREVENT: 
                    counter -= 1
                
                    timer = font.render("Timer: "+str(counter), True, black)
                    if counter <= 0:
                        timer = font.render("" , True, black)
                        store = False
                        timesup = True
            gameDisplay.fill(white)

            if not timesup:   
                text = font.render("Points: "+str(points), True, black)
                
                gameDisplay.blit(timer,(1257,10))
                gameDisplay.blit(text,(10,10))
                store = button(x, y)
                if keyboard.is_pressed('q'):
                    timesup  = True
                if keyboard.is_pressed('w'):
                    click(x ,y)
                
            else:
                fontGameOver = pygame.font.SysFont(None, 100)
                textSurf, textRect = text_objects("Game Over!", fontGameOver)
                textRect.center = (display_width / 2), (display_height / 2 -200)
                gameDisplay.blit(textSurf, textRect)
                
                fontPoints = pygame.font.SysFont(None, 70)
                
                textSurf, textRect = text_objects("Points: "+str(points), fontPoints)
                textRect.center = (display_width / 2), (display_height / 2 -100)
                gameDisplay.blit(textSurf, textRect)
                
                green_button = normal_button(597, 350)
                    
                    
                
            pygame.display.update()
            clock.tick(60)

    
 
game_intro()

print("Game Ended!")
    
pygame.quit()
quit()


