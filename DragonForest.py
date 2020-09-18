#----------------------------
# Dragon Forest
# Text adventure game
# by Rob Watts
# Python 3.7.3
# Updated 9/17/2020
#
# TODO
# -Story
#   -Need whatever the mystery of the forest is
# -Load game
#   -If save file exists with username, ask to load?
#   -If StayedAtInn=True, give a random amount of health and armor boost, else take some HP away
#    for sleeping out in the cold with the animals and bugs
# -Artwork
#   -Some art with \ are spaced incorrectly on the line, like showForest()
# -General
#   -Search code for TODO/HACK/BUG comments
#   -What am I doing with npc.py?
#   -Move more long story pieces into textblocks.py (?) or just remove it
#----------------------------

# Python Libraries
import random
import sys
import time
import math
import datetime
import configparser
import os
from datetime import timedelta

# for JSON loading
import json
from collections import OrderedDict
from pathlib import Path, PureWindowsPath

# My Custom Game Modules
from DFModules import artwork
from DFModules import textblocks
from DFModules.player import Player
from DFModules.enemy import Enemy

# Global strings # TODO: put elsewhere
enemyAdjectives = ['growling','angry','crazy','wild','cranky','hangry','scared','rabid','mean','scary','fierce','irritable','ferocious']
noCampingStrings = ['You can''t camp all day, go do something!','Such a shame you have no wood for the fire.','There''s bear crap everywhere!! Look elsewhere.']

# Constants
MAX_TIME_BETWEEN_CAMP_MINUTES = 5
LUCK_DRAGON_NUMBER = 13 # if the rand gen picks 13, get a prize in the forest
CONFIG_FILE = 'configData.ini'
GAMESAVE_FILE = 'playerSave.ini'

#
# Functions
#

def LoadDataFromJson(filepath, openMode, isOrderedDict=True):

    # use a Windows path
    filename = PureWindowsPath(filepath)

    correctPath = Path(filename)

    with open(correctPath, mode=openMode) as json_file:
        if isOrderedDict:
            jsonData = json.load(json_file, object_pairs_hook=OrderedDict)
        else:
            jsonData = json.load(json_file)

    return jsonData


def LoadGame(p1):

    # TODO: Update to use PathLib
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),GAMESAVE_FILE))

    p1.Name = config['PLAYER']['Name']
    p1.Level = config['PLAYER']['Level']
    p1.MaxHealth = config['PLAYER']['MaxHealth']
    p1.Health = config['PLAYER']['Health']
    p1.MaxArmor = config['PLAYER']['MaxArmor']
    p1.Armor = config['PLAYER']['Armor']
    p1.Xp = config['PLAYER']['Xp']
    p1.Weapon.Name = config['PLAYER']['Weapon']
    p1.Money = config['PLAYER']['Money']
    p1.LastTimeCamped = config['PLAYER']['LastTimeCamped']
    p1.HasDiscoveredTown = config['PLAYER']['HasDiscoveredTown']
    p1.StayedAtInn = config['PLAYER']['StayedAtInn']
    p1.Level1BonusReceived = config['PLAYER']['Level1BonusReceived']
    p1.Level2BonusReceived = config['PLAYER']['Level2BonusReceived']
    p1.Level3BonusReceived = config['PLAYER']['Level3BonusReceived']
    p1.Level4BonusReceived = config['PLAYER']['Level4BonusReceived']

def SaveGame(p1):

    print('< Saving Game >')
    # allow_no_value bug: https://github.com/ralphbean/bugwarrior/pull/600
    config = configparser.ConfigParser(allow_no_value=True)

    config['PLAYER'] = {
        'Name':p1.Name,
        'Level':p1.Level,
        'MaxHealth':p1.MaxHealth,
        'Health':p1.Health,
        'MaxArmor':p1.MaxArmor,
        'Armor':p1.Armor,
        'Xp':p1.Xp,
        'Weapon':p1.Weapon.Name,
        'Money':p1.Money,
        'LastTimeCamped':p1.LastTimeCamped, # can have no value
        'HasDiscoveredTown':p1.HasDiscoveredTown,
        'StayedAtInn':p1.StayedAtInn, # did the player stay at the inn (save game)? reset to False on load
        'Level1BonusReceived':p1.Level1BonusReceived,
        'Level2BonusReceived':p1.Level2BonusReceived,
        'Level3BonusReceived':p1.Level3BonusReceived,
        'Level4BonusReceived':p1.Level4BonusReceived
        }
    
    # TODO: Update to use PathLib
    with open(os.path.join(os.getcwd(),GAMESAVE_FILE),'w') as saveFile:
        config.write(saveFile)

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

