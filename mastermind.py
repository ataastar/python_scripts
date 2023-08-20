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
FIRST_SLOT_LEFT = (WIDTH - (SLOTS_X * SLOT_SIZE + SLOTS_X * SLOT_MARGIN)) // 2

# List of available colors
COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

# Initialize the list to store color buttons
color_buttons = []

# The list, which contains the colors which need to guess
secret_code = []

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")

# for drag&drop
# the dragged color index
dragged_color_index = -1
# the dragged color position before the mouse button is released
dragged_position = []

# settings variables
color_duplication_enabled = False

# stores the feedbacks
feedbacks = []

# stores the possibilities
all_possibilities = []


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


# Calculate and stores the feedback
def store_feedback(guess):
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
    feedbacks.append([correct_positions, correct_colors])


# Draws the current feedback
def draw_feedback(row_index):
    correct = feedbacks[row_index]
    circle_radius = 8
    circle_spacing = 20
    x = FEEDBACK_BUTTON_RECT.x - 120
    y = FIRST_SLOT_TOP + row_index * (SLOT_SIZE + SLOT_MARGIN) + 15
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


# Check that one of the color is clicked.
# returns the color index
def color_is_clicked(event):
    for i, color_rect in enumerate(color_buttons):
        if color_rect.collidepoint(event.pos):
            return i
    return -1


# Place the selected color
def place_color(slots, rounds_left, index_of_the_color, index_of_the_slot=-1):
    # Find the first empty slot in the current row and fill it with the selected color
    row = ROUNDS - rounds_left
    # if duplication is not allowed, then check that the row of the slot contains the selected color
    global color_duplication_enabled
    if not color_duplication_enabled:
        color = COLORS[index_of_the_color]
        for col in range(SLOTS_X):
            if slots[row][col] == color:
                return
    if index_of_the_slot == -1:
        index_of_the_slot = find_first_empty_slot(slots, row)
    if index_of_the_slot != -1:
        slots[row][index_of_the_slot] = COLORS[index_of_the_color]


# handle drag&drop and simple mouse click
def handle_mouse_button_up(event, slots, rounds_left):
    global dragged_color_index
    global dragged_position
    # when the color is dragged and the mouse button is released
    if len(dragged_position) > 0:
        # Find the row and slot index for the drop position
        row = (dragged_position[1] - FIRST_SLOT_TOP) // (SLOT_SIZE + SLOT_MARGIN)
        col = (dragged_position[0] - FIRST_SLOT_LEFT) // (SLOT_SIZE + SLOT_MARGIN)
        if row == (ROUNDS - rounds_left) and 0 <= col < SLOTS_X:
            # Place the dragged color into the slot index, define by the mouse position
            place_color(slots, rounds_left, dragged_color_index, col)
        else:
            # place the color just if the current mouse position is on the previously clicked color
            color_index = color_is_clicked(event)
            if color_index == dragged_color_index:
                place_color(slots, rounds_left, dragged_color_index)
    else:
        place_color(slots, rounds_left, dragged_color_index)
    draw_placed_colors(slots)
    dragged_color_index = -1
    dragged_position = []


# Removes the color from the slots, if the user click on the slots
def remove_color(event, slots, rounds_left):
    # check that the slots are clicked. In this case need to remove the color if it is placed
    x, y = event.pos
    slot_index = find_slot_index(x, y, ROUNDS - rounds_left)
    if slot_index != -1 and ROUNDS - rounds_left >= 0:
        slots[ROUNDS - rounds_left][slot_index] = None
        draw_placed_colors(slots)


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


# fill all possibilities
def fill_all_possibilities(current_possibility, remaining_colors):
    if not remaining_colors:
        current_possibility = []
        for color in COLORS:
            remaining_colors.append(color)
    temp_remaining_colors = remaining_colors[:]
    for color in remaining_colors:
        current_possibility.append(color)
        if len(current_possibility) == SLOTS_X:
            all_possibilities.append(current_possibility[:])
            current_possibility.pop()
        else:
            temp_remaining_colors.remove(color)
            fill_all_possibilities(current_possibility[:], temp_remaining_colors)
            current_possibility.pop()
            temp_remaining_colors.append(color)


# Calculate probability for the current slot row
def calculate_probability(row_index):
    if row_index == 0:
        probability = 1
        for possible_color_number in range(len(COLORS), len(COLORS) - SLOTS_X + 1):
            probability *= possible_color_number
    # else
    #    for


# Initialize setting page
# Settings
def settings():
    running = True
    global color_duplication_enabled
    # Clear the screen
    screen.fill(GREY)
    # Draw the checkbox and button
    draw_checkbox(100, 100, color_duplication_enabled)
    draw_start_button(150, 150)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= event.pos[0] <= 100 + CHECKBOX_SIZE and 100 <= event.pos[1] <= 100 + CHECKBOX_SIZE:
                    color_duplication_enabled = not color_duplication_enabled
                    draw_checkbox(100, 100, color_duplication_enabled)
                elif 150 <= event.pos[0] <= 250 and 150 <= event.pos[1] <= 180:
                    if game_loop():
                        return True
                    else:
                        return False
        # Update the screen
        pygame.display.flip()
        time.sleep(0.05)


# Main game loop
def game_loop():
    global ROUNDS
    global SLOTS_Y
    global secret_code
    global dragged_color_index
    global dragged_position
    global color_duplication_enabled
    global feedbacks
    secret_code = []
    # handle color duplication
    if color_duplication_enabled:
        generate_random_codes()
        ROUNDS = 8
        SLOTS_Y = 8
    else:
        generate_random_codes_without_duplication()
        ROUNDS = 6
        SLOTS_Y = 6
    slots = [[None for _ in range(SLOTS_X)] for _ in range(SLOTS_Y)]
    rounds_left = ROUNDS

    feedbacks = []

    init_color_buttons()

    screen.fill(GREY)

    running = True

    # Fill all possibilities
    global all_possibilities
    all_possibilities = []
    fill_all_possibilities([], [])

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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # check that the feedback button is clicked
                if FEEDBACK_BUTTON_RECT.collidepoint(event.pos) and rounds_left > 0:
                    store_feedback(slots[ROUNDS - rounds_left])
                    draw_feedback(ROUNDS - rounds_left)
                    rounds_left -= 1
                    # Check if the game has ended
                    if rounds_left == 0:
                        draw_secret_colors()
                # check that the restart button is clicked
                elif RESTART_BUTTON_RECT.collidepoint(event.pos):
                    return True
                else:
                    # check that the color buttons are clicked
                    color_index = color_is_clicked(event)
                    if color_index > -1:
                        dragged_color_index = color_index
                    else:
                        # check that the slots are clicked. In this case need to remove the color if it is placed
                        remove_color(event, slots, rounds_left)
            # check that the mouse is dragged
            elif event.type == pygame.MOUSEMOTION and dragged_color_index > -1:
                dragged_position = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                # when the color is clicked before (drag or simple click)
                if dragged_color_index > -1:
                    handle_mouse_button_up(event, slots, rounds_left)
        # Update the display
        pygame.display.update()
        # do not need to loop too quickly
        time.sleep(0.05)

    pygame.quit()


if __name__ == "__main__":
    while settings():
        print('restarted')
