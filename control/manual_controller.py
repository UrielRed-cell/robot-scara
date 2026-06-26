from textual.app import App,ComposeResult
from textual.widgets import Footer,Header
from textual.containers import HorizontalGroup,VerticalGroup
from textual_canvas import Canvas,CanvasError
from textual.color import Color
from textual.widgets import Button,Label,Digits,RadioButton,RadioSet,Footer,Static
from datetime import datetime,timedelta
from textual.reactive import reactive
from textual.binding import Binding
from textual.screen import Screen
from robot import SCARARobot

class VerticalMenu(HorizontalGroup):
    
    def on_mount(self)->None:
        #self.query_one(RadioSet).focus()
        self.query_one("#rutina").focus()
        self.query_one("#t_real").focus()
        self.query_one("#iniciar").disabled = True
        self.query_one("#parar").disabled = True

    def compose(self):
        with RadioSet(id="radio_set"):
            yield RadioButton("Rutina",id="rutina")
            yield RadioButton("Tiempo Real",id="t_real")
        yield Button("Iniciar",id="iniciar")
        #TODO Agregar un radiobutton flotante que sea un menu
        #Eliges si exportas o no.
        yield Button("Fin",id="parar")
        yield Label("Tiempo de ejecución",id="tiempo",classes="box") 
        yield TimeDisplay()

    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.query_one("#iniciar").disabled=False
        self.query_one("#parar").disabled=False
        
        if event.pressed.id=="rutina":
            self.app.mode="rutina"
        elif event.pressed.id=="t_real":
            self.app.mode="t_real"

    def on_button_pressed(self,event):
        button_id=event.button.id
        
        if button_id=="iniciar":
            if event.button.id=="iniciar":
                self.query_one(TimeDisplay).start()
                self.app.begin=True
        elif button_id=="parar":
            if event.button.id=="parar":
                self.query_one(TimeDisplay).stop()
                self.app.send_path()

    def action_next_widget(self):
        self.screen.focus_next()

    def action_previous_widget(self):
        self.screen.focus_previous()



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
        #self.query_one(Canvas).draw_rectangle(2,2,26,26)
        self.query_one(Canvas).can_focus=False
        self.query_one(Canvas).set_pixel(23,23,color=Color.parse("red"))
        
    def compose(self):
        yield Button("Reiniciar",id="reiniciar",variant="error")
        yield Canvas(width=50,height=50,canvas_color=Color(0,120,255),id="canva",pen_color=Color.parse("red"))
        yield Button("Reposo",id="reposo",variant="error")
    
    def reset(self):
        self.query_one(Canvas).clear()
        #self.query_one(Canvas).draw_rectangle(2,2,26,26)
        self.query_one(Canvas).set_pixel(23,23)

    def on_button_pressed(self,event):
        button_id=event.button.id
        if button_id=="reiniciar":
            #self.app.x=23
            #self.app.y=23
            #OJO esto es un paso por referencia
            self.query_one(Canvas).clear()
            self.app.path=set()
            self.app.redraw_canvas()
            timer = self.app.query_one(TimeDisplay)
            timer.reset()
        elif button_id=="reposo":
            self.app.x=23
            self.app.y=23
            self.reset()

class FooterMenu(HorizontalGroup):
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y
        #self.hrr=hrr

    def compose(self):
        yield Label(f"Posición: ({self.x},{self.y}) Herramienta: FUERA",id="position",classes="box")
        #yield Label(f"Estado de herramienta{self.hrr}",id="herramienta",classe="box")

class Popup(Screen):

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self):
        yield Static(self.message,id="msg")
        yield Button("OK", id="ok")

    def on_button_pressed(self, event):
        self.app.pop_screen()

