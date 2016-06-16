import pygame
import time
from pygame.locals import *

pygame.init()
pygame.joystick.init()
my_joystick = None

        # By default, load the first available joystick.
if (pygame.joystick.get_count() > 0):
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

    while(True):
        g_keys = pygame.event.get()
        print [ my_joystick.get_button(i) for i in range(0, my_joystick.get_numbuttons())]
        print [ my_joystick.get_axis(i) for i in range(0, my_joystick.get_numaxes())]
        time.sleep(1)