#----------------------------
# Dragon Forest
# Text adventure game
# by Rob Watts
# Python 3.7.3
# Updated 10/6/2020
#
# TODO
# -Story
#   -Need whatever the mystery of the forest is
# -Load game
#   -If save file exists with username, ask to load?
#   -If StayedAtInn=True, give a random amount of health and armor boost, else take some HP away
#    for sleeping out in the cold with the animals and bugs
# -Artwork
#   -Some art with \ are spaced incorrectly on the line, like showForest()
# -General
#   -Search code for TODO/HACK/BUG comments
#   -What am I doing with npc.py?
#   -Move more long story pieces into textblocks.py (?) or just remove it
#----------------------------

# Python Libraries
import random
import sys
import time
import math

# My Custom Game Modules
from DFModules import artwork
from DFModules.player import Player
from DFModules import dataHelper
from DFModules import forest
from DFModules import common


# Constants
CONFIG_FILE = 'configData.ini'


#---------------------------
#       Game Start
#--------------------------

def main():

    exitGame = False

    artwork.showTitle()

    print('''

    [N]ew Game
    [L]oad Game

    [Q]uit
    ''')

    action = input('Command: ').upper()

    isNewGame = False

    if action == 'N':
        isNewGame = True
    elif action == 'L':
        # Attempt to Load Game
        saves = list(dataHelper.GetGameSaves())
        if len(saves) != 0:
            print('------- SAVED GAMES -----------')
            print()
            for idx, save in enumerate(saves):
                print(f"[{idx}] {save.split('_')[0]}")
            
            loadAnswer = int(input('Save Slot Number: '))

            if loadAnswer > -1 and loadAnswer <= len(saves):
                p1 = dataHelper.LoadGame(saves[loadAnswer])
        else:
            print('No save games found.')
            isNewGame = True



    if isNewGame == True:
        print('''
        You arrive at Dragon Forest. You stare at the trees
        that have been torched by fire, next to others with wiry branches
        that reach high covered in large leaves. You hear screeches off in
        the distance and the flapping of wings.

        Thoughts of turning back fill your head, but the mystery of Dragon Forest
        brings you closer. 

        ''')

        playerName = input('What is thy name? ')

        if playerName == '' or len(playerName) < 1:
            sys.exit()

        # Load the weapon data
        weaponData = dataHelper.LoadDataFromJson("Data\\weapons.json", "r")

        # Load the enemy data
        enemyData = dataHelper.LoadDataFromJson("Data\\enemies.json", "r")

        # Create Player
        p1 = Player(playerName, weaponData)

    # Display Stats
    common.DisplayPlayerStats(p1)

    #
    # GAME LOOP
    #
    while exitGame == False:

        if p1.Level >= 1 and p1.HasDiscoveredTown == True:
            print('''
    -= FOREST MENU =-
        
    [E]xplore the Forest           [S]tats
    [C]amp                         [H]elp
    [T]own

    [Q]uit.
            
            ''')
        else:
            print('''
    -= FOREST MENU =-
    
    [E]xplore the Forest         [S]tats
    [C]amp                       [H]elp

    [Q]uit.
            
            ''')

        command = input('Command: ').upper()

        if command == 'E':
            common.DoAction('exploreForest', p1, enemyData)
            
        elif command == 'C':
            common.DoAction('camp', p1, None)

        elif command == 'S':
            common.DoAction('stats', p1, None)

        elif command == 'H':
            common.DoAction('help', None, None)

        elif command == 'T' and p1.HasDiscoveredTown:
            common.DoAction('town', p1, None)

        elif command == 'Q':
            exitGame = True

        # DEBUG
        elif command == 'D':
            print('** DEBUG MODE **')
            
            p1.Level = int(input('Level (1-4): '))
            p1.Xp = int(input('XP Amount: '))
            p1.Armor = int(input('Health Amount: '))
            p1.Armor = int(input('Armor Amount: '))
            p1.Money = int(input('Money Amount: '))
            p1.HasDiscoveredTown = True

if __name__ == "__main__":
    main()