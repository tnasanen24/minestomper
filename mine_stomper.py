"""
Modules for 
time related functions.
Writing and reading a json file.
Randomizing the game.
Graphics.
"""
import time
import json
import random
import sweeperlib

# The Game state dictionary
state = {
    "field": "",
    "field_mines": "",
    "field_lengths": "",
    "mine_amount": "",
    "win": "",
    "started": False,
    "stats": ""
}

stats = {
    "current time": time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()),
    "play_duration": 0,
    "turns" : 0,
    "mines_found": "",
    "result": "",
    "clicks": 0,
    "x_length": 0,
    "y_length": 0,
    "mine_amount": 0
}

saved_stats = [

]

# List of available tiles in the field for place_mines function
available = []

# Related to mouse_handler
MOUSE_DICT = {
    "1": "left",
    "2": "middle",
    "4": "right"
}

#Input messages for prompt_input
INP_MSG = {
    "x_len": "Please input an integer number for horizontal tiles: ",
    "y_len": "Please input an integer number for vertical tiles: ",
    "m_nmbr": "Please input an integer number of mines: ",
    "choose": "What will you choose? "
}
#Error messages for prompt_input
ERR_MSG = {
    "Int err": "You did not give an integer",
    "Str err": "You did not give a valid choice"
}

#Valid choices for menu input
#Enum('Choice', {'QUIT': ("q", "quit"), 'STATS': ("s", "stats"), 'PLAY': ("p", "play")})
VALID_CHOICE = ["p", "play", "s", "see stats", "q", "quit"]

def determine_field_size_and_tiles(x, y):
    """
    Determines the field size and returns it.
    Determines the minefield size and returns it.
    Produces the available tiles and appends them to available list outside.
    """
    field = []
    minefield = []
    #players view
    for row in range(y):
        field.append([])
        for col in range(x):
            field[-1].append(" ")

    #copy of the field for placing the mines and not showing to player.
    for row in range(y):
        minefield.append([])
        for col in range(x):
            minefield[-1].append(" ")


    #producing available tiles for placing mines
    for av_x in range(x):
        for av_y in range(y):
            available.append((av_x, av_y))
    return field, minefield

def place_mines(x, y):
    """
    Places N mines to a field in random tiles.
    Takes x and y tile coordinates from mouse handler.
    """
    #PRINT FOR ME!
    # print("place mines func:", x, y)
    # #PRINT FOR ME!
    # print("available tiles", available)
    available.remove((x, y))
    # #PRINT FOR ME!
    # print("available tiles", available)
    try:
        for i in range(state["mine_amount"]):
            random_number = random.randint(0, len(available) - 1)
            random_x, random_y = available[random_number]
            # #PRINT FOR ME!
            # print("random x: ", random_x, "x: ", x, "random y: ", random_y, "y: ", y)
            state["field_mines"][random_y][random_x] = "x"
            available.pop(random_number)
    except IndexError:
        print("Mouse click is out of bounds")
    # #PRINT FOR ME!
    # print("state field test:\n", state["field"])
    # #PRINT FOR ME!
    # print("state field mines test:\n", state["field_mines"])

def place_mine_count():
    """
    Places mine count on the adjacent tiles of mines
    """
    y_length = len(state["field_mines"])
    x_length = len(state["field_mines"][0])

    for i, row in enumerate(state["field_mines"]):
        for j, col in enumerate(row):
            if col == " ":
                state["field_mines"][i][j] = "0"
                for k in range(max(0, i-1), min(y_length -1, (i+1))+1):
                    for l in range(max(0, j - 1), min(x_length-1, (j+1))+1):
                        if state["field_mines"][k][l] == "x":
                            state["field_mines"][i][j] = int(state["field_mines"][i][j]) + 1
                            state["field_mines"][i][j] = str(state["field_mines"][i][j])

    # #PRINT FOR ME!
    # print(" ", "- " * len(state["field_mines"]))
    # for row in state["field_mines"]:
    #     print("|", " ".join(row), "|")
    # print(" ", "- " * len(state["field_mines"]))

