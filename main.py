import pygame
import random
from random import randint
import time
from collections import deque
import math

pygame.init()

# FPS
clock = pygame.time.Clock()
FPS = 60

# TIME LIMIT
TIME_LIMIT = 10000

# SCREEN SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# NUMBER OF ROWS/COLS
SQUARE_PER_ROW = 20
SQUARE_PER_COL = 20


# SPOT DIMENSIONS
SPOT_WIDTH = SCREEN_WIDTH // SQUARE_PER_COL
SPOT_HEIGHT = SCREEN_HEIGHT // SQUARE_PER_ROW

# FONTS FOR MENU
HEADER_1 = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.05))
HEADER_2 = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.04))


# FONTS FOR IN-GAME 
FONT_BIG = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.03))
FONT_SMALL = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.02))
FONT_SPOT = pygame.font.Font("freesansbold.ttf", int(SPOT_WIDTH * 0.9))


# SNAKE SPEED (lower value --> faster)
snake_speed = 65

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)  # Yellow for Medium
MAROON = (128, 0, 0)    # Maroon for Insane
PURPLE = (200, 0, 255)
TURQUOISE = (48, 213, 200)
BLUEBERRY_BLUE = (79, 134, 247)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Snake")

# Define colors for difficulty levels
EASY_COLOR = (0, 255, 0)      # Green for Easy
MEDIUM_COLOR = (255, 255, 0)  # Yellow for Medium
HARD_COLOR = (255, 0, 0)      # Red for Hard
INSANE_COLOR = (128, 0, 0)    # Maroon for Insane

def draw_galaxy():
    # Function to draw a more refined swirling galaxy effect
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    num_stars = 100
    max_radius = 250
    max_speed = 0.02
    for i in range(num_stars):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(50, max_radius)
        speed = random.uniform(0, max_speed)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        # Update the position of the stars in a gentle circular motion
        angle += speed
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        # Draw the star with a softer color palette and slight transparency effect
        size = random.randint(1, 2)
        color = (200, 200, 255)  # Soft light blue with slight white
        alpha = random.randint(100, 180)  # Transparency for smoother blending
        star_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, color + (alpha,), (size, size), size)
        SCREEN.blit(star_surface, (x - size, y - size))