# random forest events
def IsForestEvent(p1):

    randInt = random.randint(1,100)

    if randInt == 10 and p1.Health < p1.MaxHealth:
        print('You found a bag of apples under a tree, which you greedily eat before the owner returns.')
        print('Feeling fat and happy, and maybe a bit guilty, at least you''ve restored 5 HP')
        print()
        p1.Health = 5
        return True

    elif randInt == 20:
        print('So busy looking at everything, except where you are walking!')
        print('You trip over a log, and fall flat on your face, losing 10 HP')
        print()
        p1.Health = -10
        return True
    
    elif randInt == 98:
        print('Suddenly a giant fluffy bunny with floppy ears appears on a rock in front of you.')
        print('He blinks and out of no where says "HEY! I''m Vlad, the Magical Cookie Bunny!"')
        print('You stand there stunned, but even more so as he hands you a giant chocolate chip cookie worth 15 HP.')
        print()
        p1.Health = 15

    return False
    # add more


def DisplayPlayerStats(p1):
    
    print()
    print('-=-=-=-=-=-=-=-=-=-STATS=-=-=-=-=-=-=-=-=-=-=-')
    print('|')
    print('| Player Name     :  {}'.format(p1.Name))
    print('| Health (HP)     :  {}/{}'.format(p1.Health,p1.MaxHealth))
    print('| Armor  (AP)     :  {}/{}'.format(p1.Armor,p1.MaxArmor))
    print('| Weapon / Damage :  {} / {}'.format(p1.Weapon.Name, p1.Weapon.Damage))
    print('| Experience (XP) :  {}'.format(p1.Xp))
    print('| Gold Coins      :  {}'.format(p1.Money))
    print('|')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print()

def PlayerCanStayAtInn(p1):

    if p1.Level == 1 and p1.Money >= 5:
        return True
    elif p1.Level == 2 and p1.Money >= 25:
        return True
    elif p1.Level == 3 and p1.Money >= 40:
        return True

    return False

def CreateEnemy(p1, enemyData):

    playerLevelEnemyList = []

    # search through the JSON data to find Enemies that are <= level of the Player
    for enemy in enemyData['enemies']:
        if enemy['level'] <= p1.Level:
            playerLevelEnemyList.append(enemy)
    
    # From the list, randomly choose an enemy
    randomEnemyObj = random.choice(list(playerLevelEnemyList))
    
    return Enemy(randomEnemyObj)

def Attack(p1, enemyObj):

    while p1.IsDead() == False and enemyObj.IsDead() == False:
        print()
        print('You swing your {} at the {}'.format(p1.Weapon.Name, enemyObj.Name))

        # Get random damage range values from 0 to upper values
        p1_damageGiven = random.randint(0, p1.Weapon.Damage) # how much player deals
        enemy_damageGiven = random.randint(0, enemyObj.Damage) # how much enemy deals

        # Enemy's damage taken from player
        # #TODO: enemy could have armor, so use the player function and generalize it
        enemyObj.Health = (-1 * p1_damageGiven)

        # Check if player or enemy is dead
        if (enemyObj.IsDead()):
            print('You hit the {} for {} damage, and killed it!'.format(enemyObj.Name, p1_damageGiven))

            addedXp = random.randint(1, enemyObj.MaxXp)
            p1.Xp = addedXp
            print('\n\nYou have gained {} XP!'.format(addedXp))

            return
            
        else:
            print('You hit the {} for {} damage! It has {} HP.'.format(enemyObj.Name, p1_damageGiven, enemyObj.Health))

        # Calculate Player's Damage taken from enemy, factoring in armor
        enemy_damageGiven = p1.CalculateDamageTaken(enemy_damageGiven)

        if (p1.IsDead()):
            print('{} is hit with {} damage and has died! <<GAME OVER>>'.format(p1.Name, enemy_damageGiven))
            sys.exit()
        else:
            print('You are hit with {} damage and have {} HP left.'.format(enemy_damageGiven, p1.Health))

        time.sleep(1)

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
    
    print('Z',end='')
    for _ in range(10): # changed i -> _ which is a python throwaway var
        print('z',end='')
        time.sleep(0.5)
        
    print()

    # Set date time camped
    p1.LastTimeCamped = datetime.datetime.now()
    
    addedHealth = random.randint(3,10)

    # don't exceed max health when adding health
    if p1.Health < p1.MaxHealth:
        p1.Health = addedHealth
        print('<Yawwwwn> you lazily wake up, feeling much better. +{} HP gained.'.format(addedHealth))
    else:
        print('<Yawwwwn> you lazily wake up, feeling about the same, but it was a good nap.')

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
            DoAction('townInn', p1, None)

        elif action == 'B':
            DoAction('townBlacksmith', p1, None)

        elif action == 'T':
            DoAction('townTalkToNpc', p1, None)

        elif action == 'L':
            return  # should go back to the main game loop with main menu

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
                DoAction('innStay', p1, None)
            else:
                print('\n"Sorry," says the Innkeeper, "but you don''t have enough to stay."')

        elif action == 'O':
            DoAction('innDrink', p1, None)

        elif action == 'R':
            DoAction('innTownNews', p1, None)

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

