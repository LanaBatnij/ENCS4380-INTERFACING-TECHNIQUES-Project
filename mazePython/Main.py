import API
import sys

class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

N = 16
INF = 10**9 + 5
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
prev_path = [[0] * N for _ in range(N)]
current_path = [[0] * N for _ in range(N)]
flood = [[0] * N for _ in range(N)]
targets = [[N // 2 - 1, N // 2 - 1], [N // 2, N // 2 - 1], [N // 2 - 1, N // 2], [N // 2, N // 2]]
neighbours = [[set() for _ in range(N)] for _ in range(N)]
visited = [[False] * N for _ in range(N)]
previous = [[Pair(0, 0) for _ in range(N)] for _ in range(N)]


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def move_cells(x, y, x0, y0, direction, parent, ok=False):
    path = ""
    x00, y00 = x0, y0

    while parent[x0][y0][0] != -1:
        p = parent[x0][y0]
        if p[0] == x0:
            if y0 < p[1]:
                path += 'R'
            else:
                path += 'L'
        else:
            if x0 < p[0]:
                path += 'D'
            else:
                path += 'U'
        x0, y0 = p[0], p[1]

    must = 3 * (path[0] == 'L') + 2 * (path[0] == 'D') + 1 * (path[0] == 'R')

    while direction != must:
        direction = (direction + 1) % 4
        API.turnRight()

    for c in path:
        if ok:
            API.setColor(y00, N - x00 - 1, 'G')

        p = parent[x00][y00]
        x00, y00 = p[0], p[1]

        if c == 'L':
            if direction == 0:
                direction = 3
                API.turnLeft()
            elif direction == 2:
                direction = 3
                API.turnRight()
        elif c == 'R':
            if direction == 0:
                direction = 1
                API.turnRight()
            elif direction == 2:
                direction = 1
                API.turnLeft()
        elif c == 'U':
            if direction == 1:
                direction = 0
                API.turnLeft()
            elif direction == 3:
                direction = 0
                API.turnRight()
        else:
            if direction == 1:
                direction = 2
                API.turnRight()
            elif direction == 3:
                direction = 2
                API.turnLeft()

        API.moveForward()

    if ok:
        API.setColor(y00, N - x00 - 1, 'G')

    return direction

def get_path(x, y, x0, y0, direction, ok=False):
    if x == x0 and y == y0:
        return direction

    q = [[x, y]]
    visited2 = [[False] * N for _ in range(N)]
    visited2[x][y] = True
    parent = [[(-1, -1) for _ in range(N)] for _ in range(N)]

    while q:
        current = q[0]
        q.pop(0)
        xx, yy = current[0], current[1]

        for nei in neighbours[xx][yy]:
            nx, ny = nei[0], nei[1]
            if visited2[nx][ny]:
                continue
            visited2[nx][ny] = True
            q.append([nx, ny])
            parent[nx][ny] = (xx, yy)

    assert visited2[x0][y0]
    return move_cells(x, y, x0, y0, direction, parent, ok)

def check(x, y):
    return 0 <= x < N and 0 <= y < N

def check_left(x, y, dir, p):
    return not API.wallLeft() and check(x + p[0], y + p[1])

def check_right(x, y, dir, p):
    return not API.wallRight() and check(x + p[0], y + p[1])

def check_front(x, y, dir, p):
    return not API.wallFront() and check(x + p[0], y + p[1])

def is_goal(x, y):
    return (x == N // 2 or x == N // 2 - 1) and (y == N // 2 or y == N // 2 - 1)

def get_around(x, y, direction):
    around = []
    p = API.get_dir(direction, 0)

    if check_front(x, y, direction, p):
        around.append([flood[N - (y + p[1]) - 1][x + p[0]], 0])
        neighbours[N - y - 1][x].add((N - (y + p[1]) - 1, x + p[0]))
        neighbours[N - (y + p[1]) - 1][x + p[0]].add((N - y - 1, x))

    p = API.get_dir(direction, 1)
    if check_right(x, y, direction, p):
        around.append([flood[N - (y + p[1]) - 1][x + p[0]], 1])
        neighbours[N - y - 1][x].add((N - (y + p[1]) - 1, x + p[0]))
        neighbours[N - (y + p[1]) - 1][x + p[0]].add((N - y - 1, x))

    p = API.get_dir(direction, 2)
    if check_left(x, y, direction, p):
        around.append([flood[N - (y + p[1]) - 1][x + p[0]], 2])
        neighbours[N - y - 1][x].add((N - (y + p[1]) - 1, x + p[0]))
        neighbours[N - (y + p[1]) - 1][x + p[0]].add((N - y - 1, x))

    if previous[x][y][0] != -1:
        prev_x, prev_y = previous[x][y]
        around.append([flood[N - prev_y - 1][prev_x], 3])

    around.sort()
    return around

def flood_fill(x, y):
    q = [[x, y]]

    while q:
        v = q[0]
        q.pop(0)
        x, y = v[0], v[1]

        if visited[x][y]:
            mn = INF
            for nei in neighbours[x][y]:
                nx, ny = nei
                mn = min(mn, flood[nx][ny])

            if flood[x][y] <= mn:
                flood[x][y] = mn + 1
                API.setText(y, N - x - 1, str(flood[x][y]))

                for nei in neighbours[x][y]:
                    nx, ny = nei
                    q.append([nx, ny])
        else:
            mn = INF
            for a in range(4):
                nx, ny = x + dx[a], y + dy[a]
                if not check(nx, ny):
                    continue
                mn = min(mn, flood[nx][ny])

            if flood[x][y] <= mn:
                flood[x][y] = mn + 1
                API.setText(y, N - x - 1, str(flood[x][y]))

                for a in range(4):
                    nx, ny = x + dx[a], y + dy[a]
                    if not check(nx, ny):
                        continue
                    q.append([nx, ny])

def explore():
    global prev_path
    x, y, direction = 0, 0, 0

    for cell in targets:
        visited[cell[0]][cell[1]] = False

    while True:
        API.setColor(x, y, 'G')
        API.fix_walls(x, y, direction)
        visited[N - y - 1][x] = True
        current_path.append([x, y])

        if is_goal(x, y):
            break

        around = get_around(x, y, direction)

        if flood[N - y - 1][x] <= around[0][0]:
            flood_fill(N - y - 1, x)

        p = API.get_dir(direction, around[0][1])

        if around[0][1] == 1:
            direction = (direction + 1) % 4
            API.turnRight()
        elif around[0][1] == 2:
            direction = (direction - 1) % 4
            API.turnLeft()
        elif around[0][1] == 3:
            direction = (direction + 2) % 4
            API.turnRight()
            API.turnRight()

        API.moveForward()
        previous[x + p[0]][y + p[1]] = [x, y]
        x += p[0]
        y += p[1]

    if current_path == prev_path:
        direction = get_path(N - 1, 0, N - y - 1, x, direction)
        API.clearAllColor()

        while direction != 0:
            direction = (direction + 1) % 4
            API.turnRight()

        v = []
        for c in targets:
            if visited[c[0]][c[1]]:
                v = c
                break

        direction = get_path(v[0], v[1], N - 1, 0, direction, True)
        return

    prev_path = current_path.copy()
    current_path.clear()
    direction = get_path(N - 1, 0, N - y - 1, x, direction)

    while direction != 0:
        direction = (direction + 1) % 4
        API.turnRight()

    explore()

def init():
    global visited, flood, previous

    visited = [[False] * N for _ in range(N)]
    flood = [[INF] * N for _ in range(N)]
    previous = [[(-1, -1) for _ in range(N)] for _ in range(N)]

    q = []
    for v in targets:
        q.append([0, v[0], v[1]])
        flood[v[0]][v[1]] = 0
        API.setText(v[0], v[1], str(flood[v[0]][v[1]]))

    while q:
        v = q[0]
        q.pop(0)
        x, y, cost = v[1], v[2], v[0]

        for a in range(4):
            nx, ny = x + dx[a], y + dy[a]
            if not check(nx, ny):
                continue

            if cost + 1 >= flood[nx][ny]:
                continue

            flood[nx][ny] = cost + 1
            API.setText(nx, ny, str(flood[nx][ny]))
            q.append([cost + 1, nx, ny])

        q.sort()

def main():
    init()
    explore()

if __name__ == "__main__":
    main()
