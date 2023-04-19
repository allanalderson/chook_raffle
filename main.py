import random
import sys
import time
import pygame
from pygame.locals import *
pygame.init()
pygame.display.set_caption("  Chook Raffle Video Display V1.0  ")
RANGE_MIN = 1
RANGE_MAX = 199
FPS = 12
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (0, 0, 0)
GOLD = (250, 200, 90)
GREY = (170, 180, 190)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
winner_peek = 0
winner_known = True
spin_stopped = False
my_font = pygame.font.SysFont('Arial', 700)  # 490
# Create an empty list to store surfaces ready to be blited:
surface_gold = []
surface_grey = []
for i in range(10):
    surface_gold.append(my_font.render(str(i), True, GOLD))
    surface_grey.append(my_font.render(str(i), True, GREY))


rect_width = surface_grey[0].get_width()
rect_height = surface_grey[0].get_height()
rect_surface = pygame.Surface((rect_width, rect_height))
rect_surface.fill(BACKGROUND_COLOR)
# rect_surface.set_alpha(128)

class Screendigit:
    def __init__(self, x_pos, y_pos, winning_digit, suspense_digit, displayed_digit, resolved, reveal_timer):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.winning_digit = winning_digit
        self.suspense_digit = suspense_digit
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
    SingleDigit.suspense_digit = 0
    SingleDigit.displayed_digit = 0
    SingleDigit.resolved = False
    SingleDigit.reveal_timer = int(time.time() -1)
    digit_position.append(SingleDigit)


def draw_winning_ticket():
    global winner_peek
    """  Gets the winning ticket. Also splits this winning number into
     relevant positions (units, tens, hundreds, thousands) """
    global winner_known
    if winner_known == False:
        winning_ticket = random.randint (RANGE_MIN, RANGE_MAX)
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


def draw_suspense_ticket():
    global suspense_ticket
    suspense_ticket = random.randint(RANGE_MIN, RANGE_MAX)
    digit_position[0].suspense_digit = (suspense_ticket // 1 % 10)
    digit_position[1].suspense_digit = (suspense_ticket // 10 % 10)
    digit_position[2].suspense_digit = (suspense_ticket // 100 % 10)
    digit_position[3].suspense_digit = (suspense_ticket // 1000 % 10)



def start_reveal_timers():
    digit_position[3].reveal_timer = int(time.time() + -1)  # 0
    digit_position[2].reveal_timer = int(time.time() + 1)  # 1
    digit_position[1].reveal_timer = int(time.time() + 3)  # 4
    digit_position[0].reveal_timer = int(time.time() + 7)  # 8



def update_logic():
    '''waits for the reveal timers to expire then moves the winning digit into  displayed digit then marks position resolved to true
    or either Spins or stops the wheels when necessary.'''
    global winner_known
    global spin_stopped
    global winner_peek
    if spin_stopped == False:
        for i in range(4):
            if digit_position[i].resolved == False:
                digit_position[i].displayed_digit =  digit_position[i].suspense_digit # random.randint(0, 9)
        if all([digit_position[0].resolved, digit_position[1].resolved, digit_position[2].resolved,
                digit_position[3].resolved]):
            spin_stopped = True
            print("STOPPED AT", winner_peek)
            print()
            update_display()
            pygame.display.flip()
            time.sleep(2)
            pygame.event.get()  # removes key strokes from buffer
    if winner_known == True:
        for i in range(4):
            if int(time.time()) > digit_position[i].reveal_timer:
                digit_position[i].displayed_digit = digit_position[i].winning_digit
                digit_position[i].resolved = True




def update_display():
    ''' Draws  displayed_digit with a grey surface then removes leading zeros. '''
    global winner_peek
    global suspense_ticket
    global spin_stopped
    screen.fill(BACKGROUND_COLOR)
    for i in range(4):
        screen.blit(surface_grey[digit_position[i].displayed_digit], (digit_position[i].x_pos, digit_position[i].y_pos))
        if digit_position[3].resolved == False:
            if suspense_ticket < 1000:
                if digit_position[3].suspense_digit == 0:
                    screen.blit(rect_surface, (digit_position[3].x_pos, digit_position[3].y_pos))
        if digit_position[2].resolved == False:
            if suspense_ticket < 100:
                if digit_position[2].suspense_digit == 0:
                    screen.blit(rect_surface, (digit_position[2].x_pos, digit_position[2].y_pos))
        if digit_position[1].resolved == False:
            if suspense_ticket < 10:
                if digit_position[1].suspense_digit == 0:
                    screen.blit(rect_surface, (digit_position[1].x_pos, digit_position[1].y_pos))
        # Turn the winner Gold
        if spin_stopped:
            for i in range(4):
                screen.blit(surface_gold[digit_position[i].displayed_digit],
                            (digit_position[i].x_pos, digit_position[i].y_pos))
        # Erase the leading zeros of the winners blit with a rectangle
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
    for i in range(4):
        digit_position[i].resolved = False
    spin_stopped = False
    winner_known = False


draw_suspense_ticket()
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
    draw_suspense_ticket()
    update_logic()
    update_display()
    pygame.display.flip()
    FramePerSec.tick(FPS)
