#----------------------------
# Title:        Dragon Forest
# Description:  Text adventure game
# Author:       Rob Watts
# Min Python:   3.7
# Updated:      10/8/2020
#
# TODO
# -Story
#   -Need whatever the mystery of the forest is
# -Artwork
#   -Some art with \ are spaced incorrectly on the line, like showForest()
# -General
#   -Search code for TODO/HACK/BUG comments
#   -What am I doing with npc.py?
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

    # Load the weapon data
    weaponData = dataHelper.LoadDataFromJson("Data\\weapons.json", "r")

    # Load the enemy data
    enemyData = dataHelper.LoadDataFromJson("Data\\enemies.json", "r")


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

                if p1.StayedAtInn == True:
                    loudNoisesList = ['screeching','yelling','crying','pounding on the wall']
                    noise = random.choice(loudNoisesList)
                    print(f'\nThat was a restful sleep, except for the {noise}. You\'ve gained 10 HP')
                    p1.Health = 10
                else:
                    print('\nThe ground was hard and cold. You might have ants in your pants. You\'ve lost 5 HP')
                    p1.Health = -5
        else:
            print('No save games found.')
            isNewGame = True

    # New Game
    if isNewGame == True:
        print('''
        You arrive at Dragon Forest. You stare at the trees
        that have been torched by fire, next to others with wiry branches
        that reach high covered in large leaves. You hear screeches off in
        the distance and the flapping of wings.

        Thoughts of turning back fill your head, but the mystery of Dragon Forest
        brings you closer. 
        ''')

        # Get Player Name
        playerName = input('What is thy name? ')

        if playerName == '' or len(playerName) < 1:
            sys.exit()

        # Create Player
        p1 = Player(playerName, weaponData)
        p1.SetDefaultValues()

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
            print('You walk around and find a big log. You\'re not sure what lives in there. And it smells.')
            dataHelper.SaveGame(p1)

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