def floodfill(x, y):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """
    y_length = len(state["field_mines"])
    x_length = len(state["field_mines"][0])

    coordinate_list = [(x, y)]
    while len(coordinate_list) > 0:
        x_coord, y_coord = coordinate_list.pop()
        state["field"][y_coord][x_coord] = state["field_mines"][y_coord][x_coord]
        # check_surrounding_tiles(x_coord, y_coord)
        for i in range(max(0, y_coord-1), min(y_length -1, (y_coord+1))+1):
            for j in range(max(0, x_coord - 1), min(x_length-1, (x_coord+1))+1):
                #PRINT FOR ME!
                # print("floodfill 1: ", state["field_mines"][i][j])
                if state["field_mines"][i][j] == "x":
                    state["field"][y][x] = state["field_mines"][y][x]
                    return
        for i in range(max(0, y_coord-1), min(y_length -1, (y_coord+1))+1):
            for j in range(max(0, x_coord - 1), min(x_length-1, (x_coord+1))+1):
                if state["field_mines"][i][j] == "0":
                    # #PRINT FOR ME!
                    # print(int(state["field_mines"][i][j]))
                    coordinate_list.append((j, i))
                    state["field"][i][j] = "0"
                    state["field_mines"][i][j] = "0 "
                    # #PRINT FOR ME!
                    # print("field mines list\n", state["field_mines"])
                    # #PRINT FOR ME!
                    # print(coordinate_list)
                else:
                    state["field"][i][j] = state["field_mines"][i][j].strip()

def print_game_stats(data, i=None):
    """
    Prints game stats, if player chooses "See stats"
    """
    if i:
        print(
            f"Match{i + 1:2} played at {data['current time']}\n",
        )
    else:
        print(
            f"These are the results of your match:\n"
            f"Match played at {data['current time']}\n"
        )
    print(
        f"Play duration: "
        f"{time.strftime('%Mmin:%Ss', time.localtime(int(data['play_duration'])))}\n"
        f"Result: {data['result']}\n"
        f"Turns: {data['turns']}\n"
        f"Field size: {str(data['x_length'])}x{str(data['y_length'])}\n"
        f"Total amount of mines at the start: {data['mine_amount']}\n"
        f"Mines flagged on the field: {data['mines_found']}\n"
        f"Mines left on the field: {data['mine_amount'] - data['mines_found']}\n"
    )

def load_game_stats():
    """
    Loads game stats from json file
    """
    try:
        with open("./minesweeper_stats.json", "r", encoding="utf-8") as target:
            return json.load(target)
    except (IOError, json.JSONDecodeError, FileNotFoundError):
        print("Unable to open the target file. Starting with an empty save.")

def save_game_stats(win):
    """
    Saves game stats to a json file
    Takes win condition as an argument.
    """
    try:
        with open("minesweeper_stats.json", "w", encoding="utf-8") as target:
            if win:
                stats["result"] = "Win"
            else:
                stats["result"] = "Lost"
            saved_stats.insert(0, stats)
            json.dump(saved_stats, target)
    except IOError:
        print("Unable to open the target file. Saving failed.")

def end_game_print_and_restart(win):
    """
    Prints if you lost or won the game.
    Closes the graphic window.
    And calls the main to initiate a new game, if the player chooses.
    """
    won_text = "You found all the mines"
    happy_face = "✧⋆٩(ˊᗜˋ )و ⋆✧"
    lost_text = "You hit a mine.. game over"
    sad_face = ".·°՞(¯□¯)՞°·."
    if win:
        print(
            "\n",
            len(won_text) * "⋆",
            f"\n{won_text}",
            "\n", happy_face.center(len(won_text)), "\n",
            len(won_text) * "⋆",
            "\n"
        )
    else:
        print(
            "\n",
            len(lost_text) * "⋆",
            f"\n{lost_text}",
            "\n", sad_face.center(len(won_text)), "\n",
            len(lost_text) * "⋆",
            "\n"
        )
    save_game_stats(win)
    print_game_stats(stats)
    sweeperlib.close()
    main()

def check_game_end_conditions():
    """
    Checks if game ending condition is met.
    Game ending condition is that all non-mine tiles have been opened.
    """
    open_tiles = 0
    valid_tiles = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    x_len, y_len = state["field_lengths"]
    field_size = x_len * y_len
    for row in state["field"]:
        for col in row:
            if col in valid_tiles:
                open_tiles += 1
    # print("Check end cond, open tiles: ", open_tiles)
    if open_tiles == field_size - state["mine_amount"]:
        stats["mines_found"] = state["mine_amount"]
        return True
    return False

def check_mines_found():
    """"
    Checks how many mines player has flagged. (found)
    """
    x_length, y_length = state["field_lengths"]
    # print("mines: ", mines)
    mines_found = 0
    #Check if player flagged all and only the correct mines
    for i in range(y_length):
        for j in range(x_length):
            if state["field"][i][j] == "f" and state["field_mines"][i][j] == "x":
                mines_found += 1
                #PRINT FOR ME!
                # print("mines found: ", mines_found)
    stats["mines_found"] = mines_found

def mouse_handler(x, y, button, modifier):
    """
    This function is called when a mouse button is clicked inside the game window.
    Changes the state dictionary depending on what tile was pressed.
    First mouse click calls place_mines function. Otherwise ignored.
    """
    #Amount of clicks for placing mines only on first click
    clicks = stats["clicks"]

    #Turns for counting opened tiles
    turns = stats["turns"]

    x_len = len(state["field_mines"][0])
    y_len = len(state["field_mines"])

    x = int(x / 40)
    y = int(y / 40)

    if x < 0 or (x_len - 1) < x:
        print("Mouse click is out of bounds")
        return
    elif y < 0 or (y_len -1) < y:
        print("Mouse click is out of bounds")
        return

    if button == sweeperlib.MOUSE_LEFT:
        clicks += 1
        stats["clicks"] = clicks
        state["started"] = True
        if state["field"][y][x] == " " or state["field"][y][x] == "f":
            turns += 1
        stats["turns"] = turns

        if clicks == 1:
            place_mines(x, y)
            place_mine_count()

        check_mines_found()
        floodfill(x, y)
        if state["field_mines"][y][x] == "x":
            end_game_print_and_restart(win=False)
        elif check_game_end_conditions():
            end_game_print_and_restart(win=True)

    if button == sweeperlib.MOUSE_RIGHT:
        if state["field"][y][x] == "f":
            state["field"][y][x] = " "
        elif state["field"][y][x] == " ":
            state["field"][y][x] = "f"

        check_mines_found()
    #PRINT FOR ME!
    # print(f"The {MOUSE_DICT[str(button)]} mouse button was pressed at {x}, {y}")

def draw_handler():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """

    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for i, l in enumerate(state["field"]):
        for j, key in enumerate(l):
            sweeperlib.prepare_sprite(key, j * 40, i * 40)

    sweeperlib.draw_sprites()

