import kivy
kivy.require('1.10.1')

# Working prototype of LINE! app

from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
ListProperty, BooleanProperty, DictProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition 
from kivy.clock import Clock, mainthread

import os
import re

# Global Constant with all properly formatted scripts
PLAY_LIST = ['Mini Script','Romeo and Juliet', \
'Much Ado About Nothing','Test Button - Do Not Click', \
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

# Layout used when use reaches end of current section.
# Contains buttons to progress to next section or repeat
# current section.
class NextSceneLayout(BoxLayout):
    pass

# Entry screen. Contains list of plays that can be rehearsed,
# Settings button, and Information Button 
class MenuScreen(Screen):
    pass

# Main screen.  Contains character selection menu, act-scene-line selection
# (not currently functional), lineButton, and prompt button (not currently
# functional).  Title bar contains Script Menu button to return to Menu Screen
# and the Settings button (not currently functional).
class RehearseScreen(Screen):
    pass

# Contains control for volume and speed of speech, and cues mode.
class SettingsScreen(Screen):
    pass


# Contains all functions of the app
class TestApp(App):

    # Set default attributes for the normal function of the application

    # Character currently being rehearsed by user
    userChar = StringProperty()
    # Script currently being rehearsed by user
    playName = StringProperty()
    
    # Track user's progress through script
    lineNum = NumericProperty()
    charLineNum = NumericProperty()
    
    # Current attributes for section of script being rehearsed
    charList = ListProperty()
    lineList = ListProperty()

    # All speakers in the script, in order
    fullCharList = ListProperty()
    # All lines in the script, in order
    fullLineList = ListProperty()

    # List of strings, of the form Act #, Scene #
    scenesList = ListProperty()
    # Current scene being rehearsed
    currentScene = StringProperty()
    # 2D array of all lines, in order, organized by scene
    sceneLinesList = ListProperty()
    # 2D array of all speakers, in order, organized by scene
    sceneCharsList = ListProperty()

    # scenesList keyed to sceneLinesList
    sceneLinesDict = DictProperty()
    # scenesList keyed to sceneCharsList
    sceneCharsDict = DictProperty()

    # Stores screen name, used for exiting settings screen
    prevScreen = StringProperty()

    # cuesMode indicates whether the app should speak all lines but those 
    # of the userChar (when False), or skip through the script and only 
    # speak lines which are specifically cues for the userChar (when True)
    cuesMode = BooleanProperty(True)
    
    # cutMode indicates whether the app should speak entire lines (when False)
    # or skip to the last few phrases of each line for faster rehearsal.
    cutMode = BooleanProperty(False)

    volume = NumericProperty()
    rate = NumericProperty()
    
    # Resets indexes to start of current section
    def jumpToSectionStart(self, manager):
        self.lineNum = 0
        self.charLineNum = -1

    # Resets all data for rehearsal so that script will start from the beginning
    def resetScript(self, manager):

        #TODO: Check this line, not sure why it's here.
        self.prevScreen = 'menu'

        self.userChar = ''

        self.lineList = []
        self.charList = []
        self.scenesList = []

        self.sceneLinesList = []
        self.sceneCharsList = []

        self.sceneLinesDict = {}
        self.sceneCharsDict = {}
        self.currentScene = ''
        
        # Reset so that rehearsal will start from the first line
        self.jumpToSectionStart(manager)

    # Changes lineButton text to the user's current line
    def promptMe(self, manager):

        lineButton = manager.current_screen.ids.lineButton

        if self.userChar == '':
            self.nextLine(manager)
            return
        if self.charLineNum == -3:
            lineButton.text = 'You\'re at the end of the script!  Click here to return to the beginning!'
        elif self.charLineNum == -1 or self.lineNum == 0:
            if self.charList[0] == self.userChar:
                lineButton.text = self.lineList[0] + "\nClick to move to next cue."
                self.charLineNum = 0
            else:
                lineButton.text = 'You don\'t have the first line, so click here to get started!'
                self.charLineNum = -2
        else:
            lineButton.text = self.lineList[self.charLineNum] + "\nClick to move to next cue."
 
    # Speaks the line of the script which the current lineNum indicates
    def speakLine(self, manager):

        os.system("osascript -e 'set Volume " + str(self.volume) + "'")
        
        lineButton = manager.current_screen.ids.lineButton
        promptMe = manager.current_screen.ids.promptButton
        lineButton.disabled = True
        
        if not (self.charList[self.lineNum] == self.userChar):
            lineForSpeak = self.lineList[self.lineNum].replace("\'", "\\\'")
            lineForSpeak = lineForSpeak.replace(";", "\;")
            if self.cutMode:
                phrases = lineForSpeak.split("\n")
                if len(phrases) < 3:
                    lineForSpeak = " ".join(phrases)
                else:
                    lineForSpeak = " ".join(phrases[-3:])
            else:
                lineForSpeak = lineForSpeak.replace("\n", " ")
            print(lineForSpeak)
            os.system("say -v Alex" + lineForSpeak + "-r " + str(self.rate)) 
               
        self.lineNum += 1
        
        if not self.cuesMode and self.lineNum < len(self.lineList):
            if self.charList[self.lineNum] == self.userChar:
                self.lineNum += 1
                lineButton.text = 'Your Line!'
                promptMe.disabled = False
                
        lineButton.disabled = False
        
    #
    def nextScene(self, manager):
        
        lineButton = manager.current_screen.ids.lineButton
        promptButton = manager.current_screen.ids.promptButton
        self.lineNum = 0

        indexOfCurrent = self.scenesList.index(self.currentScene)
        rehearseContainer = manager.current_screen.ids.rehearseContainer
        buttonContainer = manager.current_screen.ids.buttonContainer
        rehearseContainer.remove_widget(buttonContainer)
        nextSceneContainer = NextSceneLayout(id='nextSceneLayout') 
        nextSceneLabel = nextSceneContainer.ids.nextSceneLabel

        def changeScreen(nsc):
            print(nsc.ids)
            nsc.clear_widgets()
            rehearseContainer.add_widget(buttonContainer)

        nextSceneButton = nextSceneContainer.ids.nextSceneButton
        repeatSceneButton = nextSceneContainer.ids.repeatSceneButton

        repeatSceneButton.bind(on_release=lambda x:self.setActScene(manager, self.currentScene))
        repeatSceneButton.bind(on_release=lambda x:changeScreen(nextSceneContainer))
        
        if not (self.currentScene == self.scenesList[-1]):
            nextSceneLabel.text = "You\'ve reached the end of your part for this scene."
            nextSceneButton.text = 'Rehearse next scene.'
            
            repeatSceneButton.text = 'Rehearse this scene again.'
            nextScene = self.scenesList[indexOfCurrent + 1]
            nextSceneButton.bind(on_release=lambda x:self.setActScene(manager, nextScene))
            nextSceneButton.bind(on_release=lambda x:changeScreen(nextSceneContainer))
        else:
            #TODO: Make this function.
            nextSceneLabel.text = 'You have reached the end of your part of the script.\nStart again from beginning, or practice last scene again?'
            nextSceneButton.text = "Start again from beginning."
            
            repeatSceneButton.text = "Practice last scene again."

            nextSceneButton.bind(on_release=lambda x:self.setActScene(manager, self.scenesList[0]))
            nextSceneButton.bind(on_release=lambda x:changeScreen(nextSceneContainer))
            
            self.charLineNum = -3

        rehearseContainer.add_widget(nextSceneContainer)
        lineButton.disabled = False

    # Function called by the main button (lineButton) on the Rehearse Screen
    #
    # Informs the user of what action to take and calls speakLine for cues
    #
    # Disables and re-enables lineButton to prevent simultaneous function calls
    # from causing errors
    def nextLine(self, manager):

        if self.currentScene == '':
            self.setActScene(manager, self.scenesList[0])
            
        lineButton = manager.current_screen.ids.lineButton
        promptButton = manager.current_screen.ids.promptButton
        
        lineButton.disabled = True
        self.prevScreen = 'rehearse'

        if self.userChar == '':
            lineButton.text = 'Please select a character to rehearse as first!'

            # Ensure that selected character will start from the beginning 
            # of the current section of the script
            self.jumpToSectionStart(manager)

            lineButton.disabled = False

        else:

            if self.lineNum == 0 and (self.charLineNum == -1 or self.charLineNum == -3):
                cueOrLine = '\nclick to start rehearsing.'
                if self.cuesMode:
                    cueOrLine = '\nclick to jump to your first cue.'
                lineButton.text = 'You are at the beginning of this part of the script.' + \
                            '\nIf you have the first line, speak now, otherwise ' + \
                            cueOrLine
                
                promptButton.disabled = False
                self.charLineNum = -1
                
                if self.charList[0] == self.userChar: 
                    self.lineNum += 1
                    lineButton.disabled = False
                    return
                else: 
                    for i in range(len(self.charList)):
                        if self.charList[i] == self.userChar:
                            self.charLineNum = i
                            lineButton.disabled = False
                            return

            if self.cuesMode: 
                if self.lineNum < (len(self.lineList) - 1):
                    if self.charList[self.lineNum  + 1] == self.userChar and (not self.charList[self.lineNum] == self.userChar):
                        lineButton.text = 'Next Cue!'
                        self.charLineNum = self.lineNum + 1
                        Clock.schedule_once(lambda dt: self.speakLine(manager), 0.2) 
                    else:
                        while self.lineNum < (len(self.lineList) - 1):
                            self.lineNum += 1   
                            if self.lineNum == (len(self.lineList) - 1):
                                self.nextLine(manager)
                                break
                            if self.charList[self.lineNum + 1] == self.userChar:
                                self.nextLine(manager)
                                break
                else:
                    self.nextScene(manager)
             
                lineButton.disabled = False
            
            else:
                if self.lineNum < len(self.lineList):
                    if self.charList[self.lineNum] == self.userChar:
                        promptButton.disabled = False
                        self.charLineNum = self.lineNum
                        self.lineNum += 1
                    else:
                        promptButton.disabled = True
                        lineButton.text = 'Next Line!'
                        Clock.schedule_once(lambda dt: self.speakLine(manager), 0.2)
                else:
                    self.nextScene(manager)
                lineButton.disabled = False

    # Function called on_click of the character selection dropdown menu
    def setUserChar(self, manager, selection):

        charButton = manager.screens[1].ids.charButton
        lineButton = manager.screens[1].ids.lineButton

        setattr(charButton, 'text', selection)
        
        # I DON'T WANT TO DO THIS, I THINK:
        # Reset so that rehearsal will start from the first line
        # self.jumpToSectionStart(manager)
        # lineButton.text = 'Start Rehearsing!'

        if selection == '':
            setattr(charButton, 'text', 'Character')
        self.userChar = selection

    def setActScene(self, manager, selection):
            
        actSceneButton = manager.current_screen.ids.actSceneButton
        lineButton = manager.current_screen.ids.lineButton
        
        setattr(actSceneButton, 'text', selection)

        # Reset so that rehearsal will start from the first line
        self.jumpToSectionStart(manager)
        lineButton.text = 'Start Rehearsing!'

        if selection == '':
            setattr(actSceneButton, 'text', 'Act #, Scene #')
            self.currentScene = ''
        else:
            self.lineList = self.sceneLinesDict[selection]
            self.charList = self.sceneCharsDict[selection]
            self.currentScene = selection
            while self.cuesMode and (self.userChar not in self.charList) and not (self.currentScene == self.scenesList[-1]):
                indexOfCurrent = self.scenesList.index(self.currentScene)
                print(self.scenesList[indexOfCurrent])
                self.setActScene(manager, self.scenesList[indexOfCurrent + 1])
                

    # Function to build character selection menu for Rehearse Screen
    # Clears current rehearsal data and populates dropdown.  
    def charSelect(self, manager):
        
        charMenu = manager.current_screen.ids.charMenu
        actSceneMenu = manager.current_screen.ids.actSceneMenu

        charMenu.clear_widgets()
        actSceneMenu.clear_widgets()
        cast = []

        for character in self.fullCharList:
            if character not in cast:
                btn = Button(text=character, size_hint_y=None, height=44)

                btn.bind(on_release=lambda btn: charMenu.select(btn.text))

                charMenu.add_widget(btn)
                cast.append(character)

        for scene in self.scenesList:
            btn = Button(text=scene, size_hint_y=None, height=44)

            btn.bind(on_release=lambda btn: actSceneMenu.select(btn.text))

            actSceneMenu.add_widget(btn)
        
        charButton = manager.current_screen.ids.charButton 
        actSceneButton = manager.current_screen.ids.actSceneButton
        lineButton = manager.current_screen.ids.lineButton

        setattr(charButton, 'text', 'Character')

        setattr(actSceneButton, 'text', 'Act #, Scene #')

        charButton.bind(on_press=lambda x:self.setUserChar(manager, ''))
        actSceneButton.bind(on_press=lambda x:self.setActScene(manager, ''))

        charMenu.bind(on_select=lambda instance, x:self.setUserChar(manager, x))
        actSceneMenu.bind(on_select=lambda instance, x:self.setActScene(manager, x))

    # Returns user to previous screen from Settings Screen
    def returnToPrevScreen(self, manager):
        cuesModeSwitch = manager.current_screen.ids.cuesModeSwitch
        cutModeSwitch = manager.current_screen.ids.cutModeSwitch
        volumeSlider = manager.current_screen.ids.volumeSlider
        speedSlider = manager.current_screen.ids.speedSlider
        self.cuesMode = cuesModeSwitch.active
        self.cutMode = cutModeSwitch.active
        self.volume = volumeSlider.value 
        self.rate = speedSlider.value
        manager.current = self.prevScreen
        self.setUserChar(manager, self.userChar)

    # Initial function.  Called when the app first loads.
    # Sets up Screen Manager and menu of play options.
    def build(self):

        manager= ScreenManager()
        manager.add_widget(MenuScreen(name='menu'))
        manager.add_widget(RehearseScreen(name='rehearse'))
        manager.add_widget(SettingsScreen(name='settings'))
        manager.transition = NoTransition(duration=0)

        manager.screens[2].ids.settingsButton.bind(on_release=lambda x: self.returnToPrevScreen(manager))

        # Called on_click of a play option by the user.
        # Loads the lines and character list of the selected play and
        # switches to the Rehearse Screen.
        def selectPlay(selection):

            manager.current = 'rehearse'
            result =  "".join(selection.split(" ")).lower()
            self.playName = result + ".txt"

            fileObject = open(self.playName)
            
            currentString = ''
            currentSceneLines = []
            currentSceneChars = []
            currentAct = ''
            prevLineChar = False

            for line in fileObject: 
                
                if not re.search('[a-zA-Z]', line):
                    if not currentString == '':
                        self.lineList.append(currentString)
                        currentSceneLines.append(currentString)
                    prevLineChar = False
                    currentString = ''
                elif ('ACT' in line) or ('PROLOGUE' in line):
                    currentAct = line
                    currentAct = currentAct.replace("\n", "")
                    if ('PROLOGUE' in line):
                        self.scenesList.append(currentAct)
                    print(currentAct)
                elif ('SCENE' in line):
                    sceneAndDescription = line.split('.')
                    scene = sceneAndDescription[0]
                    self.scenesList.append(currentAct + ', ' + scene)
                    if not currentSceneChars == []:
                        self.sceneCharsList.append(currentSceneChars)
                        self.sceneLinesList.append(currentSceneLines)
                    currentSceneChars = []
                    currentSceneLines = []
                elif (not 'ACT' in line) and (not 'SCENE' in line) and ('.' in line) and (not re.search('[a-z]',line)):
                    self.charList.append(line[:-1])
                    currentSceneChars.append(line[:-1])
                    prevLineChar = True
                elif prevLineChar:
                    currentString = currentString + ' ' + line
                else:
                    pass
            
            self.sceneLinesList.append(currentSceneLines)
            self.sceneCharsList.append(currentSceneChars)
            self.fullLineList = self.lineList
            self.fullCharList = self.charList

            for i in range(len(self.scenesList)):
                self.sceneLinesDict[self.scenesList[i]] = self.sceneLinesList[i]
                self.sceneCharsDict[self.scenesList[i]] = self.sceneCharsList[i]

            self.charSelect(manager)

            scriptMenuButton = manager.current_screen.ids.scriptMenuButton
            scriptMenuButton.bind(on_release=lambda x:self.resetScript(manager))

            lineButton = manager.current_screen.ids.lineButton
            lineButton.text = 'Start Rehearsing!'
            self.prevScreen = 'rehearse'
        
        playMenu = manager.current_screen.ids.playMenu
        playMenu.bind(minimum_height=playMenu.setter('height'))
        for i in range(len(PLAY_LIST)):
            btn = Button(text=PLAY_LIST[i], font_size=30, size_hint=(1, None))
            if btn.text == 'Test Button - Do Not Click':
                btn.background_color = [1, 0, 0, 1]
            btn.bind(on_release=lambda x:selectPlay(x.text))
            playMenu.add_widget(btn)

        rehearseScreen = manager.screens[1]
        lineButton = rehearseScreen.ids.lineButton
        lineButton.height = lineButton.minimum_height
        lineButton.bind(on_release=lambda x:self.nextLine(manager))  
        promptButton = rehearseScreen.ids.promptButton
        promptButton.bind(on_release=lambda x:self.promptMe(manager))
       
        # Sets up the Settings Screen
        def openSettings():

            self.prevScreen = manager.current
            manager.current = 'settings'

        menuSettingsButton = manager.current_screen.ids.settingsButton
        rehearseSettingsButton = rehearseScreen.ids.settingsButton

        menuSettingsButton.bind(on_release=lambda x:openSettings())
        rehearseSettingsButton.bind(on_release=lambda x:openSettings())

        return manager
    

if __name__ == '__main__':
    TestApp().run()