import serial
import struct
import math

class SCARARobot:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate)

    def disconnect(self):
        if self.serial:
            self.serial.close()
            self.serial = None

    def inverse_kinematics(self, x, y):
            L1 = self.L1
            L2 = self.L2

            # distancia al punto
            r2 = x**2 + y**2

            # cos(theta2)
            cos_t2 = (r2 - L1**2 - L2**2) / (2 * L1 * L2)

            # seguridad numérica
            cos_t2 = max(-1.0, min(1.0, cos_t2))

            theta2 = math.acos(cos_t2)

            # theta1
            k1 = L1 + L2 * math.cos(theta2)
            k2 = L2 * math.sin(theta2)

            theta1 = math.atan2(y, x) - math.atan2(k2, k1)

            return theta1, theta2

    def send_position(self, x, y):

        theta1, theta2 = self.inverse_kinematics(x, y)
        payload = struct.pack("<ff", theta1, theta2)  # 2 floats

        cmd = 0x01
        start = 0x02
        length = len(payload)

        packet = struct.pack("<BBB", start, cmd, length) + payload

        if self.serial:
            self.serial.write(packet)
        else:
            print("NO SERIAL:", packet)

    def send_angles(self,theta1, theta2,tool):
        start = 0x02
        cmd = 0x01

        payload = struct.pack("<ff", theta1, theta2,tool)
        length = len(payload)

        packet = struct.pack("<BBB", start, cmd, length) + payload

        self.serial.write(packet)
