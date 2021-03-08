import random
import time

# Game Modules
from DFModules import artwork
from DFModules import common
from DFModules import minigames

#
# Functions related to the Inn
#

def player_can_stay_at_inn(p1):

    if p1.Level == 1 and p1.Money >= 5:
        return True
    elif p1.Level == 2 and p1.Money >= 25:
        return True
    elif p1.Level == 3 and p1.Money >= 40:
        return True

    return False

def inn(p1):

    artwork.show_inn()

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
    [T]alk to the Inn Keeper

    [L]eave the Inn        
        ''')

        action = input('Command: ').upper()
        
        if action == 'G':
            common.do_action('innGamble', p1, None)

        elif action == 'S':
            # Can player afford to stay?
            if player_can_stay_at_inn(p1):
                isPlayerAtInn = False
                common.do_action('innStay', p1, None)
            else:
                print('\n"Sorry," says the Innkeeper, "but you don''t have enough to stay."')

        elif action == 'O':
            common.do_action('innDrink', p1, None)

        elif action == 'R':
            common.do_action('innTownNews', p1, None)

        elif action == 'T':
            common.do_action('innTalkInnkeeper', p1, None)

        elif action == 'L':
            isPlayerAtInn = False

def inn_drink(p1):
    
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

def inn_town_news(p1):
    
    print('------------------------------------------------------------------------')
    print()
    print('WANTED: Rowan McGill wanted for stealing two of Billy Grant''s cows.')
    print('Town Hall: Taxes will be raised 0.002% in February')
    print('Tybalt, the local Blacksmith, is having a special on Armor.')
    print('For Sale: 2 parcels of land for 500 coin')
    print()
    print('------------------------------------------------------------------------')


def inn_gamble(p1):
    
    gameList = ['Thimblerig', 'Pinfinger', 'Guess the Number']
    time.sleep(1)
    game = random.choice(gameList)

    print('You hear some shouting in the far corner of the room, "DOUBLE OR NOTHING!", and decide to check it out.')
    print(f'You walk up to a group of men playing "{game}" and a large pile of coins in the middle of the table.')
    print('"Hey fella", says one of the men standing around the table, ", you interested in a bit of a gamble?"')

    action = input('Command (Y/N): ').upper()

    if action == 'Y':
        actionWager = int(input('"Great! What\'s yer wager?: ').upper())

        if actionWager <= p1.Money:
            print(f'You toss {actionWager} coins on to the table and have a seat The other\'s toss in a few as well.')
            npcWagerAmount = random.randint(2,15)

            minigames.select_game(p1, game, actionWager, npcWagerAmount)
        else:
            print(f'You can\'t wager {actionWager} when you only have {p1.Money}')
    
    else:
        print('Come back anytime!')

def talk_inn_keeper(p1):
    print('''
    You see the Inn Keeper sitting at the end of the bar. You know its him by the disgruntled look on his face.
    
    "Are you Scotty?" you ask nervously. "Maybe.", he says looking straight ahead without a single care.

    "Uh, nevermind", you reply and walk away. "Sounds good", he says with a grin. 
    ''')