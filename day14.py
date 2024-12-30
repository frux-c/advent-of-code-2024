import readfile
import numpy as np
import time
import signal

test_data = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

data = readfile.read_day_file(14)

def part_one():
    p1data = data.strip().split("\n")
    p1data = [x.split(" ") for x in p1data]
    p1data = [(tuple(map(int, x[0].split("=")[1].split(","))), tuple(map(int, x[1].split("=")[1].split(",")))) for x in p1data]
    n, m  = 103, 101
    s = 100
    nparr = np.zeros((n, m), dtype=int)
    _map = {}
    for i, ((py, px), (vy, vx)) in enumerate(p1data, 1):
        _map[i] = (px, py, vx, vy)
        for _ in range(s):
            px, py, vx, vy = _map[i]
            _map[i] = ((px + vx) % n, (py + vy) % m, vx, vy)

    for _, v in _map.items():
        x, y, _, _ = v
        nparr[x][y] += 1

    # split into 4 quadrants not including the x and y axis
    q1, q2, q3, q4 = 0, 0, 0, 0
    mid_x, mid_y = n // 2, m // 2
    for i in range(n):
        for j in range(m):
            if i == mid_x or j == mid_y:
                continue
            # q1
            if i < mid_x and j < mid_y:
                q1 += nparr[i][j]
            # q2
            if i < mid_x and j > mid_y:
                q2 += nparr[i][j]
            # q3
            if i > mid_x and j < mid_y:
                q3 += nparr[i][j]
            # q4
            if i > mid_x and j > mid_y:
                q4 += nparr[i][j]
    print(q1, q2, q3, q4)
    print(q1 * q2 * q3 * q4)

ti = 0
def signal_handler(sig, frame):
    global ti
    print('You pressed Ctrl+C!')
    ti += 1
    print(ti)

def part_two():
    p1data = data.strip().split("\n")
    p1data = [x.split(" ") for x in p1data]
    p1data = [(tuple(map(int, x[0].split("=")[1].split(","))), tuple(map(int, x[1].split("=")[1].split(",")))) for x in p1data]
    n, m  = 103, 101
    nparr = np.full((n, m), ".", dtype=str)
    
    _map = {}
    for i, ((py, px), (vy, vx)) in enumerate(p1data, 1):
        _map[i] = (px, py, vx, vy)

    s = 0
    signal.signal(signal.SIGINT, signal_handler)
    with open("output.txt", "w") as f:
        while s < 100000:
            for k, v in _map.items():
                x, y, _, _ = v
                nparr[x][y] = "T"
            print(s)
            art = '\n'.join([''.join([str(cell) for cell in row]) for row in nparr])
            f.write(f"Second: {s}\n")
            f.write(art + "\n\n")
            time.sleep(0.1)
            nparr = np.full((n, m), ".", dtype=str)
            for k, v in _map.items():
                px, py, vx, vy = v
                _map[k] = ((px + vx) % n, (py + vy) % m, vx, vy)
            s += 1
        
part_two()
