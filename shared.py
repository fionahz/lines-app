# Shared Functions for Rehearse and Record
import kivy
kivy.require('1.10.1')

from kivy.uix.button import Button
from kivy.uix.label import Label
#IMPORT WHATEVER CONTAINS jumpToSectionStart
#IMPORT CLASS NextSceneLayout]
import config
from testApp import NextSceneLayout

# Function to build character selection menu for Rehearse Screen
# Clears current rehearsal data and populates dropdown.  
def buildCharacterMenu(manager, screen):
    
    charMenu = manager.screens[config.SCREEN_IDS[screen]].ids.charMenu
    charMenu.clear_widgets()
    cast = []

    for character in config.fullCharacterList:
        if character not in cast:
            btn = Button(text=character, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: charMenu.select(btn.text))
            charMenu.add_widget(btn)
            cast.append(character)
    
    charButton = manager.current_screen.ids.charButton 
    setattr(charButton, 'text', 'Character')
    charButton.bind(on_press=lambda x:setCharacter(manager, ''))
    charMenu.bind(on_select=lambda instance, x:setCharacter(manager, x))



def buildActSceneMenu(manager, screen):

    actSceneMenu = manager.screens[config.SCREEN_IDS[screen]].ids.actSceneMenu
    actSceneMenu.clear_widgets()

    for scene in config.scenesList:
        btn = Button(text=scene, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: actSceneMenu.select(btn.text))
        actSceneMenu.add_widget(btn)

    actSceneButton = manager.current_screen.ids.actSceneButton
    setattr(actSceneButton, 'text', 'Act #, Scene #')
    actSceneButton.bind(on_press=lambda x:setActScene(manager, ''))
    actSceneMenu.bind(on_select=lambda instance, x:setActScene(manager, x))


# Function called on_click of the character selection dropdown menu
def setCharacter(manager, selection):

    charButton = manager.screens[config.SCREEN_IDS['rehearse']].ids.charButton

    setattr(charButton, 'text', selection)

    if selection == '':
        setattr(charButton, 'text', 'Character')
    config.character = selection


def setActScene(manager, selection):
        
    actSceneButton = manager.current_screen.ids.actSceneButton
    lineButton = manager.current_screen.ids.lineButton
    
    setattr(actSceneButton, 'text', selection)

    # Reset so that rehearsal will start from the first line
    jumpToSectionStart()
    lineButton.text = 'Start Rehearsing!'

    if selection == '':
        setattr(actSceneButton, 'text', 'Act #, Scene #')
        config.currentScene = ''
    else:
        config.lineList = config.linesBySceneDict[selection]
        config.characterList = config.charactersBySceneDict[selection]
        config.currentScene = selection
        while config.cuesMode and (not config.character == '') and (config.character not in config.characterList) and not (config.currentScene == config.scenesList[-1]):
            indexOfCurrent = config.scenesList.index(config.currentScene)
            setActScene(manager, config.scenesList[indexOfCurrent + 1])

def changeScreen(nsc, rehearseContainer, buttonContainer):
    nsc.clear_widgets()
    rehearseContainer.add_widget(buttonContainer)

def nextScene(manager):
    
    lineButton = manager.current_screen.ids.lineButton
    promptButton = manager.current_screen.ids.promptButton
    config.lineNum = 0

    indexOfCurrent = config.scenesList.index(config.currentScene)
    rehearseContainer = manager.current_screen.ids.rehearseContainer
    buttonContainer = manager.current_screen.ids.buttonContainer
    rehearseContainer.remove_widget(buttonContainer)
    nextSceneContainer = NextSceneLayout(id='nextSceneLayout') 
    nextSceneLabel = nextSceneContainer.ids.nextSceneLabel

    nextSceneButton = nextSceneContainer.ids.nextSceneButton
    repeatSceneButton = nextSceneContainer.ids.repeatSceneButton

    repeatSceneButton.bind(on_release=lambda x:setActScene(manager, config.currentScene))
    repeatSceneButton.bind(on_release=lambda x:changeScreen(nextSceneContainer, rehearseContainer, buttonContainer))
    
    if not (config.currentScene == config.scenesList[-1]):
        nextSceneLabel.text = "You\'ve reached the end of your part for this scene."
        nextSceneButton.text = 'Rehearse next scene.'
        
        repeatSceneButton.text = 'Rehearse this scene again.'
        nextScene = config.scenesList[indexOfCurrent + 1]
        nextSceneButton.bind(on_release=lambda x:setActScene(manager, nextScene))
        nextSceneButton.bind(on_release=lambda x:changeScreen(nextSceneContainer, rehearseContainer, buttonContainer))
    
    else:
        nextSceneLabel.text = 'You have reached the end of your part of the script.\nStart again from beginning, or practice last scene again?'
        nextSceneButton.text = "Start again from beginning."
        
        repeatSceneButton.text = "Practice last scene again."

        nextSceneButton.bind(on_release=lambda x:setActScene(manager, config.scenesList[0]))
        nextSceneButton.bind(on_release=lambda x:changeScreen(nextSceneContainer, rehearseContainer, buttonContainer))
        
        config.characterLineNum = -3

    rehearseContainer.add_widget(nextSceneContainer)
    lineButton.disabled = False

def jumpToSectionStart():
    config.lineNum = 0
    config.characterLineNum = -1






