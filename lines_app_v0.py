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

from kivy.clock import Clock, mainthread
from functools import partial

import os
import re

from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

#THIS IS THE BUTTON PROGRESSION FILE.  YAY!

PLAY_LIST = ['miniScript.txt', 'smallerScript.txt','TEST','TEST','TEST','TEST','Test']

class Play(Button):
    pass

class Prompt(Button):
    pass

class Start(Button):
    pass

class Cues(CheckBox):
    pass

class Container(GridLayout):
    display = ObjectProperty()
    lengths = ObjectProperty()
    userChar = StringProperty()
    playName = StringProperty('None Selected')
    lineNum = NumericProperty()
    charLineNum = NumericProperty()
    charList = ListProperty()
    lineList = ListProperty()
    playList = ListProperty(PLAY_LIST)
    charmenu = DropDown()
    playMenu = DropDown()
    cuesMode = BooleanProperty(False)

    def play(self):


        Prompt.disabled = False

        def readLine():
            if not (self.charList[self.lineNum] == self.userChar):
                lineForSpeak = self.lineList[self.lineNum].replace("\'", "\\\'")
                os.system("say -v Alex" + lineForSpeak)
            self.lineNum += 1

        def setDisplay():
            print("Line Num is " + str(self.lineNum))
            if self.lineNum == 0:
                print('BEGINNING WAS ENTERED')
                self.display.text = 'You are at the beginning of the script.\nIf you have the first line, speak now.'
                if self.charList[0] == self.userChar: 
                    self.lineNum += 1
                    return
                else: 
                    self.charLineNum = -1
            if self.cuesMode: 
                if self.lineNum < (len(self.lineList) - 1):
                    print("lineNum = " + str(self.lineNum) + " and next character is " + self.charList[self.lineNum  + 1])
                    if self.charList[self.lineNum  + 1] == self.userChar and (not self.charList[self.lineNum] == self.userChar):
                        self.display.text = self.lineList[self.lineNum]
                        Clock.schedule_once(lambda dt: readLine(), 0.2) 
                        self.charLineNum = self.lineNum + 1
                    else:
                        print("Else was entered.")
                        while self.lineNum < (len(self.lineList) - 1):
                            print("In loop.")
                            self.lineNum += 1   
                            if self.lineNum == (len(self.lineList) - 1):
                                setDisplay()
                                break
                            if self.charList[self.lineNum + 1] == self.userChar:
                                setDisplay()
                                break
                else:
                    self.lineNum = 0
                    print('Back to beginning!')
                    self.display.text = 'You have reached the end of this script.\nClick \'Next Cue!\' to start again'           
                    self.charLineNum = -2
            else:
                if self.lineNum < len(self.lineList):
                    if self.charList[self.lineNum] == self.userChar:
                        self.display.text = 'Your  line!'    
                    else:
                        self.display.text = self.lineList[self.lineNum]
                    Clock.schedule_once(lambda dt: readLine(), 0.2)
                else:
                    self.lineNum = 0
                    self.display.text = 'You have reached the end of this script.\nClick Play to start again'

        setDisplay()

    def start(self):

        self.display.text = ''
        self.lineNum = 0
        self.charList.clear()
        self.lineList.clear()

        Play.disabled = False
        self.playName = 'None Selected'
        self.playMenu.clear_widgets()
        self.charmenu.clear_widgets()

        def selectPlay(selection):
            self.playName = selection
            print(self.playName)
            self.playMenu.dismiss()
            self.load()

        for play in self.playList:
            btn = Button(text=play, size_hint_y=None, height=44)
            btn.bind(on_press=lambda x:selectPlay(x.text))
            self.playMenu.add_widget(btn)

        scriptbutton = Button(text='Select Script to Rehearse', size_hint=(0.4, 0.1), pos_hint={ 'top' : 0.95, 'right' : 0.85})

        scriptbutton.bind(on_release=self.playMenu.open)

        self.playMenu.bind(on_select=lambda instance, x:selectPlay(x))
        
        runTouchApp(scriptbutton)

    def load(self):

        self.charList.clear() 
        
        fileObject = open(self.playName)
        
        for line in fileObject: 
            
            #Load to dict and keep line count for each character.  
            lineArray = line.split(":") 
            if len(lineArray) > 1:
                self.charList.append(lineArray[0])
                self.lineList.append(lineArray[1])

        cast = []
        for character in self.charList:
            if character not in cast:
                btn = Button(text=character, size_hint_y=None, height=44)

                # for each button, attach a callback that will call the select() method
                # on the dropdown. We'll pass the text of the button as the data of the
                # selection.
                btn.bind(on_release=lambda btn: self.charmenu.select(btn.text))

                # then add the button inside the dropdown
                self.charmenu.add_widget(btn)
                cast.append(character)
            
        mainbutton = Button(text='Select Your Character', size_hint=(0.4, 0.1), pos_hint={ 'top' : 0.95, 'right' : 0.85})

        def setUserChar(selection):
            setattr(mainbutton, 'text', selection)
            if selection == '':
                setattr(mainbutton, 'text', 'Select Your Character')
            self.userChar = selection

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        #mainbutton.bind(on_press=showMenu)
        mainbutton.bind(on_press=lambda x:setUserChar(''))
        mainbutton.bind(on_release=self.charmenu.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.charmenu.bind(on_select=lambda instance, x:setUserChar(x))
        
        runTouchApp(mainbutton)

        
    def on_checkbox_active(self, checked):
        if checked:
            print('The checkbox is active')
            self.cuesMode = True
        else:
            print('The checkbox is inactive')
            self.cuesMode = False

    def promptMe(self):
        if self.charLineNum == -1:
            self.display.text = 'You don\'t have the first line, so click \'Next Cue!\' to get started!'
        elif self.charLineNum == -2:
            self.display.text = 'You\'re at the end of the script!  Click \'Next Cue!\' to return to the beginning!'
        else:
            self.display.text = self.lineList[self.charLineNum]

class MainApp(App):

    def build(self):
        self.title = 'Awesome app!!!'
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
