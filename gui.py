#!../bin/python

import sys
import pygame
import ast
import queue


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)

    def update_text(self, new_text):
        self.text_input = new_text
        self.text = self.font.render(self.text_input, True, self.base_color)


class ButtonB():
    def __init__(self, image, hover_image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.hover_image = hover_image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen, is_hovering):
        # Use hover image if mouse is over the button
        if is_hovering:
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        self.text = self.font.render(
            self.text_input, True, self.hovering_color if self.rect.collidepoint(position) else self.base_color)


class Text:
    """Centered Text Class"""
    # Constructror

    def __init__(self, text, x, y, color=(0, 0, 0)):
        self.x = x  # Horizontal center of box
        self.y = y  # Vertical center of box
        # Start PyGame Font
        pygame.font.init()
        font = pygame.font.SysFont("sans", 12)
        self.txt = font.render(text, True, color)
        self.size = font.size(text)  # (width, height)
    # Draw Method

    def Draw(self, screen):
        drawX = self.x - (self.size[0] / 2.)
        drawY = self.y - (self.size[1] / 2.)
        coords = (drawX, drawY)
        screen.blit(self.txt, coords)


class GAME:

    def is_valid_value(self, char):
        if (char == ' ' or  # floor
            char == '#' or  # wall
            char == '@' or  # worker on floor
            char == '.' or  # dock
            char == '*' or  # box on dock
            char == '$' or  # box
                char == '+'):  # worker on dock
            return True
        else:
            return False

    def __init__(self, level):
        self.matrix = []
        if level is None:
            print("ERROR input file")
            sys.exit(1)
        else:
            try:
                # Try to open the file
                with open(level, 'r') as file:
                    next(file)  # Skip the first line

                    for line in file:
                        row = []
                        if line.strip() != "":
                            for c in line:
                                if c != '\n' and self.is_valid_value(c):
                                    row.append(c)
                                elif c == '\n':  # Jump to next row on newline
                                    continue
                                else:
                                    print("ERROR: Level " + str(level) +
                                          " has invalid value " + c)
                                    sys.exit(1)
                            self.matrix.append(row)
                        else:
                            break

            except FileNotFoundError:
                print("Error: File not found. Please check the filename and path.")
                sys.exit(1)  # Exit the program if the file doesn't exist

            except PermissionError:
                print("Error: You don't have permission to access this file.")
                sys.exit(1)  # Exit the program if there are permission issues

            except OSError as e:
                print(f"Error: An unexpected error occurred - {e}")
                sys.exit(1)  # Exit for any other I/O-related errors

    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self, x, y):
        return self.matrix[y][x]

    def set_content(self, x, y, content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print("ERROR: Value '"+content+"' to be added is not valid")

    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self, x, y):
        return self.get_content(self.worker()[0]+x, self.worker()[1]+y) not in ['#', '*', '$']

    def next(self, x, y):
        return self.get_content(self.worker()[0]+x, self.worker()[1]+y)

    def can_push(self, x, y):
        return (self.next(x, y) in ['*', '$'] and self.next(x+x, y+y) in [' ', '.'])

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True

    def move_box(self, x, y, a, b):
        #        (x,y) -> move to do
        #        (a,b) -> box to move
        current_box = self.get_content(x, y)
        future_box = self.get_content(x+a, y+b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x+a, y+b, '$')
            self.set_content(x, y, ' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x+a, y+b, '*')
            self.set_content(x, y, ' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a, y+b, '$')
            self.set_content(x, y, '.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x+a, y+b, '*')
            self.set_content(x, y, '.')

    def move(self, x, y):
        if self.can_move(x, y):
            current = self.worker()
            future = self.next(x, y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0]+x, current[1]+y, '@')
                self.set_content(current[0], current[1], ' ')
            elif current[2] == '@' and future == '.':
                self.set_content(current[0]+x, current[1]+y, '+')
                self.set_content(current[0], current[1], ' ')
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0]+x, current[1]+y, '@')
                self.set_content(current[0], current[1], '.')
            elif current[2] == '+' and future == '.':
                self.set_content(current[0]+x, current[1]+y, '+')
                self.set_content(current[0], current[1], '.')

        elif self.can_push(x, y):
            current = self.worker()
            future = self.next(x, y)
            future_box = self.next(x+x, y+y)
            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0]+x, current[1]+y, '@')
            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0]+x, current[1]+y, '@')
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0]+x, current[1]+y, '+')
            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0]+x, current[1]+y, '+')
            if current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0]+x, current[1]+y, '@')
            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0]+x, current[1]+y, '+')
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0]+x, current[1]+y, '+')
            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0]+x, current[1]+y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0]+x, current[1]+y, '+')


