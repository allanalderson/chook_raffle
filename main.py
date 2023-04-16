import random
import sys
import time
import pygame
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Chook Raffle Video Display")
RANGE_MIN = 1
RANGE_MAX = 1111
FPS = 15
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DARK = (0, 0, 0)
GOLD = (250, 190, 80)
GREY = (180, 180, 190)
BLACK = (0, 0, 0)
WHITE = (250, 250, 255)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
winner_peek = 0
winner_known = True
spin_stopped = False
my_font = pygame.font.SysFont('Arial', 700)  # 490
# Create an empty list to store surfaces ready to be blited:
surface_gold = []
for i in range(10):
    surface_gold.append(my_font.render(str(i), True, GOLD))
surface_grey = []
for i in range(10):
    surface_grey.append(my_font.render(str(i), True, GREY))
surface_dark = []
for i in range(10):
    surface_dark.append(my_font.render(str(i), True, DARK))

rect_width = surface_grey[0].get_width()
rect_height = surface_grey[0].get_height()
rect_surface = pygame.Surface((rect_width, rect_height))
rect_surface.fill((0, 0, 100))  # Fill with blue color
rect_surface.set_alpha(128)

class Screendigit:
    def __init__(self, x_pos, y_pos, winning_digit, suspence_digit, displayed_digit, resolved, reveal_timer):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.winning_digit = winning_digit
        self.suspence_digit = suspence_digit
        self.displayed_digit = displayed_digit
        self.resolved = resolved
        self.reveal_timer = reveal_timer


# Create an empty list to store instance position values
digit_position = []

# Generate 4 positions (SingleDigits) each with arguments and add them to the list
for i in range(4):
    SingleDigit = Screendigit(0, 0, 0, 0, 0, 0, 0)
    SingleDigit.x_pos = 1300 - (i * 400)
    SingleDigit.y_pos = 200
    SingleDigit.winning_digit = 0
    SingleDigit.suspence_digit = 0
    SingleDigit.displayed_digit = 0
    SingleDigit.resolved = False
    SingleDigit.reveal_timer = int(time.time() -1)
    digit_position.append(SingleDigit)


def draw_winning_ticket():
    global winner_peek
    """  Gets the winning ticket. Also splits this winning number into relevant positions (units, tens, hundreds, thousands) """
    global winner_known
    if winner_known == False:
        winning_ticket = random.randint(RANGE_MIN, RANGE_MAX + 1)
        winning_ticket = 8
        if winning_ticket > 9999:
            winning_ticket = 0
        if winning_ticket < 0:
            winning_ticket = 0
        winner_peek = winning_ticket
        digit_position[0].winning_digit = (winning_ticket // 1 % 10)
        digit_position[1].winning_digit = (winning_ticket // 10 % 10)
        digit_position[2].winning_digit = (winning_ticket // 100 % 10)
        digit_position[3].winning_digit = (winning_ticket // 1000 % 10)
        winner_known = True


def draw_suspence_ticket():
    global suspence_ticket
    suspence_ticket = random.randint(RANGE_MIN, RANGE_MAX + 1)
    digit_position[0].suspence_digit = (suspence_ticket // 1 % 10)
    digit_position[1].suspence_digit = (suspence_ticket // 10 % 10)
    digit_position[2].suspence_digit = (suspence_ticket // 100 % 10)
    digit_position[3].suspence_digit = (suspence_ticket // 1000 % 10)




def start_reveal_timers():
    digit_position[3].reveal_timer = int(time.time() + 0)  # 0
    digit_position[2].reveal_timer = int(time.time() + 1)  # 1
    digit_position[1].reveal_timer = int(time.time() + 2)  # 4
    digit_position[0].reveal_timer = int(time.time() + 3)  # 8



def update_logic():
    '''waits for the reveal timers to expire then moves the winning digit into  displayed digit then marks position resolved to true
    or either Spins or stops the wheels when necessary.'''
    global winner_known
    global spin_stopped
    global winner_peek
    if spin_stopped == False:
        for i in range(4):
            if digit_position[i].resolved == False:
                digit_position[i].displayed_digit =  digit_position[i].suspence_digit # random.randint(0, 9)
        if all([digit_position[0].resolved, digit_position[1].resolved, digit_position[2].resolved,
                digit_position[3].resolved]):
            spin_stopped = True
            print("STOPPED AT", winner_peek)
            print()
            update_display()
            time.sleep(1)
            pygame.event.get()  # removes superfulous key strokes from buffer
    if winner_known == True:
        for i in range(4):
            if int(time.time()) > digit_position[i].reveal_timer:
                digit_position[i].displayed_digit = digit_position[i].winning_digit
                digit_position[i].resolved = True




def update_display():
    ''' Draws  displayed_digit with a grey surface then removes leading zeros. '''
    global winner_peek
    screen.fill(BLACK)

    for i in range(4):
        screen.blit(surface_grey[digit_position[i].displayed_digit], (digit_position[i].x_pos, digit_position[i].y_pos))

    if digit_position[3].resolved:
        if winner_peek < 1000:
            screen.blit(rect_surface, (digit_position[3].x_pos, digit_position[3].y_pos))
    if digit_position[2].resolved:
        if winner_peek < 100:
            screen.blit(rect_surface, (digit_position[2].x_pos, digit_position[2].y_pos))
    if digit_position[1].resolved:
        if winner_peek < 10:
            screen.blit(rect_surface, (digit_position[1].x_pos, digit_position[1].y_pos))





def spin():
    '''marks all digits to resolved False'''
    global spin_stopped
    global winner_known

    print("      SPINNING . . .")
    spin_stopped = False
    winner_known = False
    for i in range(4):
        digit_position[i].resolved = False


draw_suspence_ticket()
#draw_winning_ticket()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                if winner_known == False and spin_stopped == False:  # show winner
                    draw_winning_ticket()
                    start_reveal_timers()
                    print("   SLOWING TO", winner_peek)
                elif spin_stopped:
                    spin()
    draw_suspence_ticket()
    update_logic()
    update_display()
    pygame.display.flip()
    FramePerSec.tick(FPS)
