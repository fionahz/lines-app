import kivy
kivy.require('1.10.1')

from kivy.uix.button import Button
from kivy.uix.label import Label
import config

def searchForLine(manager, phrase):
    searchResultsLayout = manager.current_screen.ids.searchResultsLayout
    searchResultsLayout.clear_widgets()
    noneFoundLabel = Label(text='No lines containing that phrase were found.\nPlease try searching a different phrase.')
    resultsDict = {}
    searchResultsLayout.bind(minimum_height=searchResultsLayout.setter('height'))
    for i in range(len(config.fullLineList)):
        if phrase in config.fullLineList[i]:
            lineForAddPieces = config.fullLineList[i].split("\n")
            lineForAdd = lineForAddPieces[0]
            resultsDict[config.fullLineList[i]] = i
            btn = Button(text=lineForAdd, font_size=30, size_hint=(1, None))
            # btn.bind(on_release=lambda x:someFunction)
            searchResultsLayout.add_widget(btn)
    if resultsDict == {}:
        searchResultsLayout.add_widget(noneFoundLabel)    