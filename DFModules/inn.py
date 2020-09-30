import random
import time

# Game Modules
from DFModules import artwork
from DFModules import common
from DFModules import minigames

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

    [G]amble
    [O]rder a Drink
    [S]tay the Night
    [R]ead the Town News

    [L]eave the Inn        
        ''')

        action = input('Command: ').upper()
        
        if action == 'G':
            common.DoAction('innGamble', p1, None)

        elif action == 'S':
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
    print(f'You have lost {abs(negativeHealthAmount)} HP. It was worth it though!')
    print('Taking another sip, you are now filled with a little more courage!')
    print()

    positiveArmorAmount = random.randint(1,4)
    p1.Armor = positiveArmorAmount
    print(f'You have gained {positiveArmorAmount} AP !')

def InnTownNews(p1):
    
    # TODO: Make this a lot more dynamic
    print('WANTED: Rowan McGill wanted for stealing two of Billy Grant''s cows.')
    print('Town Hall: Taxes will be raised 0.002% in February')
    print('Tybalt, the local Blacksmith, is having a special on Armor.')
    print('For Sale: 2 parcels of land for 500 coin')

# TODO: Refactor
def InnGamble(p1):
    
    # Thimblerig = ball and cup
    # Passe-dix: dice game
    # Highest Points: dice game (2 player), roll and highest num wins
    # Pinfinger: knife game with fingers
    # Guess a number
    gameList = ['Thimblerig','Passe-dix', 'Highest Points', 'Pinfinger', 'Guess the Number']
    game = random.choice(gameList)

    print('You hear some shouting in the far corner of the room, "DOUBLE OR NOTHING!", and decide to check it out.')
    print(f'You walk up to a group of men playing "{game}" and a large pile of coins in the middle of the table.')
    print('"Hey fella", says one of the men standing around the table, "you interested in a bit of a gamble?"')

    action = input('Command (Y/N): ').upper()

    if action == 'Y':
        actionWager = int(input('"Great! What\'s yer wager?: ').upper())

        if actionWager <= p1.Money:
            print(f'You toss {actionWager} coins on to the table and have a seat.')
            minigames.Pinfinger(p1, game, actionWager)
        else:
            print(f'You can\'t wager {actionWager} when you only have {p1.Money}')
    
    else:
        print('Come back anytime!')
