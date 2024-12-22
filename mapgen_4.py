# IMPORTS
import time
import os
import random

# PREDEFINED VARIABLES
# Text Colors
ANSI_RED = "\033[0;31;49m"
ANSI_GREEN = "\033[0;32;49m"
ANSI_PURPLE = "\033[0;35;49m"
ANSI_CYAN = "\033[0;36;49m"
ANSI_WHITE = "\033[0;37;49m"

# FUNCTIONS
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    """Funtion to sanitize inputs."""
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return ui


def clear_screen():
    """Clear all output on the screen."""
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def draw_tile(color):
    """Draws a tile of a specified color."""
    t.pendown()
    t.pensize(1)
    t.color(color)
    t.begin_fill()
    for i in range(2):
        t.forward(TILE_SIZE)
        t.right(90)
        t.forward(TILE_SIZE)
        t.right(90)
    t.end_fill()
    t.penup()
    t.forward(TILE_SIZE)

# MAIN CODE
# SECTION 1: USER INPUT
clear_screen()
print("""Welcome to MapGen 4!
This is my (now second) best map-generation project, yet
my first using Python Turtle. This project generates a map
based on certain specifications, which you will choose below.""")
map_width = int(sanitised_input("Map Width: ", int, min_=10, max_=100))
map_height = int(sanitised_input("Map Height: ", int, min_=10, max_=100))
print("""Please choose one of the following color sets,
which will decide what colors are used to represent different
things on the map.""")
print(ANSI_GREEN+"Normal")
print(ANSI_RED+"Martian")
print(ANSI_CYAN+"Aquamarine")
print(ANSI_PURPLE+"Mountain")
color_set = sanitised_input(ANSI_WHITE, str, range_=(
    "Normal", "Martian", "Aquamarine", "Mountain"))
clear_screen()

# SECTION 2: MAP GENERATION
# Generation Setup
print(ANSI_CYAN+"Setup...", end="\r")
total_tiles = map_width*map_height
tiles = []
for i in range(total_tiles):
    tiles.append("blank")
# Tile Size Computing
if map_height > map_width:
    map_size = map_height
else:
    map_size = map_width
TILE_SIZE = 50
while (TILE_SIZE*map_size) > 500:
    TILE_SIZE -= 1
print(ANSI_GREEN+"Setup Complete")
# Primary Generation - Land, Sand, and Water
print(ANSI_CYAN+"Primary Generation...", end="\r")
# First Tile
random_num = random.randint(1, 3)
if random_num == 1:
    tiles[0] = "land"
elif random_num == 2:
    tiles[0] = "water"
else:
    tiles[0] = "sand"
# First Line of Tiles
print(ANSI_CYAN+"Primary Generation", end="\r")
for i in range(1, map_width):
    previous_tile = tiles[i-1]
    random_num = random.randint(1, 100)
    if previous_tile == "land":
        if random_num <= 70:
            tiles[i] = "land"
        else:
            tiles[i] = "sand"
    elif previous_tile == "sand":
        if random_num <= 50:
            tiles[i] = "land"
        else:
            tiles[i] = "water"
    else:
        if random_num <= 80:
            tiles[i] = "water"
        else:
            tiles[i] = "sand"
for y in range(1, map_height):
    # First Tile in each line (except First Line)
    i = y*map_width
    above_tile = tiles[i-map_width]
    random_num = random.randint(1, 100)
    if above_tile == "land":
        if random_num <= 70:
            tiles[i] = "land"
        else:
            tiles[i] = "sand"
    elif above_tile == "sand":
        if random_num <= 50:
            tiles[i] = "land"
        else:
            tiles[i] = "water"
    else:
        if random_num <= 80:
            tiles[i] = "water"
        else:
            tiles[i] = "sand"
    # Each Line (except First Line)
    for x in range(map_width-1):
        i = (y*map_width)+x+1
        previous_tile = tiles[i-1]
        above_tile = tiles[i-map_width]
        random_num = random.randint(1, 100)
        if previous_tile == "land":
            if above_tile == "land":
                if random_num <= 70:
                    tiles[i] = "land"
                else:
                    tiles[i] = "sand"
            elif above_tile == "sand":
                if random_num <= 70:
                    tiles[i] = "land"
                else:
                    tiles[i] = "sand"
            else:
                if random_num <= 5:
                    tiles[i] = "land"
                elif random_num <= 95:
                    tiles[i] = "sand"
                else:
                    tiles[i] = "water"
        elif previous_tile == "sand":
            if above_tile == "land":
                if random_num <= 30:
                    tiles[i] = "sand"
                else:
                    tiles[i] = "land"
            elif above_tile == "sand":
                if x >= 2:
                    pre_previous_tile = tiles[i-2]
                    if pre_previous_tile == "land" and random_num <= 50:
                        tiles[i-2] = "water"
                if random_num <= 50:
                    tiles[i] = "land"
                else:
                    tiles[i] = "water"
            else:
                if random_num <= 30:
                    tiles[i] = "sand"
                else:
                    tiles[i] = "water"
        else:
            if above_tile == "land":
                if random_num <= 5:
                    tiles[i] = "land"
                elif random_num <= 95:
                    tiles[i] = "sand"
                else:
                    tiles[i] = "water"
            elif above_tile == "sand":
                if random_num <= 70:
                    tiles[i] = "water"
                else:
                    tiles[i] = "sand"
            else:
                if random_num <= 80:
                    tiles[i] = "water"
                else:
                    tiles[i] = "sand"
