import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImgMeca():
    
    def __init__(self,largo,ancho):
        #LARGO y ANCHO del ESAPCIO DE TRABAJO EdT
        self.LARGO=largo
        self.ANCHO=ancho
        self.img=None
        self.gris=None
        self.vectores=None
        self.vector=None
        self.trayectoria=None
    
    def carga_img(self,ruta):
        self.img=cv2.imread(ruta)
        if self.img is None:
            raise FileNotFoundError(ruta)
        self.cargada=True
    
    def normaliza(self):
        if not self.cargada:
            raise Exception("Imagen no cargada")
        l,a,_=self.img.shape
        escala=min(self.ANCHO,a,self.LARGO/l)
        self.img=cv2.resize(self.img,(
            int(a*escala),
            int(l*escala),
            )
        )
    
    def blanco_negro(self):
        self.gris=cv2.cvtColor(self.img,
                               cv2.COLOR_BGR2GRAY
                               )
    
    def bordes(self):
        _, self.bordes = cv2.threshold(
        self.gris,
        180,
        255,
        cv2.THRESH_BINARY_INV
    )
    def adelgazar(self):

        self.edge_img = cv2.ximgproc.thinning(
            self.edge_img
        )
    def pixel_a_mm(self,x,y):
        l,a=self.img.shape[:2]
        X=x*self.ANCHO/a
        Y=y*self.LARGO/l
        return (float(X),float(Y))

    def vectoriza(self):
        contornos,_ = cv2.findContours(
            self.bordes,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_NONE
        )

        self.vector=[]


        for c in contornos:

            area = cv2.contourArea(c)

            if area < 50:
                continue


            linea=[]

            for punto in c:

                x,y = punto[0]

                linea.append(
                    self.pixel_a_mm(x,y)
                )

            self.vector.append(linea)

    def relleno_morfologico(self):

        kernel = np.ones((3,3), np.uint8)

        self.gris = cv2.morphologyEx(
            self.gris,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=2
        )

    def simplifica(self, tolerancia=2):

        nuevo_vector=[]

        for contorno in self.vector:

            puntos = np.array(contorno, dtype=np.float32)

            aprox = cv2.approxPolyDP(
                puntos,
                tolerancia,
                False
            )

            linea=[]

            for punto in aprox:
                x,y = punto[0]
                linea.append(
                    (float(x),float(y))
                )

            nuevo_vector.append(linea)


        self.vector = nuevo_vector

    def preview(self):

        plt.figure()

        for linea in self.vector:

            x=[]
            y=[]

            for p in linea:
                x.append(p[0])
                y.append(p[1])

            plt.plot(x,y)


        plt.gca().invert_yaxis()
        plt.axis("equal")
        plt.show()

    def genera_trayectoria(self):

        self.trayectoria=[]


        for linea in self.vector:

            if len(linea)==0:
                continue


            inicio=linea[0]


            self.trayectoria.append(
                ("LAPIZ ARRIBA",inicio)
            )


            self.trayectoria.append(
                ("LAPIZ ABAJO",inicio)
            )


            for punto in linea[1:]:

                self.trayectoria.append(
                    ("MUEVE",punto)
                )


            self.trayectoria.append(
                ("LAPIZ ARRIBA",linea[-1])
            )
