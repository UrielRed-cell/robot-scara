from textual.app import App,ComposeResult
from textual.widgets import Footer,Header
from textual.containers import HorizontalGroup,VerticalGroup
from textual_canvas import Canvas,CanvasError
from textual.color import Color
from textual.widgets import Button,Label,Digits

class VerticalMenu(HorizontalGroup):
    def compose(self):
        yield Button("Rutina",id="rutina",variant="error")
        yield Button("Tiempo Real",id="t_real",variant="error")
        yield Label("Tiempo de ejecución",id="tiempo") 
        yield TimeDisplay()
    def on_button_pressed(self,event):
        button_id=event.button.id
        if button_id=="rutina":
            pass
        elif button_id=="t_real":
            pass

class TimeDisplay(Digits):
    def on_mount(self):
        self.update_timer=1

    def watch_time(self):
        self.update(f"{hours:02,0.f}:{minutes:02,0.f}:{seconds:05.2f}")


class HorizontalCanvas(HorizontalGroup):
    def on_mount(self):
        self.query_one(Canvas).clear()
        self.query_one(Canvas).draw_rectangle(2,2,26,26)

    def compose(self):
        yield Button("Reinicio",id="reinicio",variant="error")
        yield Canvas(30,30,Color(128,0,128),id="canva",pen_color=Color.parse("red"))
        yield Button("Reposo",id="reposo",variant="error")
    
    def reset(self):
        self.query_one(Canvas).clear()
        self.query_one(Canvas).draw_rectangle(2,2,26,26)
        self.query_one(Canvas).set_pixel(0,0)
    def on_button_pressed(self,event):
        button_id=event.button.id
        if button_id=="reinicio":
            self.reset()
            self.app.x=0
            self.app.y=0
        elif button_id=="reposo":
            pass

class FooterMenu(HorizontalGroup):
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y

    def compose(self):
        yield Label(f"Posición: ({self.x},{self.y})",id="position")

class ManualController(App):
    x,y=0,0
    #TODO Checar bidings
    #clave,accion,descripcion
    BINDINGS=[
            ("up","menu_up","arriba"),
            ("down","menu_down","abajo"),
            ("w","move_up","arriba"),
            ("a","move_left","izquierda"),
            ("s","move_down","abajo"),
            ("d","move_right","derecha")
              ]
    CSS="""FooterMenu {
    height: 3;
}

HorizontalCanvas {
    height: 35;
}"""
    def paint_pos(self):
        try:
            self.query_one("#canva").set_pixel(self.x,self.y,color=Color.parse("white"))
            self.query_one("#position").update(f"Posición: ({self.x},{self.y})")
            #TODO Arreglar
            self.query_one("#canva").set_pen(Color.parse("red"))
        except CanvasError:
            #TODO Agregar alerta
            pass
    def action_move_up(self):
        self.y-=1
        self.paint_pos()
    
    def action_move_down(self):
        self.y+=1
        self.paint_pos()

    def action_move_left(self):
        self.x-=1
        self.paint_pos()
    
    def action_move_right(self):
        self.x+=1
        self.paint_pos()

    def compose(self):
        yield VerticalGroup(VerticalMenu(),HorizontalCanvas(),FooterMenu(0,0))

    def on_mount(self):
        print(self.query_one("#position"))


