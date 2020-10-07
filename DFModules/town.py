
import time

# Game Modules
from DFModules import artwork
from DFModules import common

#
# Functions
#

def Town(p1):

    artwork.showTown()

    print('''
    Climbing over the rocks and pushing the branches out of the way, you see the town.
    As you walk towards the town, there\'s an Inn and a Blacksmith shop.
    People are bustling around doing chores, bartering for goods, yelling at each other.
    Children are playing games. One big kid is beating on another... ah, kids, what can you do?

    The rest of town is a blackened, charred, mess. A few buildings still smoldering...
    ''')

    isPlayerAtTown = True
    while isPlayerAtTown == True:

        print('''
    -= TOWN MENU =-

    [I]nn
    [B]lacksmith
    [T]alk to a Random Stranger
    
    [L]eave Town
        ''')

        action = input('Command: ').upper()
        
        if action == 'I':
            common.DoAction('townInn', p1, None)

        elif action == 'B':
            common.DoAction('townBlacksmith', p1, None)

        elif action == 'T':
            common.DoAction('townTalkToNpc', p1, None)

        elif action == 'L':
            return  # should go back to the main game loop with main menu
