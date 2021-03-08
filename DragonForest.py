#----------------------------
# Title:        Dragon Forest
# Description:  Text adventure game
# Author:       Rob Watts
# Min Python:   3.7
# Updated:      03/07/2021
#
# TODO
# -General
#   -Search code for TODO/HACK/BUG comments
#   -Need ways to get health other than leveling up
#   -Need to finish end boss
#   -Add testing and refactor as needed to support testing
# -BUG
#   -Any single quotes escaped by the \ in a (''' x ''') block have the ' missing
#   -Some art with \ are spaced incorrectly on the line, like showForest()
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


#CONFIG_FILE = 'configData.ini'


#---------------------------
#       Game Start
#--------------------------

def main():

    exitGame = False

    # Load the weapon data
    weaponData = dataHelper.load_data_from_json("Data\\weapons.json", "r")

    # Load the enemy data
    enemyData = dataHelper.load_data_from_json("Data\\enemies.json", "r")

    artwork.show_title()

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
        
        result = common.load_saved_games_menu()

        if result == None:
            isNewGame = True
            print('No Save Found or Loaded')
        else:
            # Post Load Actions
            p1 = result # re-assign for naming purposes only
            result = None # release memory
            if p1.StayedAtInn == True:
                loudNoisesList = ['screeching','yelling','crying','pounding on the wall']
                noise = random.choice(loudNoisesList)

                print(f'\nThat was a restful sleep, except for the {noise}. You\'ve gained 10 HP.')
                p1.Health = 10
                p1.StayedAtInn = False # this needs to be set to false again
            else:
                p1.Health = -5
                if p1.is_dead():
                    print('\nUnfortunately you are not only merely dead, you are really most sincerely dead.')
                    print('< Deleting Save Game >')
                    dataHelper.delete_save_game(p1.Name)
                    sys.exit()
                else:
                    print('\nThe ground was hard and cold. You might have ants in your pants. You\'ve lost 5 HP')

    elif action == 'Q':
        sys.exit()

    # New Game
    if isNewGame == True:
        print('''
        You arrive at Dragon Forest. You stare at the trees that have been 
        torched by fire, next to others with wiry branches that reach high 
        covered in large leaves. You hear screeches off in the distance and 
        the flapping of wings.

        You have thoughts of turning back, but the stories of Dragon Forest
        push you forward. 
        ''')

        # Get Player Name
        playerName = input('What is thy name? ')

        if playerName == '' or len(playerName) < 1:
            sys.exit()

        # Create Player
        p1 = Player(playerName, weaponData)
        p1.set_default_values()

    # Display Stats
    common.display_player_stats(p1)

    #
    # GAME LOOP
    #
    while exitGame == False:

        if p1.Level == 1 or p1.Level == 2 and p1.HasDiscoveredTown == True:
            print('''
    -= FOREST MENU =-
        
    [E]xplore the Forest           [S]tats
    [C]amp                         [H]elp
    [T]own

    [Q]uit.
            
            ''')
        elif p1.Level >= 3:
            print('''
    -= FOREST MENU =-
        
    [E]xplore the Forest           [S]tats
    [C]amp                         [H]elp
    [T]own
    [D]ragon Cave

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
            common.do_action('exploreForest', p1, enemyData)
            
        elif command == 'C':
            common.do_action('camp', p1, None)

        elif command == 'S':
            common.do_action('stats', p1, None)

        elif command == 'H':
            common.do_action('help', None, None)

        elif command == 'T' and p1.HasDiscoveredTown:
            common.do_action('town', p1, None)

        elif command == 'D' and p1.Level == 3:
            common.do_action('dragoncave', p1, enemyData)

        elif command == 'Q':
            exitGame = True
            print('You walk around and find a big log. You\'re not sure what lives in there. And it smells.')
            dataHelper.save_game(p1)

        # DEBUG
        elif command == "DD":
            print('** DEBUG MODE **')
            
            p1.Level = int(input('Level (1-4): '))
            p1.Xp = int(input('XP Amount: '))
            p1.Armor = int(input('Health Amount: '))
            p1.Armor = int(input('Armor Amount: '))
            p1.Money = int(input('Money Amount: '))
            p1.HasDiscoveredTown = True

if __name__ == "__main__":
    main()