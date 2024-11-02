import pygame, sys
import sokoban
from sokoban import Button, ButtonB

pygame.init()



SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    SCREEN = pygame.display.set_mode((1280, 720))

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        CHOOSE_TEXT = get_font(55).render("Choose the input case:", True, "WHITE")
        CHOOSE_RECT = CHOOSE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(CHOOSE_TEXT, CHOOSE_RECT)

        # Button dimensions and spacing
        button_width, button_height = 200, 100
        spacing_x, spacing_y = 20, 20

        # Starting position for the grid
        start_x, start_y = 200, 300

        # Create 10 buttons arranged in a grid
        testinput = []
        for i in range(10):
            row = i // 5   # Determines the row (0 or 1)
            col = i % 5    # Determines the column (0 to 4)
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)

            # Create each button with a unique label
            button = Button(
                image=None,
                pos=(x, y),
                text_input=f"{i + 1}",  # Labels 1 to 10
                font=get_font(45),
                base_color="White",
                hovering_color="Green"
            )
            testinput.append(button)

        # PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        # PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        # SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        for I in testinput:
            I.changeColor(PLAY_MOUSE_POS)
            I.update(SCREEN)


        PLAY_BACK = Button(image=None, pos=(1000, 650), text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                # Loop through each test input button and check for input
                for i in range(10):
                    if testinput[i].checkForInput(PLAY_MOUSE_POS):
                        # Format the filename as "input-01.txt" to "input-10.txt"
                        input_filename = f"input-{i+1:02}.txt"
                        gameplay(input_filename)
                        
        pygame.display.update()

def reset_game(level):
    global bfs_clicked, dfs_clicked, ucs_clicked, astar_clicked, is_moving, current_move_index, move_timer
    # Reset algorithm clicks
    bfs_clicked = False
    dfs_clicked = False
    ucs_clicked = False
    astar_clicked = False
    # Reset movement variables
    is_moving = False
    current_move_index = 0
    move_timer = 0
    # Reload the game level
    game = sokoban.GAME('input/' + level)
    # Additional resets if necessary, e.g., score, timer, etc.
    return game  # Return the new game instance
    
def gameplay(level):
    bfs_clicked = False
    dfs_clicked = False
    ucs_clicked = False
    astar_clicked = False
    is_start = True
    outputfile = "output-gui" + level[5:]
    game = sokoban.GAME('input/' + level)
    size = game.load_size()
    SCREEN = pygame.display.set_mode((size[0] + 240, size[1] + 100))
    SCREEN.fill(0)
    clock = pygame.time.Clock()

    movement_string = ""
    current_move_index = 0
    move_timer = 0
    move_interval = 300
    is_moving = False
    step = 0
    weight = "0"  # Start weight as "0"
    weights = []
    cost = 0
    game_completed = False  # Flag to track game completion

    # Load images
    start_image = pygame.transform.scale(pygame.image.load("assets/start.png"), (64, 64))
    start_hover_image = pygame.transform.scale(pygame.image.load("assets/start_hover.png"), (64, 64))
    pause_image = pygame.transform.scale(pygame.image.load("assets/pause.png"), (64, 64))
    pause_hover_image = pygame.transform.scale(pygame.image.load("assets/pause_hover.png"), (64, 64))
    reset_image = pygame.transform.scale(pygame.image.load("assets/reset.png"), (64, 64))
    reset_hover_image = pygame.transform.scale(pygame.image.load("assets/reset_hover.png"), (64, 64))

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BACK = Button(image=None, pos=(130, size[1] + 50), text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        BFS_BUTTON = ButtonB(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                             hover_image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                             pos=(size[0] + 70, 35), text_input="BFS", font=get_font(25), base_color="Green" if bfs_clicked else "#d7fcd4", hovering_color="White")
        DFS_BUTTON = ButtonB(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                             hover_image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                             pos=(size[0] + 175, 35), text_input="DFS", font=get_font(25), base_color="Green" if dfs_clicked else "#d7fcd4", hovering_color="White")
        UCS_BUTTON = ButtonB(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                             hover_image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                             pos=(size[0] + 70, 90), text_input="UCS", font=get_font(25), base_color="Green" if ucs_clicked else "#d7fcd4", hovering_color="White")
        ASTAR_BUTTON = ButtonB(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                               hover_image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (100, 50)),
                               pos=(size[0] + 175, 90), text_input="A*", font=get_font(25), base_color="Green" if astar_clicked else "#d7fcd4", hovering_color="White")

        current_image = start_image if is_start else pause_image
        current_hover_image = start_hover_image if is_start else pause_hover_image
        START_PAUSE_BUTTON = ButtonB(image=current_image, hover_image=current_hover_image, pos=(size[0] + 70, 170), text_input="", font=get_font(25), base_color="Green", hovering_color="White")

        RESET_BUTTON = ButtonB(image=reset_image, hover_image=reset_hover_image, pos=(size[0] + 170, 170), text_input="", font=get_font(25), base_color="Green", hovering_color="White")

        STEP_BUTTON = Button(image=pygame.Surface((120, 30)), pos=(size[0] + 70, 230),
                             text_input=f"Step: {step}", font=get_font(14),
                             base_color="White", hovering_color="White")
        STEP_BUTTON.image.fill("Black")

        WEIGHT_BUTTON = Button(image=pygame.Surface((140, 30)), pos=(size[0] + 80, 270),
                               text_input=f"Weight: {weight}", font=get_font(14),
                               base_color="White", hovering_color="White")
        WEIGHT_BUTTON.image.fill("Black")

        COST_BUTTON = Button(image=pygame.Surface((140, 30)), pos=(size[0] + 70, 310),
                               text_input=f"Cost: {cost}", font=get_font(14),
                               base_color="White", hovering_color="White")
        COST_BUTTON.image.fill("Black")

        STEP_BUTTON.update_text(f"Step: {step}")
        WEIGHT_BUTTON.update_text(f"Weight: {weight}")
        COST_BUTTON.update_text(f"Cost: {cost}")

        STEP_BUTTON.update(SCREEN)
        WEIGHT_BUTTON.update(SCREEN)
        COST_BUTTON.update(SCREEN)

        for button in [BFS_BUTTON, DFS_BUTTON, UCS_BUTTON, ASTAR_BUTTON, START_PAUSE_BUTTON, RESET_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN, is_hovering=button.rect.collidepoint(PLAY_MOUSE_POS))

        if game.is_completed():
            if not game_completed:  # Check if the game has not been marked as completed yet
                is_start = True  # Set is_start to True only once
                game_completed = True  # Mark as completed to prevent future changes
                SCREEN.fill(0)
                bfs_clicked = dfs_clicked = ucs_clicked = astar_clicked = False
            sokoban.display_end(SCREEN, (size[0] + 20, 350))

        sokoban.print_game(game.get_matrix(), SCREEN, level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    play()
                elif BFS_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    is_moving = False
                    bfs_clicked = True
                    dfs_clicked = ucs_clicked = astar_clicked = False
                    movement_string, weights = sokoban.solution(outputfile, 'bfs')
                    # No weight update here; it stays "0" until the first move

                elif DFS_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    is_moving = False
                    dfs_clicked = True
                    bfs_clicked = ucs_clicked = astar_clicked = False
                    movement_string, weights = sokoban.solution(outputfile, 'dfs')
                    # No weight update here; it stays "0" until the first move

                elif UCS_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    is_moving = False
                    ucs_clicked = True
                    bfs_clicked = dfs_clicked = astar_clicked = False
                    movement_string, weights = sokoban.solution(outputfile, 'ucs')
                    # No weight update here; it stays "0" until the first move

                elif ASTAR_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    is_moving = False
                    astar_clicked = True
                    bfs_clicked = dfs_clicked = ucs_clicked = False
                    movement_string, weights = sokoban.solution(outputfile, 'astar')
                    # No weight update here; it stays "0" until the first move

                elif START_PAUSE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    SCREEN.fill(0)
                    is_start = not is_start
                    is_moving = not is_moving
                    current_move_index = 0
                    move_timer = 0
                elif RESET_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    SCREEN.fill(0)
                    is_start = True
                    bfs_clicked = dfs_clicked = ucs_clicked = astar_clicked = False
                    game = reset_game(level)  # Reset everything by reloading the game
                    step = 0
                    weight = "0"  # Reset weight to 0
                    cost = 0
                    movement_string = ""  # Reset movement string
                    game_completed = False  # Reset game completed flag

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit(0)

        # Handle automated movement from the string
        if is_moving and current_move_index < len(movement_string):
            # Increment the move timer based on elapsed time
            move_timer += clock.get_time()

            if move_timer >= move_interval:
                # Get the first move from the string
                move = movement_string[0]
                move_timer = 0  # Reset the timer for the next move

                # Perform the move
                if move in "uU":
                    game.move(0, -1, True)
                elif move in "dD":
                    game.move(0, 1, True)
                elif move in "lL":
                    game.move(-1, 0, True)
                elif move in "rR":
                    game.move(1, 0, True)

                step += 1
                movement_string = movement_string[1:]  # Remove the first character

                if step > 0:  # Ensure step is greater than 0
                    # Use a try-except block to handle potential IndexError
                    try:
                        weight = str(weights[step - 1])  # Update weight as string
                    except IndexError:
                        weight = "0"  # Default to "0" if out of bounds

                cost = str(int(weight) + step)

        # Update the display
        pygame.display.update()

        # Maintain a consistent frame rate
        clock.tick(60)



def draw_member_board():
    # Coordinates for the board
    board_x = 200
    board_y = 100
    board_width = 880
    board_height = 500
    member_height = 80

    team_members = [
    {"name": "Phạm Thiên An 22120008", "duty": "Implement Breadth-First Search."},
    {"name": "Trương Vĩnh An 22120009", "duty": "Implement A* Search with heuristic."},
    {"name": "Nguyễn Đức Anh 22120013", "duty": "Implement Depth-First Search."},
    {"name": "Nguyễn Hữu Bền 22120029", "duty": "Implement Uniform Cost Search."},
    {"name": "Lý Trường Nam 22120218", "duty": "Implement Graphical User Interface."}]

    # Draw the member board
    pygame.draw.rect(SCREEN, (200, 200, 200), (board_x, board_y, board_width, board_height), 0)
    pygame.draw.rect(SCREEN, (0, 0, 0), (board_x, board_y, board_width, board_height), 5)  # Border

    # Draw each member's section
    for index, member in enumerate(team_members):
        member_y = board_y + (index * member_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), (board_x + 10, member_y + 10, board_width - 20, member_height - 20), 0)
        pygame.draw.rect(SCREEN, (0, 0, 0), (board_x + 10, member_y + 10, board_width - 20, member_height - 20), 2)  # Member border
        
        # Render the member's name and duty
        name_surface = pygame.font.Font("assets/vietnamese.otf", 20).render(member["name"], True, (0, 0, 0))
        duty_surface = pygame.font.Font("assets/vietnamese.otf", 15).render(member["duty"], True, (0, 0, 0))
        SCREEN.blit(name_surface, (board_x + 20, member_y + 16))
        SCREEN.blit(duty_surface, (board_x + 20, member_y + 44))


def members():
    while True:
        MEMBERS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        MEMBERS_BACK = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        MEMBERS_BACK.changeColor(MEMBERS_MOUSE_POS)
        MEMBERS_BACK.update(SCREEN)
        draw_member_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MEMBERS_BACK.checkForInput(MEMBERS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("ARES'S AVENTURE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"),(400,90)), pos=(640, 250), 
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        MEMBERS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"),(400,90)), pos=(640, 400), 
                            text_input="MEMBERS", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"),(400,90)), pos=(640, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, MEMBERS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if MEMBERS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    members()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()