def draw_menu():
    # Define padding and spacing as proportions of the window size
    PADDING = int(SCREEN_WIDTH * 0.05)  # 5% of screen width
    SPACING = int(SCREEN_HEIGHT * 0.1)  # 10% of screen height

    # Render text for difficulty levels
    easy_button = FONT_BIG.render("Easy", True, BLACK)
    medium_button = FONT_BIG.render("Medium", True, BLACK)
    hard_button = FONT_BIG.render("Hard", True, BLACK)
    insane_button = FONT_BIG.render("Insane", True, BLACK)

    # Calculate rectangle dimensions based on text size
    easy_rect = pygame.Rect(SCREEN_WIDTH // 2 - easy_button.get_width() // 2 - PADDING,
                             SCREEN_HEIGHT // 2 - 150,
                             easy_button.get_width() + PADDING * 2,
                             easy_button.get_height() + PADDING)

    medium_rect = pygame.Rect(SCREEN_WIDTH // 2 - medium_button.get_width() // 2 - PADDING,
                               easy_rect.bottom + SPACING,
                               medium_button.get_width() + PADDING * 2,
                               medium_button.get_height() + PADDING)

    hard_rect = pygame.Rect(SCREEN_WIDTH // 2 - hard_button.get_width() // 2 - PADDING,
                             medium_rect.bottom + SPACING,
                             hard_button.get_width() + PADDING * 2,
                             hard_button.get_height() + PADDING)

    insane_rect = pygame.Rect(SCREEN_WIDTH // 2 - insane_button.get_width() // 2 - PADDING,
                               hard_rect.bottom + SPACING,
                               insane_button.get_width() + PADDING * 2,
                               insane_button.get_height() + PADDING)

    # Smoothly transition background colors (Dynamic Gradient)
    time_elapsed = time.time() % 10  # Create a loop for color transition
    r = int(100 + 50 * math.sin(time_elapsed))
    g = int(100 + 50 * math.cos(time_elapsed))
    b = int(150 + 50 * math.sin(time_elapsed / 2))
    SCREEN.fill((r, g, b))

    # Draw the galaxy effect (should be on the background)
    draw_galaxy()

    # Draw rectangles for each difficulty level with hover effect
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Hover effect for buttons
    if easy_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, (0, 200, 0), easy_rect, 5)  # Glowing effect
        pygame.draw.rect(SCREEN, (255, 255, 255), easy_rect, 3)  # Rounded border
    else:
        pygame.draw.rect(SCREEN, EASY_COLOR, easy_rect)

    if medium_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, (255, 255, 0), medium_rect, 5)
        pygame.draw.rect(SCREEN, (255, 255, 255), medium_rect, 3)
    else:
        pygame.draw.rect(SCREEN, MEDIUM_COLOR, medium_rect)

    if hard_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, (200, 0, 0), hard_rect, 5)
        pygame.draw.rect(SCREEN, (255, 255, 255), hard_rect, 3)
    else:
        pygame.draw.rect(SCREEN, HARD_COLOR, hard_rect)

    if insane_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, (200, 0, 0), insane_rect, 5)
        pygame.draw.rect(SCREEN, (255, 255, 255), insane_rect, 3)
    else:
        pygame.draw.rect(SCREEN, INSANE_COLOR, insane_rect)

    title = HEADER_1.render("Welcome to Math Snake", True, BLACK)
    selectLevel = HEADER_2.render("Select Difficulty Level", True, BLACK)

    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.1))
    SCREEN.blit(selectLevel, (SCREEN_WIDTH // 2 - selectLevel.get_width() // 2, SCREEN_HEIGHT * 0.2))

    # Blit buttons centered within their rectangles
    SCREEN.blit(easy_button, (easy_rect.x + PADDING, easy_rect.y + PADDING // 2))
    SCREEN.blit(medium_button, (medium_rect.x + PADDING, medium_rect.y + PADDING // 2))
    SCREEN.blit(hard_button, (hard_rect.x + PADDING, hard_rect.y + PADDING // 2))
    SCREEN.blit(insane_button, (insane_rect.x + PADDING, insane_rect.y + PADDING // 2))

    # Change cursor to hand when hovering over buttons
    if easy_rect.collidepoint(mouse_x, mouse_y) or medium_rect.collidepoint(mouse_x, mouse_y) or \
            hard_rect.collidepoint(mouse_x, mouse_y) or insane_rect.collidepoint(mouse_x, mouse_y):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    pygame.display.update()

    return easy_rect, medium_rect, hard_rect, insane_rect

def get_difficulty():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):
                    return "Easy"
                elif medium_rect.collidepoint(mouse_pos):
                    return "Medium"
                elif hard_rect.collidepoint(mouse_pos):
                    return "Hard"
                elif insane_rect.collidepoint(mouse_pos):
                    return "Insane"

        SCREEN.fill(WHITE)
        easy_rect, medium_rect, hard_rect, insane_rect = draw_menu()  # Get rectangles
        pygame.display.update()

######################
class QuestionWindow():
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.digitsStart = [1, 10, 100]
        self.digitsEnd = [9,99,999]
        self.mathSymbols = ["+", "-", "*"]
        self.sign = [-1, 1]
    
    # only + and - type problems
    def createEasy(self):
        varCount = randint(2,4)
        def limit(): return randint(1, 99)
        expression = ""

        if varCount == 2:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()}"

        elif varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()}"

        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()}"

        return expression
    
    # + - * /
    def createMedium(self):
        varCount = randint(2,4)
        def limit(): return randint(1, 999)
        expression = ""

        if varCount == 2:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} {limit()}"

        elif varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()}"

        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()}"

        return expression
        

    # + - * and -ve
    def createHard(self):
        varCount = randint(2,4)
        def limit():
            number = randint(-999, 999)
            while -100 <= number <= 100: 
                number = randint(-999, 999)

            return number 

        expression = ""

        if varCount == 2:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()})"

        elif varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()}"

        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()})"

        return expression

    # + - * and -ve but with hundreds to thousands
    def createInsane(self):
        varCount = randint(3,4)
        def limit(): 
            number = randint(-9999, 9999)
            while -100 <= number <= 100: 
                number = randint(-9999, 9999)
            return number

        expression = ""

        if varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()}"

        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()})"

        return expression


    def display_expression(self):
        expression = ""

        if self.difficulty == "Easy": 
            expression = self.createEasy()
            time_limit = 10  # 10 seconds for Easy
        elif self.difficulty == "Medium": 
            expression = self.createMedium()
            time_limit = 15  # 15 seconds for Medium
        elif self.difficulty == "Hard": 
            expression = self.createHard()
            time_limit = 20  # 20 seconds for Hard
        else: 
            expression = self.createInsane()
            time_limit = 40  # 40 seconds for Insane

        start_time = time.time()

        # Initialize stars with random positions, sizes, and brightness
        num_stars = 50
        stars = [{'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'size': random.randint(10, 15),  # Bigger stars
                'brightness': random.randint(200, 255),
                'color': (255, 255, 0),
                'hovered': False,  # Track if hovered
                'burst': False,  # Flag for burst effect
                'burst_particles': []} for _ in range(num_stars)]  # To hold burst particles

        # Initialize the clock
        clock = pygame.time.Clock()

        while True:
            elapsed_time = time.time() - start_time

            # Draw semi-transparent rectangle for trails
            trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            trail_surface.fill((0, 0, 0, 20))  # Black with low alpha for fading effect
            SCREEN.blit(trail_surface, (0, 0))

            # Update and draw stars
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for star in stars:
                # If burst effect is active, create new particles
                if star['burst']:
                    # Create burst particles (smaller stars expanding and fading out)
                    for particle in star['burst_particles']:
                        particle['x'] += particle['vx']
                        particle['y'] += particle['vy']
                        particle['alpha'] -= 10  # Fade out the particles
                        pygame.draw.circle(SCREEN, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])
                        if particle['alpha'] <= 0:
                            star['burst_particles'].remove(particle)  # Remove faded particles
                    continue  # Skip drawing the original star

                # Check for interaction (hover over the star)
                if abs(star['x'] - mouse_x) < star['size'] and abs(star['y'] - mouse_y) < star['size']:
                    if not star['hovered']:  # Only change color once when hovering
                        # Change color of the star once
                        star['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                        star['hovered'] = True  # Mark as hovered

                    if pygame.mouse.get_pressed()[0]:  # Left click
                        # Trigger burst effect
                        star['burst'] = True
                        star['burst_particles'] = []  # Reset particles for this star
                        for _ in range(10):  # Create 10 burst particles
                            particle = {
                                'x': star['x'],
                                'y': star['y'],
                                'vx': random.randint(-3, 3),  # Random direction
                                'vy': random.randint(-3, 3),
                                'size': random.randint(1, 3),
                                'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),  # Random color
                                'alpha': 255  # Full opacity
                            }
                            star['burst_particles'].append(particle)

                else:
                    # If the mouse leaves the star, reset the hover flag
                    star['hovered'] = False

                # Draw the star (highlighting if hovered)
                pygame.draw.circle(SCREEN, star['color'], (star['x'], star['y']), star['size'])

                # Move star downward (adjust speed here)
                star['y'] += 2  # Slower speed
                if star['y'] > SCREEN_HEIGHT:
                    # Reset star to the top at a random position
                    star['y'] = 0
                    star['x'] = random.randint(0, SCREEN_WIDTH)
                    star['size'] = random.randint(5, 10)  # Larger size for stars
                    star['color'] = (255, 255, 0)  # Reset to yellow
                    star['burst'] = False  # Reset burst effect

            # Timer and text rendering
            timer = str(int(elapsed_time))  # Convert elapsed time to seconds
            title = HEADER_1.render("Solve the Expression", True, (255, 255, 255))  # White text
            expression_text = HEADER_2.render(expression, True, (255, 255, 255))  # White text
            timerText = FONT_BIG.render(timer, True, (255, 255, 255))  # White text

            # Place the timer on the top-left corner
            SCREEN.blit(timerText, (SCREEN_WIDTH * 0.02 - timerText.get_width() // 2, SCREEN_HEIGHT * 0.015))
            SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.1))
            SCREEN.blit(expression_text, (SCREEN_WIDTH // 2 - expression_text.get_width() // 2, SCREEN_HEIGHT * 0.52))

            pygame.display.update()

            # Check if the time limit has been reached based on difficulty
            if elapsed_time > time_limit:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Cap the frame rate (adjust here for smoothness)
            clock.tick(30)  # 30 FPS for a relaxed animation

        try:
            answer = eval(expression)
        except ZeroDivisionError:
            answer = "undefined (division by zero)"

        return answer


class Spot():
    def __init__(self, row, col, x, y, width, height):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        self.isFruit = False

    def reset(self, color, screen):
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.width, self.height))

def make_grid(row, col, dx, dy):
    grid = []
    y = 0

    for i in range(row): # first row is dedicated for score, it should not have a property
        temp = []
        x = 0
        for j in range(col):
            spot = Spot(i, j, x, y, dx, dy)
            temp.append(spot)
            x += dx
        y += dy
        grid.append(temp)

    return grid

def drawStats(screen, color, nums, time):
    spotHeight = SCREEN_HEIGHT // SQUARE_PER_ROW

    pygame.draw.rect(screen, color, pygame.Rect(0, 0, SCREEN_WIDTH, spotHeight))

    Number = FONT_BIG.render("".join(nums), True, GREEN)

    Time = FONT_BIG.render("Time : " + str(time), True, GREEN)

    screen.blit(Time, (0.02 * SCREEN_WIDTH, spotHeight * 0.25))
    screen.blit(Number, (0.42 * SCREEN_WIDTH, spotHeight * 0.25))
    #screen.blit(FruitsEaten, (0.75 * SCREEN_WIDTH, spotHeight * 0.25))

def check_visited(x, y, visited):
    return False if (x,y) in visited else True

def draw_game_over(screen, color, x, y):
    screen.fill(color)
    text = FONT_BIG.render("GAME OVER", True, BLACK)
    screen.blit(text, (x - 0.1 * SCREEN_WIDTH, y))

def draw_lines(row, col):
    dx = SCREEN_WIDTH // SQUARE_PER_COL
    dy = SCREEN_HEIGHT // SQUARE_PER_ROW

    y = 0
    for i in range(row):
        x = 0
        for j in range(col):
            # horizontal line
            pygame.draw.line(SCREEN, BLACK, (x, y), (SCREEN_WIDTH, y), width=2)
            # vertical line
            pygame.draw.line(SCREEN, BLACK, (x, y), (x, SCREEN_HEIGHT), width=2)

            x += dx
        y += dy

GRID = make_grid(SQUARE_PER_ROW, SQUARE_PER_COL, SPOT_WIDTH, SPOT_HEIGHT)

def you_win_screen():
    win_message = HEADER_1.render("You Win!", True, RED)
    restart_message = HEADER_1.render("Press R to Restart", True, BLACK)
    quit_message = HEADER_1.render("Press Q to Quit", True, BLACK)

    while True:
        SCREEN.fill(WHITE)  # Fill the screen with white background
        SCREEN.blit(win_message, (SCREEN_WIDTH // 2 - win_message.get_width() // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(quit_message, (SCREEN_WIDTH // 2 - quit_message.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Handle keypresses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                if event.key == pygame.K_r:  # Restart the game
                    return  

def you_lose_screen():
    lose_message = HEADER_1.render("You Lost!", True, RED)
    restart_message = HEADER_1.render("Press R to Restart", True, BLACK)
    quit_message = HEADER_1.render("Press Q to Quit", True, BLACK)

    while True:
        SCREEN.fill(WHITE)  # Fill the screen with white background
        SCREEN.blit(lose_message, (SCREEN_WIDTH // 2 - lose_message.get_width() // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(quit_message, (SCREEN_WIDTH // 2 - quit_message.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Handle keypresses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                if event.key == pygame.K_r:  # Restart the game
                    return  

class Snake():
    def __init__(self, width, height):
        self.row = random.randint(int(SQUARE_PER_ROW * 0.1), int(SQUARE_PER_ROW * 0.9))
        self.col = random.randint(int(SQUARE_PER_COL * 0.1), int(SQUARE_PER_COL * 0.9))
        self.width = width
        self.height = height
        self.color = BLUE
        self.body = deque([GRID[self.row][self.col]]) #  stores class spot
        self.visited = deque([(self.row, self.col)])
        self.collideWall = False

    def draw_head(self, color, screen):
        self.spot = GRID[self.row][self.col]
        pygame.draw.rect(screen, color, pygame.Rect(self.spot.x, self.spot.y, self.width, self.height))

    def draw_body(self, color, screen, arr):
        head = arr[0]
        # tail = arr[-1]
        #for spot in arr:
            #pygame.draw.rect(screen, color, pygame.Rect(spot.x, spot.y, spot.width, spot.height))

        pygame.draw.rect(screen, color, pygame.Rect(head.x, head.y, head.width, head.height))

    def eat_number(self, x, y):
        return True if (x, y) == (self.row, self.col) else False

    # paint previous tail placement as bg color
    def update_tail(self, screen, spot):
        pygame.draw.rect(screen, WHITE, pygame.Rect(spot.x, spot.y, spot.width, spot.height))

    def collisionWithSelf(self):
        count = 0
        #print((self.row, self.col), self.visited)
        for x, y in self.visited:
            if count >= 1 and (self.row, self.col) == (x, y): return True
            count += 1

        return False

    def move(self, color, screen, x, y):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]: # up
            if self.row - 1 >= 1:
                self.row -= 1

                # draw head, and cover previous head
                if not self.eat_number(x, y): # (x,y) is number coordinates
                    spot = self.body.pop()
                    self.visited.pop()
                    self.update_tail(screen, spot)

                self.draw_head(color, screen)

                # add new head
                self.body.appendleft(self.spot)
                self.visited.appendleft((self.row, self.col))

                # draw new body after new placement
                self.draw_body(BLUE, SCREEN, self.body)

            else:
                self.collideWall = True

        elif key[pygame.K_a]: # left
            if self.col - 1 >= 0:
                self.col -= 1

                # draw head, and cover previous head
                if not self.eat_number(x, y):  # (x,y) is apple coordinates
                    spot = self.body.pop()
                    self.visited.pop()
                    self.update_tail(screen, spot)

                self.draw_head(color, screen)

                # add new head
                self.body.appendleft(self.spot)
                self.visited.appendleft((self.row, self.col))

                # draw new body after new placement
                self.draw_body(BLUE, SCREEN, self.body)

            else:
                self.collideWall = True

        elif key[pygame.K_s]: # down
            if self.row + 1 <= SQUARE_PER_ROW-1:
                self.row += 1

                # draw head, and cover previous head
                if not self.eat_number(x, y):  # (x,y) is apple coordinates
                    spot = self.body.pop()
                    self.visited.pop()
                    self.update_tail(screen, spot)

                self.draw_head(color, screen)

                # add new head
                self.body.appendleft(self.spot)
                self.visited.appendleft((self.row, self.col))

                # draw new body after new placement
                self.draw_body(BLUE, SCREEN, self.body)

            else:
                self.collideWall = True

        elif key[pygame.K_d]: # right
            if self.col + 1 <= SQUARE_PER_COL-1:
                self.col += 1

                # draw head, and cover previous head
                if not self.eat_number(x, y):  # (x,y) is apple coordinates
                    spot = self.body.pop()
                    self.visited.pop()
                    self.update_tail(screen, spot)

                self.draw_head(color, screen)

                # add new head
                self.body.appendleft(self.spot)
                self.visited.appendleft((self.row, self.col))

                # draw new body after new placement
                self.draw_body(BLUE, SCREEN, self.body)

            else:
                self.collideWall = True

class Number():
    def __init__(self, width, height, number, font_size):
        self.number = number
        self.row = random.randint(1, SQUARE_PER_ROW-1)
        self.col = random.randint(1, SQUARE_PER_COL-1)
        self.width = width
        self.height = height
        self.font_size = font_size
        self.spot = GRID[self.row][self.col]

        self.font = pygame.font.Font("freesansbold.ttf", self.font_size)

    def get_number(self):
        return self.number

    def draw_Number(self, color, screen):
        text_surface = self.font.render(str(self.number), True, color)
        text_rect = text_surface.get_rect(center=(self.spot.x + self.width//2, self.spot.y + self.height//2))
        screen.blit(text_surface, text_rect)

    def collision(self, x, y):
        return True if (self.row, self.col) == (x, y) else False

    def createNewPos(self, visited):
        while True:
            #print(visited, self.row, self.col)
            self.row = random.randint(1, SQUARE_PER_ROW-1)
            self.col = random.randint(1, SQUARE_PER_COL-1)
            #print("new apple location : ", self.row, self.col)
            if (self.row, self.col) not in visited:
                break

        self.spot = GRID[self.row][self.col]

class Zero(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

class One(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

class Two(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)
    
class Three(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)
    
class Four(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

class Five(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)
    
class Six(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

class Seven(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

class Eight(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

class Nine(Number):
    def createNewNumber(self, color, screen, visited):
        self.spot.reset(color, screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)

def main():
    run = True
    time = 0
    foundDifficulty = True
    difficulty = get_difficulty()

    # Create a QuestionWindow instance and display the expression
    question_window = QuestionWindow(difficulty)
    answer = question_window.display_expression()

    snake = Snake(SPOT_WIDTH, SPOT_HEIGHT)
    SCREEN.fill(WHITE)

    zero = Zero(SPOT_WIDTH, SPOT_HEIGHT, "0", SPOT_WIDTH)
    one = One(SPOT_WIDTH, SPOT_HEIGHT, "1", SPOT_WIDTH)
    two = Two(SPOT_WIDTH, SPOT_HEIGHT, "2", SPOT_WIDTH)
    three = Three(SPOT_WIDTH, SPOT_HEIGHT, "3", SPOT_WIDTH)
    four = Four(SPOT_WIDTH, SPOT_HEIGHT, "4", SPOT_WIDTH)
    five = Five(SPOT_WIDTH, SPOT_HEIGHT, "5", SPOT_WIDTH)
    six = Six(SPOT_WIDTH, SPOT_HEIGHT, "6", SPOT_WIDTH)
    seven = Seven(SPOT_WIDTH, SPOT_HEIGHT, "7", SPOT_WIDTH)
    eight = Eight(SPOT_WIDTH, SPOT_HEIGHT, "8", SPOT_WIDTH)
    nine = Nine(SPOT_WIDTH, SPOT_HEIGHT, "9", SPOT_WIDTH)

    nums = [zero, one, two, three, four, five, six, seven, eight, nine]
    arr = []
    idx = 0

    isNegative = False
    ansLen = len(str(answer))
    if str(answer)[idx] == "-": 
        idx += 1
        ansLen -= 1
        isNegative = True
    currentNumToFind = nums[int(str(answer)[idx])]

    game_over = False
    print(answer)

    while run:
        time += 1

        if not foundDifficulty:
            time = 0
            foundDifficulty = True
            difficulty = get_difficulty()

            # Create a QuestionWindow instance and display the expression
            question_window = QuestionWindow(difficulty)
            answer = question_window.display_expression()

            snake = Snake(SPOT_WIDTH, SPOT_HEIGHT)
            SCREEN.fill(WHITE)

            zero = Zero(SPOT_WIDTH, SPOT_HEIGHT, "0", SPOT_WIDTH)
            one = One(SPOT_WIDTH, SPOT_HEIGHT, "1", SPOT_WIDTH)
            two = Two(SPOT_WIDTH, SPOT_HEIGHT, "2", SPOT_WIDTH)
            three = Three(SPOT_WIDTH, SPOT_HEIGHT, "3", SPOT_WIDTH)
            four = Four(SPOT_WIDTH, SPOT_HEIGHT, "4", SPOT_WIDTH)
            five = Five(SPOT_WIDTH, SPOT_HEIGHT, "5", SPOT_WIDTH)
            six = Six(SPOT_WIDTH, SPOT_HEIGHT, "6", SPOT_WIDTH)
            seven = Seven(SPOT_WIDTH, SPOT_HEIGHT, "7", SPOT_WIDTH)
            eight = Eight(SPOT_WIDTH, SPOT_HEIGHT, "8", SPOT_WIDTH)
            nine = Nine(SPOT_WIDTH, SPOT_HEIGHT, "9", SPOT_WIDTH)

            nums = [zero, one, two, three, four, five, six, seven, eight, nine]
            arr = []
            idx = 0

            isNegative = False
            ansLen = len(str(answer))
            if str(answer)[idx] == "-": 
                idx += 1
                ansLen -= 1
                isNegative = True
            currentNumToFind = nums[int(str(answer)[idx])]

            game_over = False
            # print(answer)

        clock.tick(FPS)

        drawStats(SCREEN, BLACK, arr, time)
        
        print("number to find: ", currentNumToFind.number, str(answer)[idx], idx, ansLen)
        # snake movement
        snake.move(BLUE, SCREEN, currentNumToFind.row, currentNumToFind.col)

        # print(snake.body)
        if not game_over:
            for i in range(len(nums)):
                nums[i].draw_Number(BLACK, SCREEN)

                if nums[i].collision(snake.row, snake.col):
                    nums[i].createNewNumber(WHITE, SCREEN, snake.visited)
                    arr.append(str(nums[i].number))  # Store as string to join later
                    if idx < ansLen:
                        if int(nums[i].number) == int(str(answer)[idx]):
                            # print(nums[i].number)
                            # print(int(str(answer)[idx]))
                            # print("xxxxxxxxxxxxxxxxxxxxxxxx")
                            idx += 1
                            if idx < ansLen:
                                currentNumToFind = nums[int(str(answer)[idx])]
                        else:
                            # print(type(nums[i].number))
                            # print(type(int(str(answer)[idx])))
                            # print("xxxxxxxxxxxxxxxxxxxxxxxx")
                            game_over = True

                    if len(arr) == ansLen:
                        # Concatenate numbers and check the answer
                        final_ans = int("-" + "".join(arr)) if isNegative else int("".join(arr))
                        if final_ans == int(answer):
                            you_win_screen()
                            foundDifficulty = False

                        else:
                            you_lose_screen()  # Call the function with ()
                            foundDifficulty = False
                            
        # draw lines
        draw_lines(SQUARE_PER_ROW, SQUARE_PER_COL)

        # game over for snake
        if snake.collisionWithSelf() or snake.collideWall:
            game_over = True
            snake = Snake(SPOT_WIDTH, SPOT_HEIGHT)

        if game_over:
            you_lose_screen()  # Call the function with ()
            foundDifficulty = False

        # snake drawing
        snake.draw_head(BLUE, SCREEN)

        # snake velocity
        pygame.time.delay(snake_speed)

        # update window
        pygame.display.update()

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    run = False

if __name__ == "__main__":
    main()
    pygame.quit()
