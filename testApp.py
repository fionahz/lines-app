import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition 

#Global Constant with all properly formatted scripts
PLAY_LIST = ['Mini Script', 'Smaller Script','This Is A Test Title','TEST2','TEST3','TEST4','TEST5','TEST6','TEST7','TEST8','TEST9','TEST10','TEST11','TEST12','TEST13','TEST14','TEST15','TEST16','TEST17','TEST18','TEST19','TEST20','TEST21','TEST22','TEST23','TEST24','TEST25']

class MenuScreen(Screen):
    pass

class RehearseScreen(Screen):
    pass

class TestApp(App):

    playName = StringProperty()
    userChar = StringProperty()
    playName = StringProperty('None Selected')
    lineNum = NumericProperty()
    charLineNum = NumericProperty()
    charList = ListProperty()
    lineList = ListProperty()
    playList = ListProperty(PLAY_LIST)
    cuesMode = BooleanProperty(False)

    def build(self):

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RehearseScreen(name='rehearse'))
        #sm.transition = NoTransition(duration=0)

        def selectPlay(selection):
            print(sm.screen_names)
            sm.current = 'rehearse'
            print(sm.current)
            result =  "".join(selection.split(" ")).lower()
            self.playName = result + ".txt"
            print(self.playName)

            print('load Button pressed')
            fileObject = open(self.playName)
            
            for line in fileObject: 
                
                #Load to dict and keep line count for each character.  
                lineArray = line.split(":") 
                if len(lineArray) > 1:
                    self.charList.append(lineArray[0])
                    self.lineList.append(lineArray[1])
        
            print(self.charList)
            print(self.lineList)

        print(sm.current_screen.ids)
        playMenu = sm.current_screen.ids.playMenu
        playMenu.bind(minimum_height=playMenu.setter('height'))
        for i in range(len(PLAY_LIST)):
            btn = Button(text=PLAY_LIST[i], font_size=30, size_hint=(1, None))
            btn.bind(on_release=lambda x:selectPlay(x.text))
            playMenu.add_widget(btn)

        return sm
    

if __name__ == '__main__':
    TestApp().run()