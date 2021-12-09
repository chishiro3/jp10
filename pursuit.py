import math
import time

import cv2
import numpy as np

from lightrover import Motor
from pll_odom import Odometry

H, W, scale = 600, 800, 250


def init_map():
    map = np.full((H+1, W+1, 3), 128, dtype=np.uint8)
    cv2.rectangle(map, (0, 0), (W, H), (230, 244, 248), -1)
    for h in range(0, H+1, 100):
        cv2.line(map, (0, h), (W, h), (0, 0, 0))
    for w in range(0, W+1, 100):
        cv2.line(map, (w, 0), (w, H), (0, 0, 0))
    cv2.line(map, (100, 0), (100, H), (0, 0, 0), thickness=2)
    cv2.line(map, (0, H-100), (W, H-100), (0, 0, 0), thickness=2)
    return map


def to_pixel(x, y):
    return int(x * scale) + 100, H - 100 - int(y * scale)


def speed(v, w):
    T = 0.145
    uR = 410*v+205*T*w+1
    uL = 410*v-205*T*w+1
    return int(uR), int(uL)


def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


motor = Motor()
odom = Odometry(motor)


waypoints = [(0, 0, 0), (0.2, 0, 0.1), (0.3, 0, 0.1), (0.4, 0.2, 0.1), (0.4, 0.3, 0.1), (0.4, 0.4, 0.1), (0.3, 0.5, 0.1),
             (0.2, 0.5, 0.1), (0.1, 0.5, 0.1), (0, 0.4, 0.1), (0, 0.3,
                                                               0.1), (0, 0.2, 0.1), (0, 0.1, 0.1), (0, 0, 0.1), (0, 0, 0)
             ]
L = 0.05
map = init_map()
trace = [(0, 0, 0, 0)]


cv2.imshow('pursuit', map)
for (wx, wy, wv) in waypoints:
    print(f'waypoint wx:{wx} wy:{wy} wv:{wv}')
    cv2.circle(map, to_pixel(wx, wy), 4, (255, 0, 0), thickness=-1)
    while distance(odom.x, odom.y, wx, wy) > L:
        pre = trace[-1]
        cv2.line(map, to_pixel(pre[1], pre[2]),
                 to_pixel(odom.x, odom.y), (0, 0, 255), 2)
        cv2.imshow('pursuit', map)
        cv2.waitKey(1)
        print("tesssssst")
        trace.append((odom.time, odom.x, odom.y))
        wxR = (wx - odom.x)*math.cos(odom.theta) + \
            (wy - odom.y)*math.sin(odom.theta)
        wyR = (wx - odom.x)*(-math.sin(odom.theta)) + \
            (wy - odom.y)*math.cos(odom.theta)
        ww = 0
        uR, uL = speed(wv, ww)
        motor.drive(uR, uL)
        odom.update()
        time.sleep(0.05)

print(f'time:{odom.time}')
cv2.imwrite('trace.png', map)
cv2.waitKey(0)
