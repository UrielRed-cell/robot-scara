from textual.app import App,ComposeResult
from textual.widgets import Footer,Header
from textual.containers import HorizontalGroup,VerticalGroup
from textual_canvas import Canvas,CanvasError
from textual.color import Color
from textual.widgets import Button,Label,Digits,RadioButton,RadioSet
from datetime import datetime,timedelta
from textual.reactive import reactive

class VerticalMenu(HorizontalGroup):
    def on_mount(self)->None:
        #self.query_one(RadioSet).focus()
        self.query_one("#rutina").focus()
        self.query_one("#t_real").focus()
        self.query_one("#iniciar").disabled = True
        self.query_one("#parar").disabled = True

    def compose(self):
        with RadioSet(id="focus_me"):
            yield RadioButton("Rutina",id="rutina")
            yield RadioButton("Tiempo Real",id="t_real")
        yield Button("Iniciar",id="iniciar")
        #TODO Agregar un radiobutton flotante que sea un menu
        #Eliges si exportas o no.
        yield Button("Parar",id="parar")
        yield Label("Tiempo de ejecución",id="tiempo") 
        yield TimeDisplay()

    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.query_one("#iniciar").disabled=False
        self.query_one("#parar").disabled=False
        
        if event.pressed.id=="rutina":
            pass
        elif event.pressed.id=="t_real":
            pass

    def on_button_pressed(self,event):
        button_id=event.button.id
        
        if button_id=="iniciar":
            if event.button.id=="iniciar":
                self.query_one(TimeDisplay).start()
        elif button_id=="parar":
            if event.button.id=="parar":
                self.query_one(TimeDisplay).stop()

class TimeDisplay(Digits):
    time=reactive(0)

    def on_mount(self):
        self.timer=None

    def start(self):
        self.timer=self.set_interval(1,self.tick)
    
    def tick(self):
        self.time+=1

    def watch_time(self,value):
        minutes=value//60
        seconds=value%60
        self.update(f"{minutes:02}:{seconds:02}")
    
    def stop(self):
        if self.timer:
            self.timer.pause()

    def reset(self):
       self.time=0 

class HorizontalCanvas(HorizontalGroup):
    def on_mount(self):
        self.query_one(Canvas).clear()
        self.query_one(Canvas).draw_rectangle(2,2,26,26)

    def compose(self):
        yield Button("Reiniciar",id="reiniciar",variant="error")
        yield Canvas(30,30,Color(128,0,128),id="canva",pen_color=Color.parse("red"))
        yield Button("Reposo",id="reposo",variant="error")
    
    def reset(self):
        self.query_one(Canvas).clear()
        self.query_one(Canvas).draw_rectangle(2,2,26,26)
        self.query_one(Canvas).set_pixel(0,0)

    def on_button_pressed(self,event):
        button_id=event.button.id
        if button_id=="reiniciar":
            self.reset()
            self.app.x=0
            self.app.y=0
            #OJO esto es un paso por referencia
            timer = self.app.query_one(TimeDisplay)
            timer.reset()
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


