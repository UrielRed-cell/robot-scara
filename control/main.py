from image_parser import ImgMeca
from pathlib import Path

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