print(ANSI_GREEN+"Primary Generation Complete")
# Secondary Generation - Rock, Shallow Water, and Sand Replacement
print(ANSI_CYAN+"Secondary Generation", end="\r")
for i in range(len(tiles)):
    # Rock Generation
    if tiles[i] == "sand":
        if i % map_width != 0:
            previous_tile = tiles[i-1]
        else:
            previous_tile = "land"
        if i % map_width != map_width-1:
            next_tile = tiles[i+1]
        else:
            next_tile = "land"
        if i >= map_width:
            above_tile = tiles[i-map_width]
        else:
            above_tile = "land"
        if i < (map_height-1)*map_width:
            below_tile = tiles[i+map_width]
        else:
            below_tile = "land"
        if((previous_tile != "water" and previous_tile != "swater") and
                (next_tile != "water" and next_tile != "swater") and
                (above_tile != "water" and above_tile != "swater") and
                (below_tile != "water" and below_tile != "swater")):
            tiles[i] = "rock"
        # Extra Sand Replacement
        if i % map_width != 0:
            previous_tile = tiles[i-1]
        else:
            previous_tile = "water"
        if i % map_width != map_width-1:
            next_tile = tiles[i+1]
        else:
            next_tile = "water"
        if i >= map_width:
            above_tile = tiles[i-map_width]
        else:
            above_tile = "water"
        if i < (map_height-1)*map_width:
            below_tile = tiles[i+map_width]
        else:
            below_tile = "water"
        count = 0
        # Checks for 75 %  water and no land or rock
        if previous_tile == "water":
            count += 1
        elif previous_tile != "sand":
            count = -100
        if next_tile == "water":
            count += 1
        elif next_tile != "sand":
            count = -100
        if above_tile == "water":
            count += 1
        elif above_tile != "sand":
            count = -100
        if below_tile == "water":
            count += 1
        elif below_tile != "sand":
            count = -100
        if count > 2:
            if random_num <= 65:
                tiles[i] = "water"
    # Shallow Water Generation
    if tiles[i] == "land" or tiles[i] == "sand":
        if i % map_width != 0:
            previous_tile = tiles[i-1]
        else:
            previous_tile = "land"
        if i % map_width != map_width-1:
            next_tile = tiles[i+1]
        else:
            next_tile = "land"
        if i >= map_width:
            above_tile = tiles[i-map_width]
        else:
            above_tile = "land"
        if i < (map_height-1)*map_width:
            below_tile = tiles[i+map_width]
        else:
            below_tile = "land"
        if previous_tile == "water" and i % map_width != 0:
            random_num = random.randint(1, 100)
            if random_num <= 70:
                tiles[i-1] = "swater"
        if next_tile == "water" and i % map_width != map_width-1:
            random_num = random.randint(1, 100)
            if random_num <= 70:
                tiles[i+1] = "swater"
        if above_tile == "water" and i >= map_width:
            random_num = random.randint(1, 100)
            if random_num <= 70:
                tiles[i-map_width] = "swater"
        if below_tile == "water" and i < (map_height-1)*map_width:
            random_num = random.randint(1, 100)
            if random_num <= 70:
                tiles[i+map_width] = "swater"
print(ANSI_GREEN+"Secondary Generation Complete")
# Tertiary Generation - Darker Rock and Deep Water
print(ANSI_CYAN+"Tertiary Generation", end="\r")
for i in range(len(tiles)):
    # Darker Rock Generation
    if tiles[i] == "rock":
        if i % map_width != 0:
            previous_tile = tiles[i-1]
        else:
            previous_tile = "land"
        if i % map_width != map_width-1:
            next_tile = tiles[i+1]
        else:
            next_tile = "land"
        if i >= map_width:
            above_tile = tiles[i-map_width]
        else:
            above_tile = "land"
        if i < (map_height-1)*map_width:
            below_tile = tiles[i+map_width]
        else:
            below_tile = "land"
        if previous_tile == "land" and i % map_width != 0:
            random_num = random.randint(1, 100)
            if random_num <= 75:
                tiles[i-1] = "drock"
        if next_tile == "land" and i % map_width != map_width-1:
            random_num = random.randint(1, 100)
            if random_num <= 75:
                tiles[i+1] = "drock"
        if above_tile == "land" and i >= map_width:
            random_num = random.randint(1, 100)
            if random_num <= 75:
                tiles[i-map_width] = "drock"
        if below_tile == "land" and i < (map_height-1)*map_width:
            random_num = random.randint(1, 100)
            if random_num <= 75:
                tiles[i+map_width] = "drock"
    # Deep Water Generation
    elif tiles[i] == "water":
        if i % map_width != 0:
            previous_tile = tiles[i-1]
        else:
            previous_tile = "water"
        if i % map_width != map_width-1:
            next_tile = tiles[i+1]
        else:
            next_tile = "water"
        if i >= map_width:
            above_tile = tiles[i-map_width]
        else:
            above_tile = "water"
        if i < (map_height-1)*map_width:
            below_tile = tiles[i+map_width]
        else:
            below_tile = "water"
        if((previous_tile == "water" or previous_tile == "dwater") and
                (next_tile == "water" or next_tile == "dwater") and
                (above_tile == "water" or above_tile == "dwater") and
                (below_tile == "water" or below_tile == "dwater")):
            random_num = random.randint(1, 100)
            if random_num <= 85:
                tiles[i] = "dwater"
