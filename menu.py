# Menu Screen Methods
import kivy
kivy.require('1.10.1')

from kivy.uix.button import Button
import re

import config
import sm
import shared

def buildPlayMenu(manager):
    playMenu = manager.current_screen.ids.playMenu
    playMenu.bind(minimum_height=playMenu.setter('height'))
    for i in range(len(config.PLAY_LIST)):
        btn = Button(text=config.PLAY_LIST[i], font_size=30, size_hint=(1, None))
        if btn.text == 'Test Button - Do Not Click':
            btn.background_color = [1, 0, 0, 1]
        btn.bind(on_release=lambda x:selectPlay(manager, x.text))
        playMenu.add_widget(btn)

# Called on_click of a play option by the user.
# Loads the lines and character list of the selected play and
# switches to the Rehearse Screen.
# Decomposition needed!
def selectPlay(manager, selection):

    sm.switchToScreen(manager, 'rehearse') 
    result =  "".join(selection.split(" ")).lower()
    playName = result + ".txt"

    fileObject = open(playName)
    
    currentString = ''
    currentSceneLines = []
    currentSceneChars = []
    currentAct = ''
    prevLineChar = False

    for line in fileObject: 
        
        if not re.search('[a-zA-Z]', line):
            if not currentString == '':
                config.lineList.append(currentString)
                config.audioFiles.append('')
                currentSceneLines.append(currentString)
            prevLineChar = False
            currentString = ''
        elif ('ACT' in line) or ('PROLOGUE' in line):
            currentAct = line
            currentAct = currentAct.replace("\n", "")
            if ('PROLOGUE' in line):
                config.scenesList.append(currentAct)
        elif ('SCENE' in line):
            sceneAndDescription = line.split('.')
            scene = sceneAndDescription[0]
            config.scenesList.append(currentAct + ', ' + scene)
            if not currentSceneChars == []:
                config.charactersByScene.append(currentSceneChars)
                config.linesByScene.append(currentSceneLines)
            currentSceneChars = []
            currentSceneLines = []
        elif (not 'ACT' in line) and (not 'SCENE' in line) and ('.' in line) and (not re.search('[a-z]',line)):
            config.characterList.append(line[:-1])
            currentSceneChars.append(line[:-1])
            prevLineChar = True
        elif prevLineChar:
            currentString = currentString + ' ' + line
        else:
            pass
    
    config.linesByScene.append(currentSceneLines)
    config.charactersByScene.append(currentSceneChars)
    config.fullLineList = config.lineList
    config.fullCharacterList = config.characterList

    for i in range(len(config.scenesList)):
        config.linesBySceneDict[config.scenesList[i]] = config.linesByScene[i]
        config.charactersBySceneDict[config.scenesList[i]] = config.charactersByScene[i]

    shared.buildCharacterMenu(manager, 'record')
    shared.buildCharacterMenu(manager, 'rehearse')
    shared.buildActSceneMenu(manager, 'record')
    shared.buildActSceneMenu(manager, 'rehearse')

    scriptMenuButton = manager.current_screen.ids.scriptMenuButton
    scriptMenuButton.bind(on_release=lambda x: sm.resetScript(manager))

    lineButton = manager.current_screen.ids.lineButton
    lineButton.text = 'Start Rehearsing!'
    config.prevScreen = 'rehearse'