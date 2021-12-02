import math
import time

from lightrover import Motor
from pll_odom import Odometry


def speed(v, w):
    # uR = 410*v+1
    # uL = 410*v+1

    T = 0.145
    uR = 410*v+205*T*w+1
    uL = 410*v-205*T*w+1
    return int(uR), int(uL)


motor = Motor()


odom = Odometry(motor)
vws = [(0.1, 0), (0.2, 0), (0.3, 0),
       (0, 10), (0, 20), (0, 30),
       (0.1, 10), (0.1, 20), (0.1, 30)]

for (tv, tw) in vws:
    print(f'tv:{tv} tw:{tw}')
    vs, ws = [], []
    for i in range(20):
        uR, uL = speed(tv, math.radians(tw))
        # print(f'uR:{uR} uL:{uL}')
        motor.drive(uR, uL)
        odom.update()
        v, w = (odom.vR + odom.vL) / 2, math.degrees(odom.w)
        vs.append(v)
        ws.append(w)
        # print(f'time:{odom.time:.3f} v:{v:.3f} w:{w:.1f}')
        time.sleep(0.05)
        # print(f'uR:{uR} uL:{uL}')

    motor.stop()
    time.sleep(3)
    vs, ws = vs[5:], ws[5:]
    print(
        f'Vのdiff {tv-sum(vs)/len(vs)}   v target: {tv} mean: {sum(vs)/len(vs): .3f} min: {min(vs): .3f} max: {max(vs): .3f}')
    print(
        f'Wのdiff {tw-sum(ws)/len(ws)}    w target: {tw} mean: {sum(ws)/len(ws): .1f} min: {min(ws): .1f} max: {max(ws): .1f}')
