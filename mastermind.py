import random
import time

import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREY = (220, 220, 220)

# Define constants
WIDTH, HEIGHT = 800, 600
SLOT_SIZE = 40
SLOTS_X = 4
SLOTS_Y = 8
ROUNDS = 8
SLOT_MARGIN = 10
FEEDBACK_BUTTON_RECT = pygame.Rect(650, 450, 100, 40)
RESTART_BUTTON_RECT = pygame.Rect(150, 450, 100, 40)
CHECKBOX_SIZE = 20

# FIRST_SLOT_TOP = (HEIGHT - (SLOTS_Y * SLOT_SIZE + (SLOTS_Y + 13) * SLOT_MARGIN)) / 2
FIRST_SLOT_TOP = 40
FIRST_SLOT_LEFT = (WIDTH - (SLOTS_X * SLOT_SIZE + SLOTS_X * SLOT_MARGIN)) / 2

# List of available colors
COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

# Initialize the list to store color buttons
color_buttons = []

# The list, which contains the colors which need to guess
secret_code = []

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")


# Function to draw a checkbox
def draw_checkbox(x, y, checked):
    pygame.draw.rect(screen, WHITE, (x, y, CHECKBOX_SIZE, CHECKBOX_SIZE))
    pygame.draw.rect(screen, BLACK, (x, y, CHECKBOX_SIZE, CHECKBOX_SIZE), 2)
    if checked:
        pygame.draw.line(screen, BLACK, (x, y), (x + CHECKBOX_SIZE, y + CHECKBOX_SIZE), 2)
        pygame.draw.line(screen, BLACK, (x, y + CHECKBOX_SIZE), (x + CHECKBOX_SIZE, y), 2)
    font = pygame.font.Font(None, 30)
    text = font.render('Color duplication is allowed', True, BLACK)
    screen.blit(text, (x + CHECKBOX_SIZE + 10, y + 2))


# Function to draw the start button
def draw_start_button(x, y):
    font = pygame.font.Font(None, 30)
    text = font.render('Start', True, BLACK)
    pygame.draw.rect(screen, WHITE, (x, y, text.get_width() + 20, text.get_height() + 10))
    pygame.draw.rect(screen, BLACK, (x, y, text.get_width() + 20, text.get_height() + 10), 2)
    screen.blit(text, (x + 10, y + 5))


# Function to calculate the feedback
def calculate_feedback(guess):
    # Check the guess and provide feedback
    secret_colors = secret_code[:]
    correct_positions = 0
    correct_colors = 0

    # sign that the 'i' COLOR take into account for correct positions
    correct_position_index = []
    # Calculate correct positions
    for i in range(SLOTS_X):
        if guess[i] == secret_colors[i]:
            correct_positions += 1
            secret_colors[i] = None
            correct_position_index.append(i)

    # Calculate correct colors in wrong positions
    for i in range(SLOTS_X):
        if guess[i] in secret_colors and i not in correct_position_index:
            correct_colors += 1
            secret_colors[secret_colors.index(guess[i])] = None

    return [correct_positions, correct_colors]


def draw_feedback(correct, rounds_left):
    circle_radius = 8
    circle_spacing = 20
    x = FEEDBACK_BUTTON_RECT.x - 120
    y = FIRST_SLOT_TOP + (ROUNDS - rounds_left) * (SLOT_SIZE + SLOT_MARGIN) + 15
    for _ in range(correct[0]):
        pygame.draw.circle(screen, BLACK, (x, y), circle_radius)
        x += circle_spacing
    for _ in range(correct[1]):
        pygame.draw.circle(screen, WHITE, (x, y), circle_radius)
        x += circle_spacing
    x = FEEDBACK_BUTTON_RECT.x - 120
    for _ in range(4):
        pygame.draw.circle(screen, BLACK, (x, y), circle_radius, 1)
        x += circle_spacing


# Generate random code for the game
def generate_random_codes():
    tmp_secret_code = [random.choice(COLORS) for _ in range(SLOTS_X)]
    for color in tmp_secret_code:
        secret_code.append(color)


# Generate random code for the game without color duplication
def generate_random_codes_without_duplication():
    tmp_secret_code = random.sample(COLORS, SLOTS_X)
    for color in tmp_secret_code:
        secret_code.append(color)


# Initialize color buttons
def init_color_buttons():
    for i, color in enumerate(COLORS):
        button_rect = pygame.Rect(
            (WIDTH - 100, i * 50 + 20),
            (50, 40))
        color_buttons.append(button_rect)


# Function to draw the color buttons
def draw_color_buttons():
    for i, color in enumerate(COLORS):
        button_rect = pygame.Rect(
            (WIDTH - 100, i * 50 + 20),
            (50, 40))
        pygame.draw.rect(screen, color, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)


# Function to check if a slot is empty
def is_slot_empty(slots, row, col):
    return slots[row][col] is None


# Function to find the first empty slot in a row
def find_first_empty_slot(slots, row):
    for col in range(SLOTS_X):
        if is_slot_empty(slots, row, col):
            return col
    return -1


