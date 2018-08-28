# Rehearse Screen Methods
import kivy
kivy.require('1.10.1')

import os
from kivy.clock import Clock, mainthread

import config
import shared

# Changes lineButton text to the user's current line
def promptMe(manager):

    lineButton = manager.current_screen.ids.lineButton

    if config.character == '':
        nextLine(manager)
        return
    if config.characterLineNum == -3:
        lineButton.text = 'You\'re at the end of the script!  Click here to return to the beginning!'
    elif config.characterLineNum == -1 or config.lineNum == 0:
        if config.characterList[0] == config.character:
            lineButton.text = config.lineList[0] + "\nClick to move to next cue."
            config.characterLineNum = 0
        else:
            lineButton.text = 'You don\'t have the first line, so click here to get started!'
            config.characterLineNum = -2
    else:
        lineButton.text = config.lineList[config.characterLineNum] + "\nClick to move to next cue."


# Speaks the line of the script which the current lineNum indicates
def speakLine(manager):

    os.system("osascript -e 'set Volume " + str(config.volume) + "'")
    
    lineButton = manager.current_screen.ids.lineButton
    promptMe = manager.current_screen.ids.promptButton
    lineButton.disabled = True
    
    if not (config.characterList[config.lineNum] == config.character):
        lineForSpeak = config.lineList[config.lineNum].replace("\'", "\\\'")
        lineForSpeak = lineForSpeak.replace(";", "\;")
        if config.cutMode:
            phrases = lineForSpeak.split("\n")
            if len(phrases) < 3:
                lineForSpeak = " ".join(phrases)
            else:
                lineForSpeak = " ".join(phrases[-3:])
        else:
            lineForSpeak = lineForSpeak.replace("\n", " ")
        os.system("say -v Alex" + lineForSpeak + "-r " + str(config.rate)) 
            
    config.lineNum += 1
    
    if not config.cuesMode and config.lineNum < len(config.lineList):
        if config.characterList[config.lineNum] == config.character:
            config.lineNum += 1
            lineButton.text = 'Your Line!'
            promptMe.disabled = False
            
    lineButton.disabled = False


# Function called by the main button (lineButton) on the Rehearse Screen
#
# Informs the user of what action to take and calls speakLine for cues
#
# Disables and re-enables lineButton to prevent simultaneous function calls
# from causing errors
def nextLine(manager):

    if config.currentScene == '':
        shared.setActScene(manager, config.scenesList[0])
        
    lineButton = manager.current_screen.ids.lineButton
    promptButton = manager.current_screen.ids.promptButton
    
    lineButton.disabled = True
    config.prevScreen = 'rehearse'

    if config.character == '':
        lineButton.text = 'Please select a character to rehearse as first!'

        # Ensure that selected character will start from the beginning 
        # of the current section of the script
        shared.jumpToSectionStart()

        lineButton.disabled = False

    else:

        if config.lineNum == 0 and (config.characterLineNum == -1 or config.characterLineNum == -3):
            cueOrLine = '\nclick to start rehearsing.'
            if config.cuesMode:
                cueOrLine = '\nclick to jump to your first cue.'
            lineButton.text = 'You are at the beginning of this part of the script.' + \
                        '\nIf you have the first line, speak now, otherwise ' + \
                        cueOrLine
            
            promptButton.disabled = False
            config.characterLineNum = -1
            
            if config.characterList[0] == config.character: 
                config.lineNum += 1
                lineButton.disabled = False
                return
            else: 
                for i in range(len(config.characterList)):
                    if config.characterList[i] == config.character:
                        config.characterLineNum = i
                        lineButton.disabled = False
                        return

        if config.cuesMode: 
            if config.lineNum < (len(config.lineList) - 1):
                if config.characterList[config.lineNum  + 1] == config.character and (not config.characterList[config.lineNum] == config.character):
                    lineButton.text = 'Next Cue!'
                    config.characterLineNum = config.lineNum + 1
                    Clock.schedule_once(lambda dt: speakLine(manager), 0.2) 
                else:
                    while config.lineNum < (len(config.lineList) - 1):
                        config.lineNum += 1   
                        if config.lineNum == (len(config.lineList) - 1):
                            nextLine(manager)
                            break
                        if config.characterList[config.lineNum + 1] == config.character:
                            nextLine(manager)
                            break
            else:
                shared.nextScene(manager)
            
            lineButton.disabled = False
        
        else:
            if config.lineNum < len(config.lineList):
                if config.characterList[config.lineNum] == config.character:
                    promptButton.disabled = False
                    config.characterLineNum = config.lineNum
                    config.lineNum += 1
                else:
                    promptButton.disabled = True
                    lineButton.text = 'Next Line!'
                    Clock.schedule_once(lambda dt:speakLine(manager), 0.2)
            else:
                shared.nextScene(manager)
            lineButton.disabled = False

