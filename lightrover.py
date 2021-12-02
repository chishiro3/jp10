<<<<<<< HEAD
import vs_wrc201_i2c
import vs_wrc201_motor
import math, time, sys

MU8_O_EN = 0x10
MU8_TRIG = 0x11
MS16_FB_PG0 = 0x20 #PGain1
MS16_FB_PG1 = 0x22 #PGain2
=======
import math
import sys
import time

import vs_wrc201_i2c
import vs_wrc201_motor

MU8_O_EN = 0x10
MU8_TRIG = 0x11
MS16_FB_PG0 = 0x20  # PGain1
MS16_FB_PG1 = 0x22  # PGain2
>>>>>>> 3694e4a8d8238337ae93384a8943987c535604a9

MS32_A_POS0 = 0x48
MS32_A_POS1 = 0x4c

<<<<<<< HEAD
MS32_T_POS0 = 0x40
MS32_T_POS1 = 0x44

=======
>>>>>>> 3694e4a8d8238337ae93384a8943987c535604a9
MS16_T_OUT0 = 0x50
MS16_T_OUT1 = 0x52

MU16_FB_PCH0 = 0x30
MU16_FB_PCH1 = 0x32

<<<<<<< HEAD
MS32_M_POS0 = 0x60 #encoder1
MS32_M_POS1 = 0x64 #encoder2
=======
MS32_M_POS0 = 0x60  # encoder1
MS32_M_POS1 = 0x64  # encoder2
>>>>>>> 3694e4a8d8238337ae93384a8943987c535604a9

WHEEL_CIRCUMFERENCE = 60.0 * math.pi / 1000
ENC_COUNTS_PER_TURN = 1188.024
ENC_PER_M = ENC_COUNTS_PER_TURN / WHEEL_CIRCUMFERENCE
M_PER_ENC = WHEEL_CIRCUMFERENCE / ENC_COUNTS_PER_TURN

ROVER_D = 0.143/2.0

DIFF_COUNT_LIMIT = 1048575

<<<<<<< HEAD
class Motor:
  def __init__(self):
    self.controller = vs_wrc201_motor.VsWrc201Motor()
    self.open()

  def open(self):
    self.i2c = vs_wrc201_i2c.VsWrc201I2c(0x10)
    self.i2c.read_all()
    self.i2c.init_memmap(2.0)
    self.i2c.send_write_map()

    self.write_msg(MU8_O_EN, 0x00, 1, 'w')
    self.write_msg(MU8_TRIG, 0x0c, 1, 'w')
    self.write_msg(MS16_FB_PG0, 0x0080, 2, 'w')
    self.write_msg(MS16_FB_PG1, 0x0080, 2, 'w')
    self.write_msg(MU16_FB_PCH0, 0x09C4, 2, 'w')
    self.write_msg(MU16_FB_PCH1, 0x09C4, 2, 'w')
    self.write_msg(MU8_O_EN, 0x03, 1, 'w')
 
  def write_msg(self, addr, data, length, cmd):
    try:
      r = 0
      if cmd == 'w':
        if length == 4:
          self.i2c.write_4_byte(addr, data)
        elif length == 2:
          self.i2c.write_2_byte(addr, data)
        elif length == 1:
          self.i2c.write_1_byte(addr, data)
      elif cmd == 's':
        self.i2c.send_write_map()
      elif cmd == 'rm':
        self.i2c.read_all()
      elif cmd == 'r':
        self.i2c.read_memmap(addr, length)
        if length == 4:
          r = self.i2c.read_s32map(addr)
        elif length == 2:
          r = self.i2c.read_s16map(addr)
        elif length == 1:
          r = self.i2c.read_s8map(addr)
      return r
    except IOError:
      return None

  def to_int(self, x):
    return x if x < 2147483648 else x - 4294967296

  def encoder(self):
    to_int = lambda x: x if x < 2147483648 else x - 4294967296
    enc0 = self.write_msg(MS32_M_POS0, 0, 4, 'r')
    enc1 = self.write_msg(MS32_M_POS1, 0, 4, 'r')
    return [to_int(enc1), -to_int(enc0)]

  def target(self):
    to_int = lambda x: x if x < 2147483648 else x - 4294967296
    enc0 = self.write_msg(MS32_T_POS0, 0, 4, 'r')
    enc1 = self.write_msg(MS32_T_POS1, 0, 4, 'r')
    return [to_int(enc1), -to_int(enc0)]

  def reset(self):
    self.write_msg(MU8_TRIG, 0xC0, 1, 'w')

  def drive(self, uR, uL):
    uL = -uL
    self.write_msg(MS32_A_POS0, uL, 4, 'w')
    self.write_msg(MS32_A_POS1, uR, 4, 'w')
    self.write_msg(MU8_TRIG, 0x03, 1, 'w')

  def stop(self):
    self.write_msg(MU8_TRIG, 0x0c, 1, 'w')

  def drive2(self, r_speed, l_speed):
    l_speed = -l_speed
    self.write_msg(MS16_T_OUT0, l_speed, 2, 'w')
    self.write_msg(MS16_T_OUT1, r_speed, 2, 'w')

