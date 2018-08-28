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
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition 
from kivy.clock import Clock, mainthread

import threading
import os
import re
import pyaudio
import wave

import menu
import config
import sm
import rehearse
import record
import shared
import search

# Layout used when use reaches end of current section.
# Contains buttons to progress to next section or repeat
# current section.
class NextSceneLayout(BoxLayout):
    pass


class SearchScreen(Screen):
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

class InfoScreen(Screen):
    pass

class RecordScreen(Screen):
    pass

# Contains all functions of the app
class TestApp(App):

    # Initial function.  Called when the app first loads.
    # Sets up Screen Manager and menu of play options.
    def build(self):

        manager = ScreenManager()
        manager.add_widget(MenuScreen(name='menu'))
        manager.add_widget(InfoScreen(name='info'))
        manager.add_widget(RecordScreen(name='record'))
        manager.add_widget(RehearseScreen(name='rehearse'))
        manager.add_widget(SearchScreen(name='search'))
        manager.add_widget(SettingsScreen(name='settings'))
        manager.transition = NoTransition(duration=0)

        # Set Up Menu Screen
        config.prevScreen = 'menu'

        menu.buildPlayMenu(manager)

        menuSettingsButton = manager.current_screen.ids.settingsButton
        menuInfoButton = manager.current_screen.ids.infoButton
        
        menuSettingsButton.bind(on_release=lambda x:sm.openSettings(manager))
        menuInfoButton.bind(on_release=lambda x:sm.switchToScreen(manager, 'info'))

        # Set Up Info Screen
        infoSettingsButton = manager.screens[config.SCREEN_IDS['info']].ids.settingsButton
        infoBackButton = manager.screens[config.SCREEN_IDS['info']].ids.backButton
        
        infoSettingsButton.bind(on_release=lambda x:sm.openSettings(manager))
        infoBackButton.bind(on_release=lambda x:sm.switchToScreen(manager, config.prevScreen))

        # Set Up Record Screen
        recordScreen = manager.screens[config.SCREEN_IDS['record']]
        #THIS IS JUST A TEST.  
        recordScreen.ids.lineSearch.bind(on_release=lambda x:sm.switchToScreen(manager, 'search'))

        # Set Up Rehearse Screen
        rehearseScreen = manager.screens[config.SCREEN_IDS['rehearse']]
        
        lineButton = rehearseScreen.ids.lineButton
        lineButton.bind(on_release=lambda x:rehearse.nextLine(manager))  
        
        promptButton = rehearseScreen.ids.promptButton
        promptButton.bind(on_release=lambda x:rehearse.promptMe(manager))

        rehearseSettingsButton = rehearseScreen.ids.settingsButton
        rehearseSettingsButton.bind(on_release=lambda x:sm.openSettings(manager))

        rehearseRecordButton = rehearseScreen.ids.recordButton
        rehearseRecordButton.bind(on_release=lambda x:sm.switchToScreen(manager, 'record'))

        # Set Up Search Screen
        searchScreen  = manager.screens[config.SCREEN_IDS['search']]

        searchBar = searchScreen.ids.searchBar
        searchBar.bind(on_text_validate=lambda x:search.searchForLine(manager, searchBar.text))

        # Set Up Settings Screen
        manager.screens[config.SCREEN_IDS['settings']].ids.settingsButton.bind(on_release=lambda x: sm.exitSettings(manager))

        return manager
    

if __name__ == '__main__':
    TestApp().run()