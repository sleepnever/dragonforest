# System
import time
import random
import math
import datetime

# Game Modules
from DFModules import artwork
from DFModules import combat
from DFModules.enemy import Enemy

# Gobals
MAX_TIME_BETWEEN_CAMP_MINUTES = 5
LUCK_DRAGON_NUMBER = 13 # if the rand gen picks 13, get a prize in the forest
enemyAdjectives = ['growling','angry','crazy','wild','cranky','hangry','scared','rabid','mean','scary','fierce','irritable','ferocious']
noCampingStrings = ['You can''t camp all day, go do something!','Such a shame you have no wood for the fire.','There''s bear crap everywhere!! Look elsewhere.']

#
# Functions that pertain to exploring the forest
#

def ExploreForest(p1, enemyData):

    artwork.showForest()
        
    print('Into the forest you go!')

    if p1.Level == 1 and p1.HasDiscoveredTown == False:
        
        print('''
        In the distance, you hear people talking and children laughing. You turn right and walk towards the noises.
        You stop in your tracks. A wall of thorny blackberry bushes. You take a deep breath...
        
        Oooh! Owwww! Ouch!

        After many more pokes, prods, cuts and yelps, you\'ve found the way to Town.
        ''')

        p1.HasDiscoveredTown = True
        
        return

    # random things that can help/hurt
    if IsForestEvent(p1):
        return

    time.sleep(1)
    print('...listening to the sounds...')
    time.sleep(1)
    print('and looking for anything interesting to fight..')
    print()

    # Random luck lottery
    LuckDragon(p1)
    
    # Create enemy based on Player's level
    enemy = Enemy.CreateEnemyByPlayerLevel(p1.Level, enemyData)

    print(f'A {random.choice(enemyAdjectives)} {enemy.Name} with {enemy.Health} HP and {enemy.Damage} Damage jumps out!')
    print(f'You grip your {p1.Weapon.Name}, with it\'s {p1.Weapon.Damage} Damage.')

    print()
    action = input('Do you want to attack? Y/N: ').upper()
    print()

    if action == 'Y':

        # Call Attack
        combat.Attack(p1, enemy)

        currentLevel = p1.Level
        p1.LevelUp()
        newLevel = p1.Level

        if newLevel > currentLevel:
            print('\nYou have Leveled Up!')

    else:

        print('You back up.')
        time.sleep(2)
        print('...slowly...')
        time.sleep(2)
        print('and RUN AWAY to saftey!')

# random forest events
def IsForestEvent(p1):

    randInt = random.randint(1,100)

    # Gain health
    if randInt == 10 and p1.Health < p1.MaxHealth:
        print('You found a bag of apples under a tree, which you greedily eat before the owner returns.')
        print('Feeling fat and happy, and maybe a bit guilty, at least you''ve restored 5 HP')
        print()
        p1.Health = 5
        return True

    # Trip and hurt self
    elif randInt == 20:
        print('So busy looking at everything, except where you are walking!')
        print('You trip over a log, and fall flat on your face, losing 10 HP')
        print()
        p1.Health = -10
        return True
    
    # Get robbed w/ some complexity
    elif randInt == 30:
        print('\t"HALT!" says a voice from the bushes. You freeze in your tracks. A gang emerges.')
        if p1.Weapon.Name == "Stick":
            print('''
            You hold up your Stick, and swing it to keep them at a distance. They start laughing.
            
            "Look everyone!, he's going to beat us off with his fishing pole!" says the gangly one.

            A fishing pole... that's a great idea you think. And then as you're daydreaming of fish,
            you take a punch to the stomach. Ooof!
            ''')
            if p1.Money >= 5:
                print('''
            Some coins fall out of your pocket. Another member kicks you and steals them as they 
            run away. You are a little bruised and missing some money, but it could have been 
            worse. Now about that fish...
                ''')
                p1.Money = -3
            elif p1.Money == 0:
                print('''
                Its a good thing you didn't have any money for them to steal. They may have tried to
                beat you for all of it.
                ''')
        else:
            print(f'You hold up your {p1.Weapon.Name}, and swing it to keep them at a distance.')
            if p1.Weapon.Name != "Dragon Bone Sword":
                print(f'The gang brandish a variety of weapons and you realize you are outnumbered, even with your {p1.Weapon.Name}.')
                if p1.Money >= 10:
                    moneyToToss = random.randint(10,p1.Money)
                    print(f'In a quick decision, you reach into your pocket and pull out {moneyToToss} coins and throw them into the air. And RUN.')
                    p1.Money = (-1 * moneyToToss)
        return True

    elif randInt == 98:
        print('Suddenly a giant fluffy bunny with floppy ears appears on a rock in front of you.')
        print('He blinks and out of no where says "HEY! I\'m Vlad, the Magical Cookie Bunny!"')
        print('You stand there stunned, but even more so as he hands you a giant chocolate chip cookie worth 15 HP.')
        print()
        p1.Health = 15

    return False
    # add more

def LuckDragon(p1):

    prize = ['money','health','armor']
    
    if random.randint(1,200) == LUCK_DRAGON_NUMBER:
        print('The mysterious Luck Dragon smiles upon you!')
        
        prizeWon = random.choice(prize)

        if prizeWon == 'money':
            print('It has given you 25, somewhat, shiny coins.')
            p1.Money = 25
            
        elif prizeWon == 'health':
            print('You''ve gained 25 HP.')
            p1.Health = 25

        elif prizeWon == 'armor':
            print('You''ve gained 20 AP.')
            p1.Armor = 20
        
        print()

def Camp(p1):

    # Check to see if it's been at least MAX_TIME_BETWEEN_CAMP_MINUTES
    # since last camp to prevent +HP abuse
    if p1.LastTimeCamped != None:
        currentDT = datetime.datetime.now()
        timeDelta = currentDT - p1.LastTimeCamped
        
        if ((timeDelta.seconds/60) < MAX_TIME_BETWEEN_CAMP_MINUTES):
            print(random.choice(noCampingStrings))
            return

    artwork.showCamp()

    print('You decide this is a good place to camp for a while.')
    
    # BUG: within VSCode this properly Zzzzz's but in terminal it pauses for 10 and then prints Zzzzz
    # and the while loop below does the same thing.
    print('Z',end='')
    for _ in range(10): # changed i -> _ which is a python throwaway var
        print('z',end='')
        time.sleep(0.5)
    
    #campTimer = 10
    #while campTimer > 0:
    #    print('z',end='')
    #    campTimer -= 1
    #    time.sleep(0.5)

    print()

    # Set date time camped
    p1.LastTimeCamped = datetime.datetime.now()
    
    addedHealth = random.randint(3,10)

    # don't exceed max health when adding health
    if p1.Health < p1.MaxHealth:
        p1.Health = addedHealth
        print(f'<Yawwwwn> you lazily wake up, feeling much better. +{addedHealth} HP gained.')
    else:
        print('<Yawwwwn> you lazily wake up, feeling about the same, but it was a good nap.')