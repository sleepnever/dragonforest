import random
import time

# Game Modules
from DFModules import artwork
from DFModules import common

#
# Functions related to the Inn
#

def PlayerCanStayAtInn(p1):

    if p1.Level == 1 and p1.Money >= 5:
        return True
    elif p1.Level == 2 and p1.Money >= 25:
        return True
    elif p1.Level == 3 and p1.Money >= 40:
        return True

    return False

def Inn(p1):

    artwork.showInn()

    print('You burst through the doors of the Inn like you own the place!')
    print()
    time.sleep(2)
    print('Nobody noticed.')

    isPlayerAtInn = True
    while isPlayerAtInn == True:

        print('''
    -= INN MENU =-

    [G]et a Room
    [O]rder a Drink
    [R]ead the Town News

    [L]eave the Inn        
        ''')

        action = input('Command: ').upper()
        
        if action == 'G':
            # Can player afford to stay?
            if PlayerCanStayAtInn(p1):
                isPlayerAtInn = False
                common.DoAction('innStay', p1, None)
            else:
                print('\n"Sorry," says the Innkeeper, "but you don''t have enough to stay."')

        elif action == 'O':
            common.DoAction('innDrink', p1, None)

        elif action == 'R':
            common.DoAction('innTownNews', p1, None)

        elif action == 'L':
            isPlayerAtInn = False

def InnDrink(p1):
    
    print('You take a swig from the big jug...')
    print()
    
    time.sleep(1)
    negativeHealthAmount = random.randint(-5,-1)
    p1.Health = negativeHealthAmount

    print('The room starts to spin. What\'s in thi..s?')
    print('You have lost {} HP. It was worth it though!'.format(abs(negativeHealthAmount)))
    print('Taking another sip, you are now filled with a little more courage!')
    print()

    positiveArmorAmount = random.randint(1,4)
    p1.Armor = positiveArmorAmount
    print('You have gained {} AP !'.format(positiveArmorAmount))

def InnTownNews(p1):
    
    # TODO: Make this a lot more dynamic
    print('WANTED: Rowan McGill wanted for stealing two of Billy Grant''s cows.')
    print('Town Hall: Taxes will be raised 0.002% in February')
    print('Tybalt, the local Blacksmith, is having a special on Armor.')
    print('For Sale: 2 parcels of land for 500 coin')