print(ANSI_GREEN+"Tertiary Generation Complete")
# Map Generation Complete
print("Map Generation Complete"+ANSI_WHITE)
time.sleep(2)
clear_screen()

# SECTION 3: MAP PRINTING
# turtle import lower to prevent console disappearing
# Setup
import turtle as t
t.speed(0)
t.colormode(255)
t.title("MapGen 4")
t.hideturtle()
t.penup()
TURTLE_SIZE = 20
screen = t.Screen()
screen.setup(width=600, height=600, startx=0, starty=0)
t.goto(TURTLE_SIZE/2 - screen.window_width()/2,
       screen.window_height()/2 - TURTLE_SIZE/2)
t.pendown()
# Color Choosing
color_land = color_sand = color_s_water = color_water = (0, 0, 0)
color_d_water = color_d_rock = color_rock = (0, 0, 0)
if color_set == "Normal":
    color_land = (0, 102, 0)
    color_sand = (153, 153, 0)
    color_s_water = (0, 57, 160)
    color_water = (0, 0, 153)
    color_d_water = (0, 0, 100)
    color_d_rock = (64, 64, 64)
    color_rock = (80, 80, 80)
elif color_set == "Martian":
    color_land = (175, 60, 60)
    color_sand = (100, 40, 40)
    color_s_water = (75, 25, 25)
    color_water = (0, 57, 160)
    color_d_water = (0, 0, 153)
    color_d_rock = (219, 75, 75)
    color_rock = (255, 90, 90)
elif color_set == "Aquamarine":
    color_land = (120, 210, 33)
    color_sand = (178, 193, 60)
    color_s_water = (128, 255, 192)
    color_water = (90, 220, 170)
    color_d_water = (75, 190, 150)
    color_d_rock = (80, 88, 92)
    color_rock = (95, 105, 110)
elif color_set == "Mountain":
    color_land = (100, 100, 100)
    color_sand = (80, 80, 80)
    color_s_water = (60, 60, 60)
    color_water = (40, 120, 40)
    color_d_water = (0, 0, 153)
    color_d_rock = (220, 220, 220)
    color_rock = (120, 120, 120)
# Stats
print(ANSI_CYAN+"""Map Stats
Note that "water" is not necessarily blue or resembling water.
Same goes for every other color."""+ANSI_WHITE)
print("Land:", str(round(tiles.count("land")*100/len(tiles), 2))+"%")
print("Sand:", str(round(tiles.count("sand")*100/len(tiles), 2))+"%")
print("Shallow Water:", str(round(tiles.count("swater")*100/len(tiles), 2))+"%")
print("Water:", str(round(tiles.count("water")*100/len(tiles), 2))+"%")
print("Deep Water:", str(round(tiles.count("dwater")*100/len(tiles), 2))+"%")
print("Darker Rock:", str(round(tiles.count("drock")*100/len(tiles), 2))+"%")
print("Lighter Rock:", str(round(tiles.count("rock")*100/len(tiles), 2))+"%")

# Map Printing
for y in range(map_height):
    for x in range(map_width):
        i = y*map_width+x
        if tiles[i] == "land":
            tile_color = color_land
        elif tiles[i] == "sand":
            tile_color = color_sand
        elif tiles[i] == "swater":
            tile_color = color_s_water
        elif tiles[i] == "water":
            tile_color = color_water
        elif tiles[i] == "dwater":
            tile_color = color_d_water
        elif tiles[i] == "drock":
            tile_color = color_d_rock
        elif tiles[i] == "rock":
            tile_color = color_rock
        else:
            tile_color = (0, 0, 0)
        draw_tile(tile_color)
    t.right(90)
    t.forward(TILE_SIZE)
    t.right(90)
    t.forward(TILE_SIZE * map_width)
    t.right(180)

t.Screen().exitonclick()
