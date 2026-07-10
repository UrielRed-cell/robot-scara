import serial
import struct
import math

class SCARARobot:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
        # Geometría del brazo
        self.L1 = 80
        self.L2 = 70
        self.max_reach = 150
        self.min_reach = 10  # 80 - 70 (El agujero negro)
        
        # --- EL TRUCO DEL OFFSET ---
        # 1. Escala: ¿Cuántos centímetros reales equivale 1 píxel?
        # Supongamos que quieres que tu dibujo de 46x49px mida unos 50cm reales.
        self.cm_per_pixel = 1.0 # Cambia esto si quieres el dibujo más grande o chico
        
        # 2. X Offset: Empujamos el lienzo hacia adelante (lejos del robot)
        # Lo ponemos a 40 cm adelante. Así nunca tocará la zona muerta de 10 cm.
        self.offset_x = 40.0 
        
        # 3. Y Offset: Centramos el lienzo frente al robot.
        # Si la altura es 49, la bajamos a la mitad para que el píxel Y=24.5 quede al centro (Y=0)
        self.offset_y = - (49 * self.cm_per_pixel) / 2.0 

    def transform_pixels_to_cm(self, pixel_x, pixel_y):
        # Matemáticas simples: Trasladar el origen de los píxeles a la nueva zona segura
        x_cm = self.offset_x + (pixel_x * self.cm_per_pixel)
        y_cm = self.offset_y + (pixel_y * self.cm_per_pixel)
        
        return x_cm, y_cm
    

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate)

    def disconnect(self):
        if self.serial:
            self.serial.close()
            self.serial = None

    def inverse_kinematics(self, pixel_x, pixel_y):
        # 1. Transformación a la "Caja Segura" (Workspace Integrado)
        # Forzamos la cuadrícula de 46x49 a existir en una zona donde el brazo SIEMPRE deba flexionar.
        escala_cm = 1.2  # Tamaño real de cada píxel (ajústalo si quieres el dibujo más grande o chico)
        
        # X: Empujamos el lienzo 50 cm adelante del robot. 
        # (Suficientemente lejos de la base, pero lejos del límite de 150cm)
        x = 50.0 + (pixel_x * escala_cm)
        
        # Y: Centramos el lienzo respecto a la base del robot (49 / 2 = 24.5)
        y = (pixel_y - 24.5) * escala_cm
        
        r2 = x**2 + y**2
        r = math.sqrt(r2)
        
        # 2. Protección contra Singularidad de Frontera
        # Limitamos 'r' a 148 cm como máximo para evitar que el brazo quede 100% rígido.
        if r > 148.0:
            r = 148.0
            r2 = r**2
            angle = math.atan2(y, x)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            
        elif r < 15.0:
            r = 15.0
            r2 = r**2
            angle = math.atan2(y, x) if (x != 0 or y != 0) else 0 
            x = r * math.cos(angle)
            y = r * math.sin(angle)

        # 3. Cinemática Inversa Pura
        cos_t2 = (r2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        cos_t2 = max(-1.0, min(1.0, cos_t2))
        
        postura_codo = 1  
        theta2_rad = math.acos(cos_t2) * postura_codo
        
        beta = math.atan2(y, x)
        alpha = math.atan2(self.L2 * math.sin(theta2_rad), self.L1 + self.L2 * math.cos(theta2_rad))
        
        theta1_rad = beta - alpha
        
        # 4. Mapeo a Hardware Físico (Servomotores)
        theta1_math = math.degrees(theta1_rad)
        theta2_math = math.degrees(theta2_rad)
        
        # Ajuste de fase para motores estándar (0 a 180 grados, donde 90° es el centro muerto)
        # Esto evita que el Arduino reciba valores negativos que rompen el movimiento.
        theta1_motor = theta1_math + 90.0
        theta2_motor = theta2_math + 90.0
        
        # Recorte de seguridad para no tronar los engranes físicos
        theta1_motor = max(0.0, min(180.0, theta1_motor))
        theta2_motor = max(0.0, min(180.0, theta2_motor))

        return theta1_motor, theta2_motor

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

        payload = struct.pack("<ffB", theta1, theta2,tool)

        length = len(payload)

        packet = struct.pack("<BBB", start, cmd, length) + payload
        if self.serial:
            self.serial.write(packet)
        else: 
            print("NO SERIAL: ",packet)