# Function to draw the placed colors in the slots
def draw_placed_colors(slots):
    for row in range(ROUNDS):
        for col in range(SLOTS_X):
            if slots[row][col] is not None:
                color = slots[row][col]
                color_circle_center = (
                    col * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_LEFT + SLOT_SIZE // 2,
                    row * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_TOP + SLOT_SIZE // 2
                )
                pygame.draw.circle(screen, color, color_circle_center, SLOT_SIZE // 2)
            else:
                # draw the grey slot
                slot_rect = pygame.Rect(
                    (
                        col * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_LEFT,
                        row * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_TOP),
                    (SLOT_SIZE, SLOT_SIZE))
                pygame.draw.rect(screen, GREY, slot_rect)
                # draw the black border
                slot_rect = pygame.Rect(
                    (
                        col * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_LEFT,
                        row * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_TOP),
                    (SLOT_SIZE, SLOT_SIZE))
                pygame.draw.rect(screen, BLACK, slot_rect, 2)


def draw_feedback_button(rounds_left):
    pygame.draw.rect(screen, GREEN if rounds_left == 0 else RED, FEEDBACK_BUTTON_RECT)
    font = pygame.font.Font(None, 30)
    text = font.render("Check", True, WHITE)
    screen.blit(text, (FEEDBACK_BUTTON_RECT.x + 20, FEEDBACK_BUTTON_RECT.y + 10))


def draw_restart_button():
    pygame.draw.rect(screen, BLACK, RESTART_BUTTON_RECT)
    font = pygame.font.Font(None, 30)
    text = font.render("Restart", True, WHITE)
    screen.blit(text, (RESTART_BUTTON_RECT.x + 15, RESTART_BUTTON_RECT.y + 10))


def fill_slots_with_clicked_color(slots, rounds_left, event):
    for i, color_rect in enumerate(color_buttons):
        if color_rect.collidepoint(event.pos):
            # Find the first empty slot in the current row and fill it with the selected color
            row = ROUNDS - rounds_left
            col = find_first_empty_slot(slots, row)
            if col != -1:
                slots[row][col] = COLORS[i]
                return True
    return False


# Function to draw the secret colors at the end of the game
def draw_secret_colors():
    for i in range(len(secret_code)):
        color_circle_center = (
            i * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_LEFT + SLOT_SIZE // 2,
            ROUNDS * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_TOP + SLOT_SIZE // 2
        )
        pygame.draw.circle(screen, secret_code[i], color_circle_center, SLOT_SIZE // 2)


# Function to find the slot index based on the mouse position
def find_slot_index(x, y, row):
    for col in range(SLOTS_X):
        slot_rect = pygame.Rect(
            (col * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_LEFT,
             row * (SLOT_SIZE + SLOT_MARGIN) + FIRST_SLOT_TOP),
            (SLOT_SIZE, SLOT_SIZE)
        )
        if slot_rect.collidepoint(x, y):
            return col
    return -1


# Initialize setting page
# Settings
def settings():
    running = True
    checkbox_checked = False
    # Clear the screen
    screen.fill(GREY)
    # Draw the checkbox and button
    draw_checkbox(100, 100, checkbox_checked)
    draw_start_button(150, 150)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= event.pos[0] <= 100 + CHECKBOX_SIZE and 100 <= event.pos[1] <= 100 + CHECKBOX_SIZE:
                    checkbox_checked = not checkbox_checked
                    draw_checkbox(100, 100, checkbox_checked)
                elif 150 <= event.pos[0] <= 250 and 150 <= event.pos[1] <= 180:
                    if game_loop(checkbox_checked):
                        return True

        # Update the screen
        pygame.display.flip()
        time.sleep(0.05)


# Main game loop
def game_loop(with_duplication):
    global ROUNDS
    global SLOTS_Y
    global secret_code
    secret_code = []
    if with_duplication:
        generate_random_codes()
        ROUNDS = 8
        SLOTS_Y = 8
    else:
        generate_random_codes_without_duplication()
        ROUNDS = 6
        SLOTS_Y = 6
    slots = [[None for _ in range(SLOTS_X)] for _ in range(SLOTS_Y)]
    rounds_left = ROUNDS

    init_color_buttons()

    screen.fill(GREY)

    running = True

    # Draw placed colors in the slots
    draw_placed_colors(slots)

    # Draw color selection buttons
    draw_color_buttons()

    # Draw buttons
    draw_feedback_button(rounds_left)
    draw_restart_button()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if FEEDBACK_BUTTON_RECT.collidepoint(event.pos) and rounds_left > 0:
                    draw_feedback(calculate_feedback(slots[ROUNDS - rounds_left]), rounds_left)
                    rounds_left -= 1
                    # Check if the game has ended
                    if rounds_left == 0:
                        draw_secret_colors()
                elif RESTART_BUTTON_RECT.collidepoint(event.pos):
                    return True
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                      and fill_slots_with_clicked_color(slots, rounds_left, event)):
                    draw_placed_colors(slots)
                else:
                    x, y = event.pos
                    slot_index = find_slot_index(x, y, ROUNDS - rounds_left)
                    if slot_index != -1 and ROUNDS - rounds_left >= 0:
                        slots[ROUNDS - rounds_left][slot_index] = None
                        draw_placed_colors(slots)

        # Update the display
        pygame.display.update()
        # do not need to loop too quickly
        time.sleep(0.05)

    pygame.quit()


if __name__ == "__main__":
    while settings():
        print('restarted')
