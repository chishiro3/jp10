import math
import time

import matplotlib.pyplot as plt
import numpy as np

from lightrover import Motor
from pll_odom import Odometry

motor = Motor()
odom = Odometry(motor)
mvs, us = [], [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for u in us:
    print(f'u:{u}')
    vs = []
    for i in range(20):
        motor.drive(u, u)
        odom.update()
        e, t = motor.encoder(), motor.target()
        v = (odom.vR + odom.vL) / 2
        vs.append(v)
        print(f'time:{odom.time:.3f} e:{e} t:{t} v:{v:.3f}')
        time.sleep(0.05)
        mvs.append(sum(vs[5:]) / len(vs[5:]))

        motor.stop()
        time.sleep(3)
print(f'us:{us}')
print(f'mvs:{mvs}')
c = np.polyfit(mvs, us, 1)
print(f'u = {c[0]} v + {c[1]}')
plt.figure()
plt.plot(mvs, us)
plt.grid()
plt.xlabel('v [m/s]')
plt.ylabel('u')
plt.savefig(f'vu.png')
plt.show()
