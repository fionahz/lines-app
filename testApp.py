import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
ListProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition 

#Global Constant with all properly formatted scripts
PLAY_LIST = ['Mini Script', 'Smaller Script','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click', \
'Test Button - Do Not Click','Test Button - Do Not Click']

class MenuScreen(Screen):
    pass

class RehearseScreen(Screen):
    pass

class TestApp(App):

    userChar = StringProperty()
    playName = StringProperty('None Selected')
    
    lineNum = NumericProperty()
    charLineNum = NumericProperty()
    
    charList = ListProperty()
    lineList = ListProperty()
    
    cuesMode = BooleanProperty(False)

    def charSelect(self, screens):
        
        charMenu = screens.current_screen.ids.charMenu
        charMenu.clear_widgets()
        cast = []

        for character in self.charList:
            if character not in cast:
                btn = Button(text=character, size_hint_y=None, height=44)

                btn.bind(on_release=lambda btn: charMenu.select(btn.text))

                charMenu.add_widget(btn)
                cast.append(character)
        
        charButton = screens.current_screen.ids.charButton 

        def setUserChar(selection):
            setattr(charButton, 'text', selection)
            if selection == '':
                setattr(charButton, 'text', 'Character')
            self.userChar = selection

        charButton.bind(on_press=lambda x:setUserChar(''))

        charMenu.bind(on_select=lambda instance, x:setUserChar(x))

    def build(self):

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RehearseScreen(name='rehearse'))
        sm.transition = NoTransition(duration=0)

        def selectPlay(selection):

            print('play selected')

            self.charList = []
            self.lineList = []
            sm.current = 'rehearse'
            result =  "".join(selection.split(" ")).lower()
            self.playName = result + ".txt"

            fileObject = open(self.playName)
            
            for line in fileObject: 
                
                #Load to dict and keep line count for each character.  
                lineArray = line.split(":") 
                if len(lineArray) > 1:
                    self.charList.append(lineArray[0])
                    self.lineList.append(lineArray[1])

            print(self.charList)
            
            self.charSelect(sm)

        playMenu = sm.current_screen.ids.playMenu
        playMenu.bind(minimum_height=playMenu.setter('height'))
        for i in range(len(PLAY_LIST)):
            btn = Button(text=PLAY_LIST[i], font_size=30, size_hint=(1, None))
            if btn.text == 'Test Button - Do Not Click':
                btn.background_color = [1, 0, 0, 1]
            btn.bind(on_release=lambda x:selectPlay(x.text))
            playMenu.add_widget(btn)

        return sm
    

if __name__ == '__main__':
    TestApp().run()