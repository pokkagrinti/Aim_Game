# To do:
#   1)Make sure start and end matches.
#       -Take last element in list and compare to click destination
#       -if (x orgin - x dest) < 5  and (y orgin - y dest) < 5
#       -if not remove


import pygame
import random
import keyboard
import os
import win32gui
import win32api
import time
import threading

os.environ['SDL_VIDEO_CENTERED'] = "1"

# Global Variables
DISPLAY_WIDTH = 1344
DISPLAY_HEIGHT = 756

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)

RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)

RED_BUTTON_SIZE = 20

stop_thread = False
recording_mouse = False
mouse_path_list = []


def text_objects(text, fontsize):
    """Set text's size and color"""
    font = pygame.font.SysFont(None, fontsize)
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def button(screen, x, y):
    mouse = pygame.mouse.get_pos()
    if x + 20 > mouse[0] > x and y + 20 > mouse[1] > y:
        pygame.draw.rect(screen, BRIGHT_RED, (x, y, 20, 20))
        return mouse
    else:
        pygame.draw.rect(screen, RED, (x, y, 20, 20))
    return False


def draw_red_button(screen, x, y):
    """Draw an interactive red button on screen"""
    mouse_position = pygame.mouse.get_pos()
    mouse_pos_x = mouse_position[0]
    mouse_pos_y = mouse_position[1]

    if x + RED_BUTTON_SIZE > mouse_pos_x > x and y + RED_BUTTON_SIZE > mouse_pos_y > y:
        pygame.draw.rect(screen, BRIGHT_RED, (x, y, RED_BUTTON_SIZE, RED_BUTTON_SIZE))
        return mouse_position
    else:
        pygame.draw.rect(screen, RED, (x, y, RED_BUTTON_SIZE, RED_BUTTON_SIZE))
    return False


def draw_green_button(screen, x, y):
    """Draw an interactive green button on screen"""
    mouse_position = pygame.mouse.get_pos()
    mouse_pos_x = mouse_position[0]
    mouse_pos_y = mouse_position[1]

    if x + 150 > mouse_pos_x > x and y + 75 > mouse_pos_y > y:
        pygame.draw.rect(screen, BRIGHT_GREEN, (x, y, 150, 75))
        return True
    else:
        pygame.draw.rect(screen, GREEN, (x, y, 150, 75))
    return False


def timer_text(screen, time_left):
    """Display a countdown Timer in the game"""
    textSurf, textRect = text_objects("Timer: " + str(time_left), 25)

    # Set Timer text at top right corner
    return screen.blit(textSurf, (1257, 10))


def points_text(screen, points):
    """Display the current point in the game"""
    textSurf, textRect = text_objects("Points: " + str(points), 25)

    # Set Points text at top left corner
    return screen.blit(textSurf, (10, 10))


def click(x, y):
    """Aimbot easter egg in the game."""
    fg_win = win32gui.GetForegroundWindow()
    x1, y1 = win32gui.ClientToScreen(fg_win, (x, y))
    x1 += 1
    y1 += 1
    win32api.SetCursorPos((x1, y1))


def record_mouse():
    """Records mouse movement and save it to a list"""
    global mouse_path_list
    while True:
        time.sleep(0.025)

        global recording_mouse
        if recording_mouse:
            x, y = pygame.mouse.get_pos()
            time_of_coords = len(mouse_path_list)
            mouse_path_list.append((x, y, time_of_coords))

        global stop_thread
        if stop_thread:
            break


def main():
    global stop_thread
    global recording_mouse
    global mouse_path_list

    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Aim map')

    button_location_x = random.randint(86, 1238)
    button_location_y = random.randint(44, 692)

    # Game Information
    points = 0

    timer_secs = 30
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    cursor_coordinates = False

    times_up = True
    reset = True

    t1 = threading.Thread(target=record_mouse)
    t1.start()

    file_counter = 1
    exist = True

    while exist:
        file_path = "./Recordings/recording" + str(file_counter) + ".txt"
        exist = os.path.isfile(file_path)

    with open(file_path, "w") as f:
        done = 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = 1
                    break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if cursor_coordinates:
                        recording_mouse = True
                        if mouse_path_list:
                            f.write(str(mouse_path_list) + "\n")
                        f.write("Mouse: %s\n" % str(pygame.mouse.get_pos()))
                        mouse_path_list = []
                        points += 1
                        button_location_x = random.randint(86, 1238)
                        button_location_y = random.randint(44, 692)
                    elif reset:
                        timer_secs = 30
                        points = 0
                        reset = False
                        times_up = False
                elif event.type == pygame.USEREVENT:
                    if timer_secs > 0:
                        timer_secs -= 1
                    else:
                        times_up = True

                        # Disable red button
                        cursor_coordinates = False

            screen.fill(WHITE)

            if times_up:
                recording_mouse = False

                textSurf, textRect = text_objects("Game Over!", 100)
                textRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2 - 200)
                screen.blit(textSurf, textRect)

                textSurf, textRect = text_objects("Points: " + str(points), 70)
                textRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2 - 100)
                screen.blit(textSurf, textRect)

                reset = draw_green_button(screen, 597, 350)


            else:
                timer_text(screen, timer_secs)
                points_text(screen, points)

                # If cursor coordinates is in the button, store it in cursor_coordinates
                cursor_coordinates = draw_red_button(screen, button_location_x, button_location_y)

                if keyboard.is_pressed('q'):
                    times_up = True

                    # Disable red button
                    cursor_coordinates = False

                if keyboard.is_pressed('w'):
                    # Easter egg
                    click(button_location_x, button_location_y)

            pygame.display.update()
            clock.tick(60)

    stop_thread = True
    t1.join()


if __name__ == "__main__":
    main()
