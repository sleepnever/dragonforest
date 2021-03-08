import random
import time

from DFModules import artwork

#
# Minigames 
#

# Thimblerig = ball and cup
# Pinfinger: knife game with fingers
# Guess a number

def select_game(p1, game, wager, npcWager):

    if game.lower() == "thimblerig":
        thimblerig(p1, wager, npcWager)

    if game.lower() == "pinfinger":
        pinfinger(p1, wager, npcWager)
    
    if game.lower() == "guess the number":
        guess_the_number(p1, wager, npcWager)

def thimblerig(p1, wager, npcWager):

    artwork.inn_gamble_thimblerig_b()

    print(f'You have to be fast for this game. Keep your eye on the cup with the ball.')

    randomCupFuncList = [artwork.inn_gamble_thimblerig_a, artwork.inn_gamble_thimblerig_b, artwork.inn_gamble_thimblerig_c]
    randCup = random.choice(randomCupFuncList)

    artwork.inn_gamble_thimblerig_end()

    guess = input("Which cup? A, B or C: ")

    randCup()

    # DEBUG
    #foo = randCup.__name__[-1]
    #print(f'Guess = {guess} and answer = {foo}')

    # match guess letter to function end letter
    if guess.upper() == randCup.__name__[-1]:
        print('You Win!')
    else:
        print('You Lose!')

def passedix(p1, wager, npcWager):
    pass

def pinfinger(p1, wager, npcWager):

    artwork.inn_gamble_pinfinger()

    print('''
    \n
    A scraggly man across the table with several missing fingers, slams a dirty and rusted knife on the table.
    You stare at it. You\'ve seen cleaner privy chambers. Here goes...
    ''')

    # 10 fingers
    hitNumFingers = random.randint(1,10)

    # 1 in 10 chance of hitting your finger
    hitNumChance = random.randint(1,10)

    # if speed > someNum, chance of hitting should increase
    # slightly
    speed = random.uniform(0.5,1)

    isFingerHit = False

    #if __debug__:
    #    print(f'DEBUG: Speed={speed}, {hitNumFingers} == {hitNumChance}')

    for _ in range(1,10):
        print(" <tik> ", end='')
        
        time.sleep(speed)
        
        if hitNumFingers == hitNumChance:
            isFingerHit = True
            break

    if isFingerHit:
        print('"Ouuuuuuch!" you yelp in pain. The group roars with laughter.')
        print('Not only did you lose your money, you hurt yourself.')
        p1.Money = (-1 * wager)
        p1.Health = -10
    else:
        print('You won! And you kept all your fingers!')
        p1.Money = wager

        print(f'The group looks at you in amazement. You give a wide smile, grab your winnings of {wager} coin and head out.')
    

def guess_the_number(p1, wager, npcWager):
    
    num = random.randint(1,50)
    theNum = random.randint(2,49)

    print(f'Guess between 1 and {num}...')

    guess = int(input('"Your Guess: '))

    if guess == theNum:
        print(f'"Arrrgh. You\'ve guessed it!", groans the man. "Here take yer winnings."')
        print()
        print(f'You take your {wager} coins and the extra {npcWager} wagered by the others.')
        p1.Money = npcWager
    else:
        print(f'"Ohhh soooo close! Well, not really.", says the man.')
        p1.Money = -1 * (wager + npcWager)