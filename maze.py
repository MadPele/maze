from random import randint
import asyncio
import queue
from termcolor import colored

maze = [
    'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
    'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X',
    'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', 'X',
    'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', ' ', 'X',
    'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X', ' ', 'X',
    'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X', ' ', 'X',
    'X', ' ', ' ', ' ', 'X', 'X', ' ', 'X', ' ', 'X',
    'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X',
    'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X',
    'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'
]

single_path_maze = []
road = queue.Queue()
single_path = queue.Queue()

# str_maze = "11111101011000111111"5
# str_maze = "111111111.1.1..11.1.1..11......111111111"
str_maze = "11111111111111111111" \
           "1o1oooooo1o1oo1oooo1" \
           "1o1o1oooooo1oo1111o1" \
           "1o1o1111o1o1ooooooo1" \
           "1o1oooo1o1o1o11o1111" \
           "1o111111o1o1oo1oooo1" \
           "1oooooo1o1o1oo111111" \
           "11111oooo1o11oooooo1" \
           "1oooooooo1ooooooooo1" \
           "11111111111111111111"
# str_maze = ""

wall = '1'
footpath = 'o'
columns = 20


def import_maze(maze_str, wall, footpath):
    # Transfer string into array and replace walls and footpath
    if wall != 'X':
        maze_str = maze_str.replace(wall, 'X')
    if footpath != ' ':
        maze_str = maze_str.replace(footpath, ' ')

    return list(maze_str)


def print_maze(pmaze):
    # Print maze
    for r in range(rows):
        for c in range(columns):
            if len(str(pmaze[c + r * columns])) > 1:
                print(pmaze[c + r * columns], sep=' ', end=' ')
            else:
                if pmaze[c + r * columns] == 'S' or pmaze[c + r * columns] == 'E':
                    print(colored(pmaze[c + r * columns], 'red'), sep=' ', end='  ')
                elif pmaze[c + r * columns] == '*':
                    print(colored(pmaze[c + r * columns], 'green'), sep=' ', end='  ')
                elif pmaze[c + r * columns] == 'X':
                    print(colored(pmaze[c + r * columns], 'blue'), sep=' ', end='  ')
                else:
                    print(pmaze[c + r * columns], sep=' ', end='  ')
        print('')
    print('')


def copy_maze():
    sp_maze = []
    for item in maze:
        sp_maze.append(item)
    return sp_maze


def print_sigle_path(path):
    # Print shortest path from start to end
    position = start
    for letter in path:
        if letter == 'U':
            position -= columns
            single_path_maze[position] = '*'
        elif letter == 'D':
            position += columns
            single_path_maze[position] = '*'
        elif letter == 'L':
            position -= 1
            single_path_maze[position] = '*'
        elif letter == 'R':
            position += 1
            single_path_maze[position] = '*'

    print_maze(single_path_maze)


def set_point(point):
    # Set start/end point (manually or automatically)
    pointer = 0
    choice = input(f'Do you wanna set {point}ing point?(yes/no) ')
    while True:
        # Set start/end point manually
        if choice.lower() == 'yes' or choice.lower() == 'y':
            while True:
                print(f'Where you wanna {point}?')
                x_pointer = input('Coordinate X: ')
                try:
                    x_pointer = int(x_pointer)
                    if x_pointer < 1:
                        print('This coordinate are out of range')
                        continue
                    y_pointer = input('Coordinate Y: ')
                    y_pointer = int(y_pointer)
                    if y_pointer < 1:
                        print('This coordinate are out of range')
                        continue
                except ValueError:
                    print('This is not number!')
                    continue

                pointer = x_pointer - 1 + (y_pointer - 1) * columns
                try:
                    if maze[pointer] == ' ':
                        break
                    elif maze[pointer] == 'X':
                        print(f'You cant {point} on the wall!')
                    elif maze[pointer] == 'S':
                        print(f'Staring and ending coordinates can\'t be the same')
                except IndexError:
                    print('This coordinates are out of range')
                    continue
        elif choice.lower() == 'no' or choice.lower() == 'n':
            # Set start/end point automatically
            while True:
                pointer = randint(0, columns * rows - 1)
                if maze[pointer] == ' ':
                    break
        else:
            choice = input('This is not correct answer. Try again. ')
            continue
        break
    if point == 'start':
        # Set start point into maze
        print(f'Starting coordinates set on: X={(pointer%columns)+1} and Y={int(pointer/columns)+1}\n')
        maze[pointer] = 'S'
        return pointer
    elif point == 'end':
        # Set end point into maze
        print(f'Ending coordinates set on: X={(pointer%columns)+1} and Y={int(pointer/columns)+1}\n')
        maze[pointer] = 'E'


async def make_step(position, path, step):
    # Go up
    if maze[position - columns] == ' ':
        maze[position - columns] = step
        road.put(position - columns)
        single_path.put(path + 'U')
    elif maze[position - columns] == 'E':
        print('You hit end in: ' + str(step) + ' steps!\n')
        print('Shortest way to end:')
        print_sigle_path(path)
        print('Alternative ways:')
        print_maze(maze)
        exit()

    # Go down
    if maze[position + columns] == ' ':
        maze[position + columns] = step
        road.put(position + columns)
        single_path.put(path + 'D')
    elif maze[position + columns] == 'E':
        print('You hit end in: ' + str(step) + ' steps!\n')
        print('Shortest way to end:')
        print_sigle_path(path)
        print('Alternative ways:')
        print_maze(maze)
        exit()

    # Go left
    if maze[position - 1] == ' ':
        maze[position - 1] = step
        road.put(position - 1)
        single_path.put(path + 'L')
    elif maze[position - 1] == 'E':
        print('You hit end in: ' + str(step) + ' steps!\n')
        print('Shortest way to end:')
        print_sigle_path(path)
        print('Alternative ways:')
        print_maze(maze)
        exit()

    # Go right
    if maze[position + 1] == ' ':
        maze[position + 1] = step
        road.put(position + 1)
        single_path.put(path + 'R')
    elif maze[position + 1] == 'E':
        print('You hit end in: ' + str(step) + ' steps!\n')
        print('Shortest way to end:')
        print_sigle_path(path)
        print('Alternative ways:')
        print_maze(maze)
        exit()

    return True


async def make_all_ways():
    # Main function for searching exit from maze
    step = 1
    road.put(start)
    single_path.put('')
    task = True

    while task:
        for i in range(road.qsize()):
            position = road.get()
            path = single_path.get()
            position = int(position)
            task = asyncio.create_task(make_step(position, path, step))

            await task
            if not task:
                break
        step += 1


# Transfer string into maze if is any(and have at least 15 spots)
if len(str_maze) > 14:
    maze = import_maze(str_maze, wall, footpath)

rows = int(len(maze) / columns)

print_maze(maze)
start = set_point('start')
set_point('end')
single_path_maze = copy_maze()
asyncio.run(make_all_ways())
