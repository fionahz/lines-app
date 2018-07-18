import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

#Global Constant with all properly formatted scripts
PLAY_LIST = ['miniScript.txt', 'smallerScript.txt','TEST1','TEST2','TEST3','TEST4','TEST5','TEST6','TEST7','TEST8','TEST9','TEST10','TEST11','TEST12','TEST13','TEST14','TEST15','TEST16','TEST17','TEST18','TEST19','TEST20','TEST21','TEST22','TEST23','TEST24','TEST25']

class HomeScreen(BoxLayout):
    pass

class TestApp(App):
    #playMenu = ObjectProperty()
    #playMenu.minimum_height = playMenu.setter('height')
    def build(self):
        self.root = HomeScreen()
        playMenu = self.root.ids.playMenu
        playMenu.bind(minimum_height=playMenu.setter('height'))
        for i in range(len(PLAY_LIST)):
            btn = Button(text=PLAY_LIST[i], font_size=30, size_hint=(1, None))
            playMenu.add_widget(btn)

        return self.root

if __name__ == '__main__':
    TestApp().run()