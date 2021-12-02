import math
import time


class Odometry:
    T, D, R = 0.143, 0.06, 1188.024

    def __init__(self, motor):

        self.motor = motor
        self.x, self.y, self.theta, self.time = 0, 0, 0, 0
        self.base = time.perf_counter_ns()
        self.e = self.motor.encoder()

    def update(self):

        pre_t, pre_e = self.time, self.e
        self.time = (time.perf_counter_ns() - self.base) / 1000000000
        self.e = self.motor.encoder()
        eR, eL = self.e[0] - pre_e[0], self.e[1] - pre_e[1]
        dR = eR / Odometry.R * Odometry.D * math.pi
        dL = eL / Odometry.R * Odometry.D * math.pi
        dt = self.time - pre_t
        dtheta = (dR - dL) / Odometry.T
        dN = (dR + dL) / 2
        dx = dN * math.cos(dtheta/2)
        dy = dN * math.sin(dtheta/2)
        self.x += math.cos(self.theta) * dx - math.sin(self.theta) * dy
        self.y += math.sin(self.theta) * dx + math.cos(self.theta) * dy
        self.theta += dtheta
        self.vR, self.vL, self.w = dR / dt, dL / dt, dtheta / dt
