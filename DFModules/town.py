
import time

# Game Modules
from DFModules import artwork
from DFModules import common

#
# Functions
#

def Town(p1):

    artwork.showTown()

    # First time coming into town, show these opening story lines
    if p1.HasDiscoveredTown == False:
        print('Climbing over the rocks and pushing the branches out of the way, you see a town.')
        time.sleep(2)
        print('As you walk towards the town, you spot an Inn and... a Blacksmith shop!')
        time.sleep(1)
        print('You look at your battle worn Stick, wanting to toss it into the bushes where it belongs, but alas you keep it.')
        time.sleep(1)
        print('People are bustling around doing chores, bartering for goods, yelling at each other.')
        time.sleep(1)
        print('Children are playing games. One big kid is beating on another... ah, kids, what can you do?')
        time.sleep(1)
        print()
        print('As you get closer and can see around the street, you stop. Stunned.')
        time.sleep(2)
        print('The rest of town is a blackened, charred, mess. A few buildings still smoldering...')
        p1.HasDiscoveredTown = True

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
