import pygame
import random

# window params
width = 1000
height = 700
screen = None
# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
pink = (255, 0, 255)
obs_len = 7
found = False
# ---------
# Grid Properties
blocksize = 0
rows = 0
cols = 0
# -------------

running = True  # Main Loop Controller

opened = []
closed = []
first = True
w = 0.5  # Huristic Obstacle Wieght
inip = (0, 0)
cp = (0, 0)  # starting position

# Matrix Mapping
status_matrix = []
# -------------


def check(k):
    k = int(k)
    return k != 1


# Movements
def up(cur_pos):
    if cur_pos[1] - 1 >= 0:
        k = status_matrix[cur_pos[0]][cur_pos[1] - 1]
        if check(k):
            return (cur_pos[0], cur_pos[1] - 1)


def down(cur_pos):
    if cur_pos[1] + 1 < rows:
        k = status_matrix[cur_pos[0]][cur_pos[1] + 1]
        if check(k):
            return (cur_pos[0], cur_pos[1] + 1)


def forward(cur_pos):
    if cur_pos[0] + 1 < cols:
        k = status_matrix[cur_pos[0] + 1][cur_pos[1]]
        if check(k):
            return (cur_pos[0] + 1, cur_pos[1])


def backward(cur_pos):
    if cur_pos[0] - 1 >= 0:
        k = status_matrix[cur_pos[0] - 1][cur_pos[1]]
        if check(k):
            return (cur_pos[0] - 1, cur_pos[1])
# ---------


# Queue Ops
def enqueue(val):
    global first
    if val not in closed:
        first = False
        ct = cost(val)
        hu = huristic(val)
        # if ct > hu:
        # ct = 0.01*(abs(ct - hu)) * ct
        opened.append([hu, val])


def dequeue():
    global search
    if len(opened) == 0:
        print("Unable To Find Any solution")
        search = False
        return
    opened.sort()
    val = opened.pop(0)[1]
    closed.append(val)
    return val
# --------------


# Calculation Functions
def cost(cur_pos):
    sl = status_matrix[:cur_pos[0]][:cur_pos[1]]
    obstacles = 0
    for i in range(0, len(sl)):
        for j in range(0, len(sl[i])):
            if sl[i][j] == 2:
                obstacles += 1
    a = abs(cur_pos[0] - inip[0])**2 + abs(cur_pos[1] - inip[1])**2
    return a - obstacles * w


def huristic(cur_pos):
    sl = status_matrix[cur_pos[0]:][cur_pos[1]:]
    obstacles = 0
    for i in range(0, len(sl)):
        for j in range(0, len(sl[i])):
            if sl[i][j] == 2:
                obstacles += 1
    a = abs(cur_pos[0] - (cols - 1))**2 + abs(cur_pos[1] - (rows - 1))**2
    return a + obstacles * w


def astar(curPos):
    global found
    if status_matrix[curPos[0]][curPos[1]] == 3:
        print("Found")
        return
    else:
        up_pos = up(curPos)
        if up_pos is not None:
            enqueue(up_pos)

        down_pos = down(curPos)
        if down_pos is not None:
            enqueue(down_pos)

        forward_pos = forward(curPos)
        if forward_pos is not None:
            enqueue(forward_pos)

        backward_pos = forward(curPos)
        if backward_pos is not None:
            enqueue(backward_pos)

        new_pos = dequeue()
        if new_pos is None:
            print("Unable to find any solution!")
            exit(0)
        if (status_matrix[new_pos[0]][new_pos[1]] == 3):
            print("Found")
            found = True
            return (-1, -1)
        status_matrix[new_pos[0]][new_pos[1]] = 2

        return new_pos


def highlight_path():
    for i in closed:
        status_matrix[i[0]][i[1]] = 4


def init(size, initPos):
    global screen
    global blocksize
    global rows
    global cols
    global status_matrix
    global cp
    global inip
    inip = initPos
    cp = initPos
    # Difficulty
    size = int(size)
    if size == 1:
        print("OK1")
        blocksize = 20
    elif size == 2:
        print("OK2")
        blocksize = 10
    elif size == 3:
        print("OK3")
        blocksize = 5
    elif size == 4:
        print("Toughest")
        blocksize = 2
    else:
        blocksize = 5
    rows = height//blocksize
    cols = width//blocksize
    status_matrix = [[0 for i in range(rows)]
                     for j in range(cols)]
    status_matrix[cp[0]][cp[1]] = 2    # Starting
    status_matrix[-1][-1] = 3  # Goal
    pygame.init()
    screen = pygame.display.set_mode([width, height])


def setup_obstacles():
    for i in range(0, cols*rows//70):
        x = random.randint(1, cols - obs_len)
        y = random.randint(1, rows - obs_len)
        status_matrix[x][y] = 1
        for i in range(0, obs_len):
            if x + i < cols:
                status_matrix[x + i][y] = 1

    for i in range(0, cols*rows//70):
        x = random.randint(1, cols - obs_len)
        y = random.randint(1, rows - obs_len)
        print(x, y)
        status_matrix[x][y] = 1
        for i in range(0, obs_len):
            if y + i < rows:
                status_matrix[x][y + i] = 1


def main():

    global running
    global found
    global screen
    global cp
    size = input("Enter Difficulty Level: ")
    x = input("Enter initial X: ")
    y = input("Enter inital Y: ")
    init(size, (int(x), int(y)))
    setup_obstacles()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        fill = False
        m, k = 0, 0
        if not found:
            cp = astar(cp)
        if cp == (-1, -1):
            highlight_path()
            print("OVER!")
        k = 0
        m = 0

        # Draw sequence
        for i in range(0, 1000, blocksize):
            m = 0
            for j in range(0, 700, blocksize):
                fill = 1
                color = black
                if status_matrix[k][m] == 1:
                    fill = 0
                    color = white
                elif status_matrix[k][m] == 2:
                    fill = 0
                    color = red
                elif status_matrix[k][m] == 3:
                    fill = 0
                    color = green
                elif status_matrix[k][m] == 4:
                    fill = 0
                    color = pink
                pygame.draw.rect(screen, color,
                                 (i, j, blocksize, blocksize), fill)
                m += 1
            k += 1

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