def main():
  target_linear_x = float(sys.argv[1])
  target_angular_z = math.radians(float(sys.argv[2]))
  target_v = [target_linear_x + ROVER_D * target_angular_z, target_linear_x - ROVER_D * target_angular_z]

  motor = Motor()

  start_t = time.perf_counter_ns()
  t = start_t
  e = motor.encoder()
  print(f'time:{t/1000000:.2f} e[0]:{e[0]} e[1]:{e[1]}')

  pos_x = 0
  pos_theta = 0
  linear_x = 0
  angular_z = 0
  for i in range(50):
    pre_e = e
    pre_t = t
    current_v = [linear_x + ROVER_D * angular_z, linear_x - ROVER_D * angular_z]
    #target_v = [0.1, 0.1]
    #target_v = [r, l]
    rl = motor.controller.pos_controll(current_v, target_v)
    #rl = [r, l]
    print(f'rl:{rl}')
    motor.drive(*rl)

    t = time.perf_counter_ns()
    e = motor.encoder()
    dt = (t - pre_t) / 1000000000
    d = [e[0] - pre_e[0], pre_e[1] - e[1]]
    d = [(-d[i] if abs(d[i]) < DIFF_COUNT_LIMIT else 0) for i in range(2)]
    m = [float(d[i]) * M_PER_ENC for i in range(2)]
    v = [m[i] / dt for i in range(2)]
    linear_x = (v[0] + v[1]) / 2
    angular_z = (v[1] - v[0]) / (2 * ROVER_D)
    pos_x += linear_x * dt
    pos_theta += angular_z * dt
    print(f'time:{(t-start_t)/1000000000:.2f} e:{e} d:{d} v:{v} linear_x:{linear_x} angular_z:{math.degrees(angular_z)} x:{pos_x} th:{math.degrees(pos_theta)}')
    time.sleep(0.05)


if __name__ == '__main__':
  main()

=======

class Motor:
    def __init__(self):
        self.controller = vs_wrc201_motor.VsWrc201Motor()
        self.open()

    def open(self):
        self.i2c = vs_wrc201_i2c.VsWrc201I2c(0x10)
        self.i2c.read_all()
        self.i2c.init_memmap(2.0)
        self.i2c.send_write_map()

        self.write_msg(MU8_O_EN, 0x00, 1, 'w')
        self.write_msg(MU8_TRIG, 0x0c, 1, 'w')
        self.write_msg(MS16_FB_PG0, 0x0080, 2, 'w')
        self.write_msg(MS16_FB_PG1, 0x0080, 2, 'w')
        self.write_msg(MU16_FB_PCH0, 0x09C4, 2, 'w')
        self.write_msg(MU16_FB_PCH1, 0x09C4, 2, 'w')
        self.write_msg(MU8_O_EN, 0x03, 1, 'w')

    def write_msg(self, addr, data, length, cmd):
        try:
            r = 0
            if cmd == 'w':
                if length == 4:
                    self.i2c.write_4_byte(addr, data)
                elif length == 2:
                    self.i2c.write_2_byte(addr, data)
                elif length == 1:
                    self.i2c.write_1_byte(addr, data)
            elif cmd == 's':
                self.i2c.send_write_map()
            elif cmd == 'rm':
                self.i2c.read_all()
            elif cmd == 'r':
                self.i2c.read_memmap(addr, length)
                if length == 4:
                    r = self.i2c.read_s32map(addr)
                elif length == 2:
                    r = self.i2c.read_s16map(addr)
                elif length == 1:
                    r = self.i2c.read_s8map(addr)
            return r
        except IOError:
            return None

    def to_int(self, x):
        return x if x < 2147483648 else x - 4294967296

    def encoder(self):
        def to_int(x): return x if x < 2147483648 else x - 4294967296
        enc0 = self.write_msg(MS32_M_POS0, 0, 4, 'r')
        enc1 = self.write_msg(MS32_M_POS1, 0, 4, 'r')
        return [to_int(enc0), to_int(enc1)]

    def drive(self, r_speed, l_speed):
        l_speed = -l_speed
        self.write_msg(MS32_A_POS0, l_speed, 4, 'w')
        self.write_msg(MS32_A_POS1, r_speed, 4, 'w')
        self.write_msg(MU8_TRIG, 0x03, 1, 'w')


def main():
    target_linear_x = float(sys.argv[1])
    target_angular_z = math.radians(float(sys.argv[2]))
    target_v = [target_linear_x + ROVER_D * target_angular_z,
                target_linear_x - ROVER_D * target_angular_z]

    motor = Motor()

    start_t = time.perf_counter_ns()
    t = start_t
    e = motor.encoder()
    print(f'time:{t/1000000:.2f} e[0]:{e[0]} e[1]:{e[1]}')

    pos_x = 0
    pos_theta = 0
    linear_x = 0
    angular_z = 0
    for i in range(50):
        pre_e = e
        pre_t = t
        current_v = [linear_x + ROVER_D * angular_z,
                     linear_x - ROVER_D * angular_z]
        #target_v = [0.1, 0.1]
        #target_v = [r, l]
        rl = motor.controller.pos_controll(current_v, target_v)
        #rl = [r, l]
        print(f'rl:{rl}')
        motor.drive(*rl)

        t = time.perf_counter_ns()
        e = motor.encoder()
        dt = (t - pre_t) / 1000000000
        d = [e[0] - pre_e[0], pre_e[1] - e[1]]
        d = [(-d[i] if abs(d[i]) < DIFF_COUNT_LIMIT else 0) for i in range(2)]
        m = [float(d[i]) * M_PER_ENC for i in range(2)]
        v = [m[i] / dt for i in range(2)]
        linear_x = (v[0] + v[1]) / 2
        angular_z = (v[1] - v[0]) / (2 * ROVER_D)
        pos_x += linear_x * dt
        pos_theta += angular_z * dt
        print(f'time:{(t-start_t)/1000000000:.2f} e:{e} d:{d} v:{v} linear_x:{linear_x} angular_z:{math.degrees(angular_z)} x:{pos_x} th:{math.degrees(pos_theta)}')
        time.sleep(0.05)


if __name__ == '__main__':
    main()
>>>>>>> 3694e4a8d8238337ae93384a8943987c535604a9
