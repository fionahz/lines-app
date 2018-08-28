# Screen Change Methods
import kivy
kivy.require('1.10.1')

import config
import shared

# Switch to selected screen
def switchToScreen(manager, screen):
    manager.current = screen

# Resets all data for rehearsal so that script will start from the beginning
def resetScript(manager):

    #TODO: Check this line, not sure why it's here.
    config.prevScreen = 'menu'

    config.character = ''

    config.lineList = []
    config.characterList = []
    config.scenesList = []

    config.fullLineList = []
    config.fullCharacterList = []

    config.linesBySceneList = []
    config.charactersBySceneList = []

    config.linesBySceneDict = {}
    config.charactersBySceneDict = {}
    config.currentScene = ''
    
    # Reset so that rehearsal will start from the first line
    shared.jumpToSectionStart()

# Returns user to previous screen from Settings Screen
def exitSettings(manager):
    cuesModeSwitch = manager.current_screen.ids.cuesModeSwitch
    cutModeSwitch = manager.current_screen.ids.cutModeSwitch
    volumeSlider = manager.current_screen.ids.volumeSlider
    speedSlider = manager.current_screen.ids.speedSlider
    config.cuesMode = cuesModeSwitch.active
    config.cutMode = cutModeSwitch.active
    config.volume = volumeSlider.value 
    config.rate = speedSlider.value
    switchToScreen(manager, config.prevScreen) 
    shared.setCharacter(manager, config.character)

# Sets up the Settings Screen
def openSettings(manager):
    config.prevScreen = manager.current
    switchToScreen(manager, 'settings') 