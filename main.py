from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import Clock, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse, Line
from kivy.metrics import dp
import random
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

class FirstPage(Screen):
    the_random = ObjectProperty(None)
    slid = ObjectProperty(None)
    togglik = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed_x_where = random.choice([1, -1])
        self.speed_y_where = random.choice([1, -1])

        # Window.minimum_width = 500
        # Window.minimum_height = 300
        # Window.maximum_width = 600
        # Window.maximum_height = 400

        self.sound = SoundLoader.load("sounds/pink.mp3")
        self.sound.volume += 0.9

        Clock.schedule_interval(self.update, 0.001)
        self.num = 0
    
    def on_size(self, *kwargs):
        print(self.size)

    def update(self, dt):
        self.speed_x = dp(self.speed_x_where * int(self.slid.value))
        self.speed_y = dp(self.speed_y_where * int(self.slid.value))
        x, y = self.the_random.el.pos
        w, h = self.the_random.el.size
        self.sound_yes_no = False

        if x + self.speed_x <= 0:
            x = 0
            self.speed_x_where = self.speed_x_where * -1
            self.sound_yes_no = True
        elif x + self.speed_x + w >= int(self.the_random.width):
            x = int(self.the_random.width - w)
            self.speed_x_where = self.speed_x_where * -1
            self.sound_yes_no = True
        else:
            x += self.speed_x
        
        if y + self.speed_y <= 0:
            y = 0
            self.speed_y_where = self.speed_y_where * -1
            self.sound_yes_no = True
        elif int(y + self.speed_y + h) >= int(self.the_random.height):
            y = int(self.the_random.height - h)
            self.speed_y_where = self.speed_y_where * -1
            self.sound_yes_no = True
        else:
            y += self.speed_y
            
        
        self.the_random.el.pos = x, y

        if self.num == 0:
            self.num = 1

        elif self.sound_yes_no and self.togglik.state == "normal" and int(self.slid.value) != 0:
            self.sound.play()
    
    def restart(self):
        self.slid.value = 0
        xel, yel = self.the_random.el.size
        self.the_random.el.pos = random.randint(5, int(self.the_random.width - xel - 5)), random.randint(5, int(self.the_random.height - yel - 5))
        x, y = self.the_random.el.pos

    def new_side(self):
        self.manager.transition = SlideTransition(direction="right")
        self.slid.value = 0
        self.manager.current = "second"

class Random(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(0, .3, .7)
            self.rec = Rectangle(pos = self.pos, size = self.size)

            self.el_color = Color(1, 1, 1)
            self.el = Ellipse(size= (dp(50), dp(50)), pos = (self.width/2 - dp(25) , self.height/2 - dp(25)))
            self.num = 0
        
        self.ball_colors = [(1, 1, 1, 1), (0, 1, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1), (0.5, 0, 0.5, 1), (1, 0.5, 0, 1), (1, 0, 1, 1), (1, 1, 0, 1)]
        self.the_color = (1, 1, 1, 1)
        self.next_color = (1, 1, 1, 1)

    def on_size(self, *kwargs):
        self.el.size = dp(50), dp(50)
        x, y = self.el.size
        self.rec.size = self.size
        self.rec.pos = self.pos
        w, h = self.size
        if self.num == 0:
            self.num = 1
        elif self.num == 1:
            self.el.pos = (random.randint(5, int(w - x - 5)), random.randint(5, int(h - y - 5)))
            self.num = 2
        else:
            self.el.pos = (self.width/2 - dp(25) , self.height/2 - dp(25))
    
    def on_touch_down(self, touch):
        w, h = self.el.size
        x, y = self.el.pos
        if touch.x >= x and touch.x <= x + w and touch.y >= y and touch.y <= y + h:
            # change color of ellipse
            # self.el.canvas.before.clear()  # Clear previous color instruction
            while self.next_color == self.the_color:
                self.next_color = random.choice(self.ball_colors)
            self.the_color = self.next_color
            with self.canvas.before:
                self.el_color.rgba = self.the_color

class SecondPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def new_side(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "ball"

class Random2(Widget):
    width_of_line = ObjectProperty(None)
    name_color = StringProperty("white")
    button_name_id = ObjectProperty(None)
    toggle_button = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_line = None
        self.num = 0
        self.line_colors = [(1, 1, 1, 1), (0, 1, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1), (1, 0.5, 0, 1), (1, 0, 1, 1), (1, 1, 0, 1), (0.4, 0.2, 0.0, 1)]
        self.the_line_color = (1, 1, 1, 1)
        self.names_of_colors = ["white", "Cyan", "Green", "Red", "Orange", "Magenta", "Yellow", "Brown"]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.x <= self.width and touch.y <= self.height - dp(int(self.width_of_line.value)):
            with self.canvas:
                Color(rgba=self.the_line_color)
                self.current_line = Line(points=(touch.x, touch.y), width=dp(int(self.width_of_line.value)))
                self.canvas.add(self.current_line)
        else:
            self.current_line = None
    
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and self.current_line and touch.x <= self.width and touch.y <= self.height - dp(int(self.width_of_line.value)):
            self.current_line.points += [touch.x, touch.y]
    
    def change_color(self):
        self.num += 1
        if self.num > len(self.line_colors) - 1:
            self.num = 0
        self.the_line_color = self.line_colors[self.num]
        self.name_color = self.names_of_colors[self.line_colors.index(self.the_line_color)]
        self.button_name_id.color = self.the_line_color
        self.toggle_button.state = "normal"
    
    def clear(self):
        self.canvas.clear()

    def on_size(self, *kwargs):
        self.canvas.clear()
    
    def rubber_cleaner(self, widget):
        if widget.state == "down":
            self.the_line_color = (0, 0, 0, 1)
        else:
            self.the_line_color = self.line_colors[self.num]



class OwnApp(App):
    def build(self):

        self.sm = ScreenManager()

        self.ball_screen = FirstPage(name="ball")
        self.second_screen = SecondPage(name="second")

        for one in [self.ball_screen, self.second_screen]:
            self.sm.add_widget(one)


        return self.sm

if __name__ == "__main__":
    OwnApp().run()