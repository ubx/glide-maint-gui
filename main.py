from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import subprocess

Builder.load_file('main.kv')


class MainScreen(Screen):
    pass

class CanMonitorScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='menu'))
sm.add_widget(CanMonitorScreen(name='canmonitor'))

class UIApp(App):
    run_xcsoar = ["/home/andreas/ClionProjects/XCSoar/output/UNIX/bin/xcsoar", "-fly", "-profile=default.prf"]
    def build(self):
        return sm

    def doit(self):
        subprocess.call(self.run_xcsoar)


if __name__ == "__main__":
    UIApp().run()