def print_game(matrix, screen, level):
    q = queue.Queue()
    # Open the file in read mode
    with open('input' + '/' + level, 'r') as file:
        # Read the first line, strip whitespace, and split by spaces
        numbers = file.readline().strip().split()

        # Add each number to the queue (converted to int if needed)
        for num in numbers:
            q.put(num)  # Convert to integer if you want to work with numbers
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == ' ':  # floor
                screen.blit(floor, (x, y))
            elif char == '#':  # wall
                screen.blit(wall, (x, y))
            elif char == '@':  # worker on floor
                screen.blit(worker, (x, y))
            elif char == '.':  # dock
                screen.blit(docker, (x, y))
            elif char == '*':  # box on dock
                screen.blit(box_docked, (x, y))
                if not q.empty():  # Check if queue is not empty before popping
                    weight_value = q.get()  # Pop an element from the queue
                    # Create a text instance with the weight value
                    text = Text(weight_value, x + 16, y + 16)
                    text.Draw(screen)  # Draw the text on the screen
            elif char == '$':  # box
                screen.blit(box, (x, y))
                text = Text(q.get(), x+16, y+16)
                text.Draw(screen)
            elif char == '+':  # worker on dock
                screen.blit(worker_docked, (x, y))
            x = x + 32
        x = 0
        y = y + 32


def display_end(screen, pos):
    """Display a completion message at a specified position on the screen."""
    message = "Level Completed"
    fontobject = pygame.font.Font(None, 25)

    # Unpack the position tuple
    box_x, box_y = pos  # pos is expected to be a tuple (x, y)

    # Get the size of the rendered message
    message_surface = fontobject.render(message, True, (255, 255, 255))
    message_width, message_height = message_surface.get_size()

    # Define the dimensions of the box
    box_width = 200
    box_height = 40  # Increased height for better padding

    # Draw the black box
    pygame.draw.rect(screen, (0, 0, 0),
                     (box_x, box_y, box_width, box_height), 0)
    # Draw the white border
    pygame.draw.rect(screen, (255, 255, 255),
                     (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 1)

    # Calculate the position to center the message in the box
    text_x = box_x + (box_width - message_width) // 2
    text_y = box_y + (box_height - message_height) // 2

    # Blit the message onto the screen at the calculated position
    screen.blit(message_surface, (text_x, text_y))
    pygame.display.flip()


def solution(filename, search_type):
    # Mapping of types to line numbers
    line_map = {
        'bfs': (3, 4),
        'dfs': (7, 8),
        'ucs': (11, 12),
        'astar': (15, 16)
    }

    # Get the line numbers for the given type
    line_numbers = line_map.get(search_type.lower())

    if not line_numbers:
        return None, None  # Return None for both if the search type is not valid

    # Open the file and read the specific lines
    with open('output-gui/' + filename, 'r') as file:
        move_string = None
        weights = None
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_numbers[0]:
                move_string = line.strip()  # Assign line 3 (or its equivalent)
            elif current_line_number == line_numbers[1]:
                weights = line.strip()  # Assign line 4 (or its equivalent)

    # Convert the weights string to a list if it's not None
    if weights is not None:
        # Convert string representation to a list
        weights = ast.literal_eval(weights)

    return move_string, weights  # Return both values


wall = pygame.image.load('images/wall.png')
floor = pygame.image.load('images/floor.png')
box = pygame.image.load('images/rock.png')
box_docked = pygame.image.load('images/rock_docked.png')
worker = pygame.image.load('images/character.png')
worker_docked = pygame.image.load('images/character.png')
docker = pygame.image.load('images/dock.png')
background = 255, 226, 191