def Blacksmith(p1):

    artwork.showBlacksmith()

    print('The Blacksmith sees you approaching, as he hammers on a shiny blade. He starts to grin.')
    time.sleep(1)
    
    if p1.Weapon.Name == "Stick":
        print('As you move closer, he sees you have nothing. Well, a stick. No armor. Nary a ching-a-ling of coin in your pocket.')    
        time.sleep(2)
        print('His facial expression goes soft. You stop short and wonder if you should just go find another stick.')
        print('You look down at your torn clothes (stupid raccoon), and that big scratch on your arm (crazy squirrel).')
        print()
        print('No, you need something. Anything really...')
        print()
    else:
        print('"Ahhh back again I see!"')

    isPlayerAtBlacksmith = True
    while isPlayerAtBlacksmith == True:

        print('''
    -= BLACKSMITH MENU =-

    [W]eapon Purchase
    [A]rmor Upgrade

    [L]eave Blacksmith
        ''')

        action = input('Command: ').upper()
        
        if action == 'W':
            DoAction('blacksmithWeapons', p1, None)
        elif action == 'A':
            DoAction('blacksmithArmorUpgrade', p1, None)
        elif action == 'L':
            return

def BlacksmithWeapons(p1):

    print('Welcome to my Armory wall. This is what I have for purchase. Coin only.')
    print()
    print('<===|- WEAPONS -|===>')
    print()
    
    # this is the dynamic 2 column method, but it only works with even lists
    # and it still has numbering issues, so I'm skipping for my other solution
    # which includes damage and cost
    '''
    bsmithWeapons = []
    
    for weapon in p1.WeaponData['weapons']:
        bsmithWeapons.append(weapon['name'])
    
    # Don't want the user to be able to buy their starting Weapon
    bsmithWeapons.remove("Stick")

    bsmithWeaponsCount = len(bsmithWeapons)

    # NOTE: In 3.x, / gives a float, not an int. Need // #
    indexCol1 = 0 # TODO: index of column 1 should start at 1
    indexCol2 = math.ceil(bsmithWeaponsCount//2) # index column2 starts at len(list)/2 + 1

    # TODO: I cannot figure out an odd numbered list properly.
    # HACK: just use an even number of weapons in weapons.json for now

    # slice list based on even or odd num of items
    #if len(bsmithWeapons) % 2 == 0:
    #    col2 = bsmithWeaponsCount//2
    #else:
    #    col2 = math.ceil(bsmithWeaponsCount//2)

    col2 = bsmithWeaponsCount//2

    # slice list into 2 columns using zip() function
    for left,right in zip(bsmithWeapons[::1],bsmithWeapons[col2::]):
        print('[{}] {:<12} [{}] {:<12}'.format(indexCol1,left,indexCol2,right))

        # increment the column indexes manually
        indexCol1 += 1
        indexCol2 += 1
    '''

    print('NAME                    DAMAGE   COST')
    
    weaponDict = {}
    for idx, weapon in enumerate(p1.WeaponData['weapons']):
        
        # don't show the default 'stick'
        if idx == 0:
            continue

        weaponDict[idx] = weapon['name']
        print('[{}] {:<20} {}       {}'.format(idx, weapon['name'],weapon['damage'],weapon['cost']))

    print('\n[E]xit Buy Menu')

    command = input('\nCommand: ').upper()

    if command == 'E':
        pass

    elif int(command) in range(1,len(p1.WeaponData['weapons'])):
        
        #weaponName = bsmithWeapons[int(command)]
        weaponName = weaponDict.get(int(command))

        # player can purchase
        if p1.BuyWeapon(weaponName):
            print('You purchased a {}'.format(weaponName))
        else:
            print('You do not have enough money.')

