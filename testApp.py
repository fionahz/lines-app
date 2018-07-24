import kivy
kivy.require('1.10.1')

# Working prototype of LINE! app

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
from kivy.clock import Clock, mainthread

import os

# Global Constant with all properly formatted scripts
#
# At this stage of development, contains test strings 
# to demonstrate the scrolling capability of the menu
# screen.
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

# Entry screen.  Contains list of plays that can be rehearsed,
# Settings button, and Information Button (Neither are currently
# functional)
class MenuScreen(Screen):
    pass

# Main screen.  Contains character selection menu, act-scene-line selection
# (not currently functional), lineButton, and prompt button (not currently
# functional).  Title bar contains Script Menu button to return to Menu Screen
# and the Settings button (not currently functional).
class RehearseScreen(Screen):
    pass


# Contains all functions of the app
class TestApp(App):

    # Set default attributes for the normal function of the application

    userChar = StringProperty()
    playName = StringProperty('None Selected')
    
    lineNum = NumericProperty()
    charLineNum = NumericProperty()
    
    charList = ListProperty()
    lineList = ListProperty()

    # cuesMode indicates whether the app should speak all lines but those 
    # of the userChar (when False), or skip through the script and only 
    # speak lines which are specifically cues for the userChar (when True)
    # 
    # At this stage of development, cuesMode is automatically and 
    # permanently set to True
    cuesMode = BooleanProperty(True)

    # Resets all data for rehearsal so that script will start from the beginning
    def resetData(self):

        print('Reset Data was called!')

        self.userChar = ''

        self.lineList = []
        self.charList = []
        
        # Reset so that rehearsal will start from the first line
        self.lineNum = 0
        self.charLineNum = -1

    
    def promptMe(self, btn):
        print('Line Num: ' + str(self.lineNum))
        print('Character Line: ' + str(self.charLineNum))
        if self.userChar == '':
            self.nextLine(btn)
            return
        if self.charLineNum == -3:
            btn.text = 'You\'re at the end of the script!  Click here to return to the beginning!'
        elif self.charLineNum == -1 or self.lineNum == 0:
            if self.charList[0] == self.userChar:
                btn.text = self.lineList[0] + "\nClick to move to next cue."
                self.charLineNum = 0
            else:
                btn.text = 'You don\'t have the first line, so click here to get started!'
        else:
            btn.text = self.lineList[self.charLineNum] + "\nClick to move to next cue."
 
    # Speaks the line of the script which the current lineNum indicates,
    # Re-enables the lineButton 
    def speakLine(self, btn):
            if not (self.charList[self.lineNum] == self.userChar):
                lineForSpeak = self.lineList[self.lineNum].replace("\'", "\\\'")
                os.system("say -v Alex" + lineForSpeak)
            self.lineNum += 1
            btn.disabled = False

    # Function called by the main button (lineButton) on the Rehearse Screen
    #
    # Informs the user of what action to take and calls speakLine for cues
    #
    # Disables and re-enables lineButton to prevent simultaneous function calls
    # from causing errors
    def nextLine(self, btn):

        btn.disabled = True

        if self.userChar == '':
            btn.text = 'Please select a character to rehearse as first!'

            # Ensure that selected character will start from the beginning of the script
            self.lineNum = 0
            self.charLineNum = -1

            btn.disabled = False

        else:

            if self.lineNum == 0 and (self.charLineNum == -1 or self.charLineNum == -3):
                btn.text = 'You are at the beginning of this part of the script.' + \
                            '\nIf you have the first line, speak now, otherwise ' + \
                            '\nclick to jump to your first cue.'
                self.charLineNum = -1
                if self.charList[0] == self.userChar: 
                    self.lineNum += 1
                    btn.disabled = False
                    return
                else: 
                    for i in range(len(self.charList)):
                        if self.charList[i] == self.userChar:
                            self.charLineNum = i
                            btn.disabled = False
                            return

            if self.cuesMode: 
                if self.lineNum < (len(self.lineList) - 1):
                    if self.charList[self.lineNum  + 1] == self.userChar and (not self.charList[self.lineNum] == self.userChar):
                        #btn.text = self.lineList[self.lineNum]    This would be used to display the cue-line text
                        btn.text = 'Next Cue!'
                        self.charLineNum = self.lineNum + 1
                        Clock.schedule_once(lambda dt: self.speakLine(btn), 0.2) 
                    else:
                        while self.lineNum < (len(self.lineList) - 1):
                            self.lineNum += 1   
                            if self.lineNum == (len(self.lineList) - 1):
                                self.nextLine(btn)
                                break
                            if self.charList[self.lineNum + 1] == self.userChar:
                                self.nextLine(btn)
                                break
                else:
                    self.lineNum = 0
                    btn.text = 'You have reached the end of your part of this script.\nClick here to start again!'           
                    self.charLineNum = -3
                    btn.disabled = False
            
            
            # This mode is currently inaccessible 
            else:
                if self.lineNum < len(self.lineList):
                    if self.charList[self.lineNum] == self.userChar:
                        btn.text = 'Your  line!'    
                    else:
                        #btn.text = self.lineList[self.lineNum]    This would be used to display the cue-line text
                        btn.text = 'Next Line!'
                    Clock.schedule_once(lambda dt: self.speakLine(btn), 0.2)
                else:
                    self.lineNum = 0
                    btn.text = 'You have reached the end of this script.\nClick here to start again'
                    btn.disabled = False

    # Function to build character selection menu for Rehearse Screen
    # Clears current rehearsal data and populates dropdown.  
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
        lineButton = screens.current_screen.ids.lineButton

        setattr(charButton, 'text', 'Character')

        # Function called on_click of the character selection dropdown menu
        def setUserChar(selection):
            setattr(charButton, 'text', selection)
            
            # Reset so that rehearsal will start from the first line
            self.lineNum = 0
            self.charLineNum = -1
            lineButton.text = 'Start Rehearsing!'

            if selection == '':
                setattr(charButton, 'text', 'Character')
            self.userChar = selection

        charButton.bind(on_press=lambda x:setUserChar(''))

        charMenu.bind(on_select=lambda instance, x:setUserChar(x))

    # Initial function.  Called when the app first loads.
    # Sets up Screen Manager and menu of play options.
    def build(self):

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RehearseScreen(name='rehearse'))
        sm.transition = NoTransition(duration=0)

        # Called on_click of a play option by the user.
        # Loads the lines and character list of the selected play and
        # switches to the Rehearse Screen.
        def selectPlay(selection):

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

            sm.current_screen.bind(on_enter=lambda x:self.charSelect(sm))

            scriptMenuButton = sm.current_screen.ids.scriptMenuButton
            scriptMenuButton.bind(on_release=lambda x:self.resetData())
            print(scriptMenuButton.text)

            lineButton = sm.current_screen.ids.lineButton
            lineButton.text = 'Start Rehearsing!'
        
        playMenu = sm.current_screen.ids.playMenu
        playMenu.bind(minimum_height=playMenu.setter('height'))
        for i in range(len(PLAY_LIST)):
            btn = Button(text=PLAY_LIST[i], font_size=30, size_hint=(1, None))
            if btn.text == 'Test Button - Do Not Click':
                btn.background_color = [1, 0, 0, 1]
            btn.bind(on_release=lambda x:selectPlay(x.text))
            playMenu.add_widget(btn)

        rehearseScreen = sm.screens[1]
        lineButton = rehearseScreen.ids.lineButton
        lineButton.bind(on_release=lambda x:self.nextLine(lineButton))  
        promptButton = rehearseScreen.ids.promptButton
        promptButton.bind(on_release=lambda x:self.promptMe(lineButton))

        return sm
    

if __name__ == '__main__':
    TestApp().run()