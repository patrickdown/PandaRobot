from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock

Builder.load_string("""
<HighFiveScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Image:
            source: 'highfiveimage.jpg'
""")

class HighFiveScreen(Popup):

    def __init__(self, **kwargs):
        super(HighFiveScreen, self).__init__(**kwargs)
        self.title = "Way to go!"
        Clock.schedule_once(self.CloseScreen, 3)

    def CloseScreen(self, dt):
        self.dismiss()
    
showing_screen = False

def show_high_five():
    global showing_screen
    if showing_screen: return
    showing_screen = True
    scr = HighFiveScreen()
    scr.open()
    showing_screen = False
    
