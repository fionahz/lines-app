#Constants and important global variables

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

#Keep these numbers up to date  with the order that screens are added to the manager
SCREEN_IDS = {'menu': 0, 'info': 1, 'record': 2, 'rehearse': 3, 'search': 4, 'settings': 5}

# Character currently being rehearsed by user
character = ""
# Script currently being rehearsed by user
playName = ""

# Track user's progress through script
lineNum = 0
characterLineNum = -1

# Current attributes for section of script being rehearsed
characterList = []
lineList = []

# All speakers in the script, in order
fullCharacterList = []
# All lines in the script, in order
fullLineList = []

# List of strings, of the form Act #, Scene #
scenesList = []
# Current scene being rehearsed
currentScene = ""
# Stores screen name, used for exiting settings screen
prevScreen = ""
# 2D array of all lines, in order, organized by scene
linesByScene = []
# 2D array of all speakers, in order, organized by scene
charactersByScene = []

# scenesList keyed to sceneLinesList
linesBySceneDict = {}
# scenesList keyed to sceneCharsList
charactersBySceneDict = {}

# cuesMode indicates whether the app should speak all lines but those 
# of the userChar (when False), or skip through the script and only 
# speak lines which are specifically cues for the userChar (when True)
cuesMode = True

# cutMode indicates whether the app should speak entire lines (when False)
# or skip to the last few phrases of each line for faster rehearsal.
cutMode = False

volume = 2
rate = 200

audioFiles = []

recordMode = ""