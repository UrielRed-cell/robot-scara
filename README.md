
# Robot SCARA Pintor

Robot SCARA diseñado para dibujar sobre papel utilizando servomotores SG90 y piezas impresas en 3D.

## Descripción

Este proyecto consiste en el diseño y construcción de un brazo robótico tipo SCARA capaz de mover un marcador o bolígrafo sobre una hoja de papel para realizar dibujos simples.

El objetivo principal es servir como plataforma de aprendizaje para diseño mecánico, modelado CAD, impresión 3D y robótica básica.

## Características

* Arquitectura SCARA.
* Accionamiento mediante servomotores SG90.
* Piezas diseñadas en FreeCAD.
* Componentes imprimibles en 3D.
* Soporte para bolígrafo o marcador.
* Diseño modular y fácil de modificar.

## Programa 
El control del robot se dividira en dos partes
* Control de **bajo** nivel
* Control de **alto** nivel
En el caso de alto nivel se cuenta con la carpeta control en la cual se encuentran:
_image-parser_ y _main_
la forma de uso de _image-parser_ es:
```
BASE = Path(__file__).resolve().parent.parent

imagen = BASE / "furrul_prueba.png"
print(BASE)
print(imagen)
print(imagen.exists())
rbs=ImgMeca(200,200)

rbs.carga_img(imagen)
rbs.normaliza()
rbs.blanco_negro()
rbs.bordes()
rbs.vectoriza()
#print(rbs.vector)
print(len(rbs.vector))
```
Estos trazos seran enviados a _com-serial_ para finalmente llegar al mcu

***EMBEBIDO*** 
Para la comunicación se usara la plataforma laso que permitira una comunicación efectiva entre un mcu y una computadora

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

## Autor

Uriel

## LICENSE
The MIT License applies to all files in this repository,
including source code, PCB designs, CAD models and documentation,
unless otherwise specified.