def BlacksmithArmorUpgrade(p1):

    print('''   
             __________
             |  ARMOR  |
             |         |
              \\______/
    ''')
    print('Current Coin : {}'.format(p1.Money))
    print('Current Armor: {}'.format(p1.Armor))

    if p1.Armor != p1.MaxArmor:
        
        upgradeCost = ((p1.Xp * 2) * random.randint(1,3))
        upgradeAmount = (p1.Xp + p1.Armor)
        
        print('Upgrade Cost : {} coin for {} AP'.format(upgradeCost, upgradeAmount))

        action = input('\nDo you want to upgrade? Y/N: ').upper()    

        if action == 'Y':
            if p1.UpgradeArmor(upgradeCost, upgradeAmount):
                print('\n"Enjoy your armor and your lighter pocket!", laughs the Blacksmith.')
            else:
                print('"Come back when you have more money...", groans the Blacksmith.')
                randInt = random.randint(1,50)
                if randInt == 20:
                    print('''
                    <THWACK>
                    
                    Something hard hit you in the back of the head. Rubbing your sore spot, you
                    look down to find a shiny coin. What the...?
                    
                    ''')
                    print('"Penny for your thoughts! Get it?!", the Blacksmith says with a crude smile.')
                    p1.Money = 1

    else:
        print('Your Armor is already at Max.')


def ExploreForest(p1, enemyData):

    artwork.showForest()
        
    print('Into the forest you go!')

    if p1.Level == 1 and p1.HasDiscoveredTown == False:
        textblocks.showTownDiscovery()
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
    enemy = CreateEnemy(p1, enemyData)

    print('A {} {} with {} HP and {} Damage jumps out!'.format(random.choice(enemyAdjectives),enemy.Name, enemy.Health, enemy.Damage))
    print('You grip your {}, with it''s {} Damage.'.format(p1.Weapon.Name, p1.Weapon.Damage))

    print()
    action = input('Do you want to attack? Y/N: ').upper()
    print()

    if action == 'Y':

        # Call Attack
        Attack(p1, enemy)

        p1.LevelUp()

    else:

        print('You back up.')
        time.sleep(2)
        print('...slowly...')
        time.sleep(2)
        print('and RUN AWAY to saftey!')


def DoAction(action, playerObj, enemyData):

    if action == 'talk':
        # do something.. need function/module for NPCs
        print('TODO: run into random NPC in forest, hear a story/get info')
        
    elif action == 'exploreForest':
        ExploreForest(playerObj, enemyData)

    elif action == 'stats':
        DisplayPlayerStats(playerObj)

    elif action == 'camp':
        Camp(playerObj)

    elif action == 'town':
        Town(playerObj)

    elif action == 'townInn':
        Inn(playerObj)

    elif action == 'townBlacksmith':
        Blacksmith(playerObj)

    elif action == 'blacksmithWeapons':
        BlacksmithWeapons(playerObj)

    elif action == 'blacksmithArmorUpgrade':
        BlacksmithArmorUpgrade(playerObj)

    elif action == 'innStay':
        print('You head to your room. Its not much and there is a funny smell, but it will suffice.')
        playerObj.StayedAtInn = True
        SaveGame(playerObj)

        sys.exit()

    elif action == 'innDrink':
        InnDrink(playerObj)

    elif action == 'innTownNews':
        InnTownNews(playerObj)
    
    elif action == 'help':
        textblocks.showHelp()


#---------------------------
#       Game Start
#--------------------------

def main():

    exitGame = False

    artwork.showTitle()
    textblocks.showIntro()

    playerName = input('What is thy name? ')

    if playerName == '' or len(playerName) < 1:
        sys.exit()

    # TODO: LoadGame() if <condition> exists. If not, ask for name and create the file

    # Load the weapon data
    weaponData = LoadDataFromJson("Data\\weapons.json", "r")

    # Load the enemy data
    enemyData = LoadDataFromJson("Data\\enemies.json", "r")

    # Create Player
    p1 = Player(playerName, weaponData)

    # Display Stats
    DisplayPlayerStats(p1)

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
            DoAction('exploreForest', p1, enemyData)
            
        elif command == 'C':
            DoAction('camp', p1, None)

        elif command == 'S':
            DoAction('stats', p1, None)

        elif command == 'H':
            DoAction('help', None, None)

        elif command == 'T' and p1.HasDiscoveredTown:
            DoAction('town', p1, None)

        elif command == 'Q':
            exitGame = True

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