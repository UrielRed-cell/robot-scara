from image_parser import ImgMeca
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

imagen = BASE / "furrul_negro.png"
print(BASE)
print(imagen)
print(imagen.exists())
rbs=ImgMeca(200,200)

rbs.carga_img(imagen)
rbs.normaliza()
rbs.blanco_negro()
rbs.relleno_morfologico()
rbs.bordes()
rbs.vectoriza()
#print(rbs.vector)
print(len(rbs.vector))
rbs.simplifica(1.2)
rbs.preview()
