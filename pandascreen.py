from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from takepicture import take_picture
from highfive import poll_high_five, sampling_rate
from highfivescreen import show_high_five
import time

ser = None
try:
    import serial
    ser = serial.Serial('/dev/ttyACM1', 9600)
except ImportError:
    pass


def Smile():
    ser.write("1")

def Frown():
    ser.write("2")


Builder.load_string("""

<ImageButton@Button>:
    source: None
    background_normal: 'button_normal.png'
    background_down: 'button_down.png'
    border: 30,30,30,30

    Image:
        source: root.source
        center: root.center

<InfoLabel@Label>:
    valign: 'middle'
    color: 0,0,0,1
    font_size: 25

<PandaScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            size_hint: 1, None
            height: 200
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            ImageButton:
                source: "heart-icon-3346-96px.png"
                on_press: root.DoHeart()
            ImageButton:
                source: "smiley-icon-5.png"
                on_press: root.DoSmile()
            ImageButton:
                source: "camera-icon-42-96px.png"
                on_press: root.DoCamera()

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        InfoLabel:
            size_hint: 1, None
            text: "High fives: " + str(root.high_fives)
""")

class PandaScreen(FloatLayout):
    high_fives = NumericProperty(0)

    def __init__(self, **kwargs):
        super(PandaScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.CheckHighFive, 1.0/sampling_rate)

    def CheckHighFive(self, dt):
        new_count = poll_high_five()
        if new_count > self.high_fives:
            show_high_five()
            self.high_fives = new_count

    def DoHeart(self):
        show_high_five()
        print("Heart Pressed")

    def DoSmile(self):
        Smile()
        print("Smile Pressed")

    def DoCamera(self):
        take_picture()
        print("Camera Pressed")


class ButtonsApp(App):

    def build(self):
        return PandaScreen()

def PollHighFive(dt):
    pass

if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    ButtonsApp().run()