def interval_handler(elapsed):
    # things happen
    """
    Calls the draw handler to update the window.
    Calculates the elapsed time.
    """
    draw_handler()
    seconds = stats["play_duration"]
    seconds += elapsed
    stats["play_duration"] = seconds


def prompt_input(prompt, error_message, threshold_value):
    """
    Prompts the user for an integer using the prompt parameter.
    If an invalid input is given, an error message is shown using
    the error message parameter. Threshold value is used to parse too high values.
    A valid input is returned as an integer. 
    """
    user_input = 10**6
    while True:
        while user_input > threshold_value:
            try:
                user_input = int(input(prompt).strip())
            except ValueError:
                print(error_message)
            else:
                if user_input > threshold_value:
                    print("Value is over", threshold_value)
                    continue
                else:
                    return user_input

def prompt_string_input(prompt, error_message):
    """
    Prompts the user for a string using the prompt parameter.
    If an invalid input is given, an error message is shown using
    the error message parameter.
    Returns valid input
    """
    while True:
        menu_input = input(prompt).strip().lower()
        if menu_input in VALID_CHOICE:
            return menu_input
        else:
            print(error_message)

def main():
    """
    Main function that prints the instructions to terminal.
    Calls for prompt function and then determines actions based on user input.
    """
    print("Welcome to MineStomper")
    print("Open all the tiles that don't have a mine.")
    print("If you hit a mine you lose.")
    print(
        "You can choose to:\n"
        "(P)lay\n"
        "(S)ee stats\n"
        "(Q)uit\n"
    )

    menu_input = prompt_string_input(INP_MSG["choose"], ERR_MSG["Str err"])

    if menu_input == "p" or menu_input == "play":
        init_game_state()
        start_game()
    elif menu_input == "s" or menu_input == "see stats":
        data = load_game_stats()
        if data:
            for i, stat in enumerate(data[:5]):
                print_game_stats(stat, i)
        else:
            print("You do not have saved games yet\n")
        main()

    else:
        print("Goodbye")
        return

def init_game_state():
    """
    Initialises the game.
    """
    print("Max number of tiles horizontal/vertical is 100")
    print("Max number of mines is total number of tiles - 1")
    x_length = prompt_input(INP_MSG["x_len"], ERR_MSG["Int err"], 100)
    y_length = prompt_input(INP_MSG["y_len"], ERR_MSG["Int err"], 100)
    field, minefield = determine_field_size_and_tiles(x_length, y_length)
    mine_amount = prompt_input(INP_MSG["m_nmbr"], ERR_MSG["Int err"], (x_length * y_length - 1))
    global state
    state = {
        "field": field,
        "field_mines": minefield,
        "field_lengths": (x_length, y_length),
        "mine_amount": mine_amount,
        "win": "",
        "started": False
    }
    stats_dict = {
        "current time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "play_duration": 0,
        "turns" : 0,
        "mines_found": mine_amount,
        "result": "",
        "clicks": 0,
        "x_length": x_length,
        "y_length": y_length,
        "mine_amount": mine_amount
    }
    global stats
    stats = stats_dict

def start_game():
    """
    Starts the game graphics wise.
    """
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window()
    sweeperlib.set_draw_handler(draw_handler)
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_interval_handler(interval_handler, 1/60)
    sweeperlib.start()

if __name__ == "__main__":
    main()
