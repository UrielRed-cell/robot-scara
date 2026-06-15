import cv2

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
        self.bordes=cv2.Canny(self.gris,50,150)
    
    def pixel_a_mm(self,x,y):
        l,a=self.img.shape[:2]
        X=x*self.ANCHO/a
        Y=y*self.LARGO/l
        return (float(X),float(Y))

    def vectoriza(self):
        contornos,_=cv2.findContours(
                self.bordes,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE
                    )
        self.vector=[]
        for c in contornos:
            linea=[]
            for punto in c:
                x,y=punto[0]
                linea.append(
                            self.pixel_a_mm(x,y)
                        )
            self.vector.append(linea)

