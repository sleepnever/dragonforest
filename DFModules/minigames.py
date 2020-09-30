import random
import time

from DFModules import artwork

#
# Minigames 
#

# TODO: Refactor
def Pinfinger(p1, game, wager):

    artwork.InnGamblePinfinger()

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

    if __debug__:
        print(f'DEBUG: Speed={speed}, {hitNumFingers} == {hitNumChance}')

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
    
    # This should be a random event, and random pot money number
    #print('As you get up and start to walk away, you hear "Double or nothing. And I\'ll even throw in my pot of {}.')

def Passedix():
    pass

def HighPoints():
    pass

def GuessTheNumber():
    pass