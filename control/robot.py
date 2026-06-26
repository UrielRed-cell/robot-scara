import serial

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
        # aquí tu modelo real SCARA
        theta1 = x * 0.5
        theta2 = y * 0.5
        return theta1, theta2

    def send_position(self, x, y):
        theta1, theta2 = self.inverse_kinematics(x, y)

        cmd = f"{theta1:.2f},{theta2:.2f}\n"

        if self.serial:
            self.serial.write(cmd.encode())
        else:
            print("NO SERIAL:", cmd)
