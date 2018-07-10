# UI focused version of v0
import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.clock import Clock, mainthread

import os

from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

#Global Constant with all properly formatted scripts
PLAY_LIST = ['miniScript.txt', 'smallerScript.txt','TEST1','TEST2','TEST3','TEST4','TEST5','TEST6','TEST7','TEST8','TEST9','TEST10','TEST11','TEST12','TEST13','TEST14','TEST15','TEST16','TEST17','TEST18','TEST19','TEST20','TEST21','TEST22','TEST23','TEST24','TEST25']
#PLAY_LIST = ['miniScript.txt', 'smallerScript.txt','TEST1']

# class Gears(Button):
#     pass

# class Info(Button):
#     pass

class Container(GridLayout): 
    header = BoxLayout(orientation='horizontal')
    windowManager = BoxLayout(orientation='vertical')
    
    def showInfo(self):
        print('Info requested')
    
    def showGears(self):
        print('Settings shown')

    print('Working?')

    appName = Label(text='L I N E S')
    instructions = Label(text='Click on the play you want to rehearse!')

    # playMenu = ScrollView(size_hint=(1, None))
    # playList = GridLayout(cols=1, size_hint_y=None)
    # playList.bind(minimum_height=playList.setter('height')) 

    # for i in range(len(PLAY_LIST)):
    #         btn = Button(text=PLAY_LIST[i], size_hint_y=None, height=80, font_size=40)
    #         playList.add_widget(btn)

    # playMenu.add_widget(playList)

    gears = Button(background_normal='settings.png')
    info = Button(text='i')

    header.add_widget(gears)
    header.add_widget(appName)
    header.add_widget(info)
    windowManager.add_widget(header)
    windowManager.add_widget(instructions)
    #windowManager.add_widget(playMenu)

    #runTouchApp(playMenu)

class MainviApp(App):

    def build(self):
        self.title = 'Awesome app!!!'
        return Container()


if __name__ == "__main__":
    app = MainviApp()
    app.run()
