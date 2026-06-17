from image_parser import ImgMeca
from pathlib import Path
import pygame

BASE = Path(__file__).resolve().parent.parent

imagen = BASE / "furrul_negro.png"
# repl.py

def control_manual():

    pygame.init()

    pantalla = pygame.display.set_mode((400,400))
    pygame.display.set_caption("SCARA manual")

    x = 200
    y = 200

    velocidad = 0.2

    activo = True

    while activo:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                activo = False


        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_UP]:
            y -= velocidad

        if teclas[pygame.K_DOWN]:
            y += velocidad

        if teclas[pygame.K_LEFT]:
            x -= velocidad

        if teclas[pygame.K_RIGHT]:
            x += velocidad
        if teclas[pygame.K_SPACE]:
            color=RED


        pantalla.fill((30,30,30))


        pygame.draw.circle(
            pantalla,
            (255,255,255),
            (x,y),
            10
        )


        pygame.display.flip()


        # Aquí mandarías al Arduino
        print(
            f"MOVE X{x} Y{y}"
        )


    pygame.quit()



def cargar_imagen(tipo):

    ruta = input(
        "Ruta de imagen: "
    )


    robot = ImgMeca(
        200,
        200
    )


    if tipo == "png":

        robot.carga_img(
            ruta
        )

        robot.normaliza()
        robot.blanco_negro()
        robot.bordes()
        robot.vectoriza()
        robot.simplifica()


    elif tipo == "bmp":

        robot.carga_bmp(
            ruta
        )

        robot.vectoriza_sprite()


    robot.preview()



def repl():

    while True:

        print("""
======== SCARA ========

1) Imagen PNG/JPG
2) Sprite BMP
3) Control manual
4) Salir

=======================
""")

        opcion=input("> ")


        if opcion=="1":

            cargar_imagen("png")


        elif opcion=="2":

            cargar_imagen("bmp")


        elif opcion=="3":

            control_manual()


        elif opcion=="4":

            break


        else:

            print(
                "Opción inválida"
            )



if __name__=="__main__":
    repl()