class ManualController(App):
    rb=None
    x,y=23,23
    tool=False
    path=set()
    mode=None
    begin=False
    scara_x_range=10
    scara_y_range=10
    last_sent=None
    #TODO Checar bidings
    #clave,accion,descripcion
    BINDINGS:list[Binding]=[
        Binding("p" ,"tool","dibujar",show=True),
        Binding("tab","cambia","cambia",show=True),
        Binding("enter", "activar", "activar",show=True),
        Binding("w","move_up","arriba",show=True),
        Binding("a","move_left","izquierda",show=True),
        Binding("s","move_down","abajo",show=True),
        Binding("d","move_right","derecha",show=True)
              ]
    CSS_PATH = "styles.tcss"
    
    def paint_pos(self):
        if not self.begin:
            return
        try:
            if self.tool:
                #self.query_one("#canva").set_pixel(self.x,self.y,color=Color.parse("white"))
                self.path.add((self.x,self.y))
                if self.mode=="t_real":
                    self.send_pos()
            self.redraw_canvas()
            self.query_one("#position").update(f"Posición: ({self.x},{self.y}) Herramienta: {'LISTA' if self.tool else 'FUERA'}")
            #TODO Arreglar
            #self.query_one("#canva").set_pen(Color.parse("red"))
        except CanvasError:
            #TODO Agregar alerta
            pass

    def redraw_canvas(self):
        canvas = self.query_one("#canva")

        canvas.clear()

        # Dibujar todos los trazos guardados
        for x, y in self.path:
            canvas.set_pixel(x,y,color=Color.parse("white"))

        # Dibujar cursor actual
        canvas.set_pixel(self.x,self.y,color=Color.parse("red"))
#No se ocupa
    def move_cursor(self, dx, dy):
        # borrar cursor viejo
        self.canvas.set_pixel(self.x,self.y,color=self.background_color)

        self.x += dx
        self.y += dy

        # dejar trazo si está activo
        if self.drawing:
            self.canvas.set_pixel(self.x,self.y,color=Color.parse("white"))

        # dibujar cursor
        self.canvas.set_pixel(self.x,self.y,color=Color.parse("red"))
    
    def update_tool(self):
        pass
        #self.query_one("#herramienta").update(f"Herramienta: {self.tool}")

    def action_move_up(self):
        if not self.begin:
            return
        self.y = max(0, self.y-1)
        self.paint_pos()
    
    def action_move_down(self):
        if not self.begin:
            return
        self.y = min(49, self.y+1)
        self.paint_pos()

    def action_move_left(self):
        if not self.begin:
            return
        self.x = max(0, self.x-1)
        self.paint_pos()
    
    def action_move_right(self):
        if not self.begin:
            return
        self.x = min(46, self.x+1)
        self.paint_pos()

    def action_tool(self):
        self.tool=not self.tool
        self.paint_pos()
    #def action_tool(self):
    #    self.tool=!self.tool
    #   self.update_tool()
#    def action_next_widget(self):
#        self.focus_index += 1

#        if self.focus_index >= len(self.menu_widgets):
#            self.focus_index = 0

#        self.menu_widgets[self.focus_index].focus()


#    def action_previous_widget(self):
#        self.focus_index -= 1

#       if self.focus_index < 0:
#            self.focus_index = len(self.menu_widgets)-1

#       self.menu_widgets[self.focus_index].focus()

    def action_activate(self):
        if self.focused:
            self.focused.press()

    def compose(self):
        yield VerticalGroup(VerticalMenu(),HorizontalCanvas(),FooterMenu(23,23))
        yield Footer()

    def on_mount(self):    
        #TODO BORRAR 
        self.focus_index = 0

        self.menu_widgets=[
                self.query_one("#rutina"),
                self.query_one("#t_real"),
                self.query_one("#iniciar"),
                self.query_one("#parar"),
                self.query_one("#reposo"),
                ]
        #print(self.query_one("#position"))
        #rb=SCARARobot()

    def show_popup(self, text: str):
        self.push_screen(Popup(text))

    def on_button_pressed(self, event):
        if event.button.id == "parar":
            self.show_popup("Exportado con éxito ✅")
    
        if event.button.id == "iniciar":
            try:
                rb=SCARARobot()
                self.show_popup("Conexión en vivo 🔴")
            except e:
                self.show_popup("Error en conexión 🔴")
#    def on_key(self, event):
#        if isinstance(self.focused, RadioSet):
#            if event.key in ("left", "right"):
#                event.stop()
#                self.action_next_widget()

            #elif event.key in ("up", "left"):
                #event.stop()
                #self.action_previous_widget()
    def canvas_to_scara(self, x, y):
        xmin, xmax = self.scara_x_range
        ymin, ymax = self.scara_y_range

        xs = (x / 46) * (xmax - xmin) + xmin
        ys = (y / 49) * (ymax - ymin) + ymin

        return xs, ys
    
    def send_pos(self):
        xs,ys=self.canva_to_scara(self.x,self.y)
        if self.last_sent!=(xs,ys):
            self.rb.send_position(xs,ys)
            self.last_sent=(xs,ys)

            pass
            
        #con=rb.conection()


    
    def send_path(self):
        for x,y in self.path:
            xs,ys=self.canvas_to_scara(x,y)
            self.robot.send_position(xs,ys)
