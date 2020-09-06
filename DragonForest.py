#----------------------------
# Dragon Forest
# Text adventure game
# by Rob Watts
# Python 3.7.3
# Updated 9/5/2020
#
# TODO
# -Search code for TODO comments
# -What am I doing with npc.py?
# -Move more long story pieces into textblocks.py (?) or just remove it
# -When player levels up, how to get Armor and new weapons?
# -Story
#   -Need whatever the mystery of the forest is
# -Load game
#   -If save file exists with username, ask to load?
# -Artwork
#   -Some art with \ are spaced incorrectly on the line, like showForest()
# -General
#
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
GAMESAVE_FILE = 'player.ini'

#
# Functions
#

def loadWeaponsFromJson():

    # use a Windows path
    filename = PureWindowsPath("Data\\weapons.json")

    # PathLib will convert the path correctly for the OS
    correctPath = Path(filename)

    with open(correctPath, mode="r") as json_file:
    # object_pairs_hook=OrderedDict will load JSON data in order
        weapons = json.load(json_file, object_pairs_hook=OrderedDict)

    return weapons


def loadEnemiesFromJson():

    # use a Windows path
    filename = PureWindowsPath("Data\\enemies.json")

    correctPath = Path(filename)

    with open(correctPath, mode="r") as json_file:
        enemies = json.load(json_file, object_pairs_hook=OrderedDict)

    return enemies


def loadGame():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),GAMESAVE_FILE)) # TODO: Update to use PathLib

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

def saveGame():

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
        'Xp':p1.Xp),
        'Weapon':p1.Weapon.Name,
        'Money':p1.Money,
        'LastTimeCamped':p1.LastTimeCamped, # can have no value
        'HasDiscoveredTown':p1.HasDiscoveredTown
        }
    
    # TODO: Update to use PathLib
    with open(os.path.join(os.getcwd(),GAMESAVE_FILE),'w') as configFile:
        config.write(configFile)

def luckDragon():

    prize = ['money','health','armor']
    
    if random.randint(1,200) == LUCK_DRAGON_NUMBER:
        print('The mysterious Luck Dragon smiles upon you!')
        
        prizeWon = random.choice(prize)

        if prizeWon == 'money':
            print('It has given you 10 somewhat shiny coins.')
            p1.Money += 10
        elif prizeWon == 'health':
            print('You''ve gained 15 HP.')
            p1.UpdateHealth(15)
        elif prizeWon == 'armor':
            print('You''ve gained 10 AP.')
            p1.UpdateArmor(10)
        
        print()

# random forest events
def IsForestEvent():

    randInt = random.randint(1,100)

    if randInt == 10 and p1.Health < p1.MaxHealth:
        print('You found a bag of apples under a tree, which you greedily eat before the owner returns.')
        print('Feeling fat and happy, and maybe a bit guilty, at least you''ve restored 5 HP')
        print()
        p1.UpdateHealth(5)
        return True

    elif randInt == 20:
        print('So busy looking at everything, except where you are walking!')
        print('You trip over a log, and fall flat on your face, losing 10 HP')
        print()
        p1.UpdateHealth(-10)
        return True

    return False
    # add more


def displayPlayerStats():
    
    print()
    print('-=-=-=-=-=-=-=-=-=-STATS=-=-=-=-=-=-=-=-=-=-=-')
    print('| Player Name     : {}'.format(p1.Name))
    print('| Health (HP)     : {}/{}'.format(p1.Health,p1.MaxHealth))
    print('| Armor  (AP)     : {}/{}'.format(p1.Armor,p1.MaxArmor))
    print('| Weapon / Damage : {} / {}'.format(p1.Weapon.Name, p1.Weapon.Damage))
    print('| Experience (XP) : {}'.format(p1.Xp))
    print('| Coins           : {}'.format(p1.Money))
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print()

def PlayerCanStayAtInn():

    if p1.Level == 1 and p1.Money >= 5:
        return True
    elif p1.Level == 2 and p1.Money >= 25:
        return True
    elif p1.Level == 3 and p1.Money >= 40:
        return True

    return False

def CreateEnemy(playerLevel):

    playerLevelEnemyList = []

    # search through the JSON data to find Enemies that are <= level of the Player
    for enemy in enemyData['enemies']:
        if enemy['level'] <= playerLevel:
            playerLevelEnemyList.append(enemy)
    
    # From the list, randomly choose an enemy
    randomEnemyObj = random.choice(list(playerLevelEnemyList))
    
    return Enemy(randomEnemyObj)


def attack(enemyObj):

    while p1.IsDead() == False and enemyObj.IsDead() == False:
        print()
        print('You swing your {} at the {}'.format(p1.Weapon.Name, enemyObj.Name))

        # Get random damage range values
        p1_damage = random.randint(0, p1.Weapon.Damage)
        enemy_damage = random.randint(0, enemyObj.Damage)

        # Calculate Damage
        p1.CalculateDamage(p1_damage)
        enemyObj.Health = enemyObj.Health - enemy_damage

        # Check if player or enemy is dead
        if (enemyObj.IsDead()):
            print('You hit the {} for {} damage, and killed it!'.format(enemyObj.Name, p1.Weapon.Damage))

            addedXp = random.randint(1, enemyObj.MaxXp)
            p1.AddXp(addedXp)
            print('\n\nYou have gained {} XP'.format(addedXp))

            return
            
        else:
            print('You hit the {} for {} damage! It has {} HP.'.format(enemyObj.Name, enemy_damage, enemyObj.Health))
            
        if (p1.IsDead()):
            print('{} is hit with {} damage and has died! <<GAME OVER>>'.format(p1.Name, str(p1_damage)))
            sys.exit()
        else:
            print('You are hit with {} damage and have {} HP left.'.format(str(p1_damage),str(p1.Health)))

        time.sleep(1)

def camp():

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
    
    addedHealth = random.randint(1,10)

    # don't exceed max health when adding health
    if p1.Health < p1.MaxHealth:
        p1.UpdateHealth(addedHealth)
        print('<Yawwwwn> you lazily wake up, feeling much better. +{} HP gained.'.format(addedHealth))
    else:
        print('<Yawwwwn> you lazily wake up, feeling about the same, but it was a good nap.')

def town():

    artwork.showTown()

    # First time coming into town, show these opening story lines
    if p1.HasDiscoveredTown == False:
        print('Climbing over the rocks and pushing the branches out of the way, you see a town.')
        time.sleep(1)
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

    [G]o to the Inn
    [V]isit Blacksmith
    [T]alk to a Random Stranger
    
    [L]eave Town
        ''')

        action = input('Command: ').upper()
        
        if action == 'G':
            doAction('townInn')

        elif action == 'V':
            doAction('townBlacksmith')

        elif action == 'T':
            doAction('townTalkToNpc')

        elif action == 'L':
            return  # should go back to the main game loop with main menu

def inn():

    artwork.showInn()

    print('You burst through the doors of the Inn like you own the place!')
    print()
    time.sleep(1)
    print('Nobody noticed.')
    print()
    time.sleep(1)

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
            if PlayerCanStayAtInn():
                isPlayerAtInn = False
                doAction('innStay')
            else:
                print('\n"Sorry," says the Innkeeper, "but you don''t have enough to stay.')

        elif action == 'O':
            doAction('innDrink')

        elif action == 'R':
            doAction('innTownNews')

        elif action == 'L':
            isPlayerAtInn = False

def innDrink():
    
    print('You take a swig from the big jug...')
    print()
    
    time.sleep(1)
    negativeHealthAmount = random.randint(-5,-1)
    p1.UpdateHealth(negativeHealthAmount)

    print('The room starts to spin. What\'s in thi..s?')
    print('You have lost {} HP. It was worth it though!'.format(abs(negativeHealthAmount)))
    print('Taking another sip, you are now filled with a little more courage!')
    print()

    positiveArmorAmount = random.randint(1,4)
    p1.UpdateArmor(positiveArmorAmount)
    print('You have gained {} AP !'.format(positiveArmorAmount))

def innTownNews():
    
    # TODO: Make this a lot more dynamic
    print('"Well...", Beatris says, "here\'s what I know."')
    
    print('Gertrude is having some issues, so I would stay clear.')
    print('Tybalt, the local Blacksmith, can fix your armor and weaponry.')
    print('Meric got in a fight with Rowan, but Meric went home sore.')
    # if player took a drink, throw in a funny line like this. Will need a flag in the player class
    print('And I think that drink I gave you was to kill the roaches. I have your drink right here.')

def blacksmith():

    artwork.showBlacksmith()

    print('The Blacksmith sees you approaching, as he hammers on a shiny blade. He starts to grin.')
    time.sleep(1)
    
    if p1.Weapon.Name == "Stick" and p1.Money < 5:
        print('As you move closer, he sees you have nothing. Well, a stick. No armor. No ching-a-ling of coin in your pocket.')    
        time.sleep(1)
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

    [T]alk to Blacksmith
    [W]eapon Purchase/Upgrade
    [A]rmor Purchase/Upgrade

    [L]eave Blacksmith
        ''')

        action = input('Command: ').upper()
        
        if action == 'T':
            pass
        elif action == 'W':
            pass
        elif action == 'A':
            pass
        elif action == 'L':
            return

def exploreForest():

    artwork.showForest()
        
    print('Into the forest you go!')

    if p1.Level == 1 and p1.HasDiscoveredTown == False:
        print('In the distance, you hear people talking and children laughing. You turn right and walk towards the noises.')
        print('You stop in your tracks. A wall of thorny blackberry bushes. You take a deep breath...')
        time.sleep(1)
        print('Oooh! Owwww! Ouch!')
        time.sleep(0.5)
        print('After many more pokes, prods, cuts and yelps, you\'ve found the way to Town.')
        p1.HasDiscoveredTown = True
        return

    if IsForestEvent(): # random things that can help/hurt. If one occurs, exit out of the next piece back to menu
        return

    time.sleep(1)
    print('...listening to the sounds...')
    time.sleep(1)
    print('and looking for anything interesting.')
    print()

    # Random luck lottery
    luckDragon()
    
    # Create enemy based on Player's level
    enemy = CreateEnemy(p1.Level)

    print('A {} {} with {} HP and {} Damage jumps out!'.format(random.choice(enemyAdjectives),enemy.Name, enemy.Health, enemy.Damage))
    print('You grip your {}, with it''s {} Damage.'.format(p1.Weapon.Name, p1.Weapon.Damage))

    print()
    action = input('Do you want to attack? Y/N: ').upper()
    print()

    if action == 'Y':

        # Call Attack
        attack(enemy)

        # Fight is over
        print('\nThe fight has left you with {}/{} HP'.format(p1.Health,p1.MaxHealth))

    else:

        print('You back up.')
        time.sleep(2)
        print('...slowly...')
        time.sleep(2)
        print('and RUN AWAY to saftey!')

def showHelp():

    print('''
    [GAME HELP]

    Forest
        Exploring the Forest allows you to gain eXPerience points and level up. Random events may
        occur to help or hinder.

    Camping
        Regain some Health Points by taking a short snooze.

    Town
        Explore the offerings, including the Inn and Blacksmith. The Inn will allow you to Save your
        Game by purchasing a night's stay, while the Blacksmith will help you upgrade your Weapons
        and Armor. 
    
    ''')

def doAction(action):

    if action == 'talk':
        # do something.. need function/module for NPCs
        print('TODO: run into random NPC in forest, hear a story/get info')
        
    elif action == 'exploreForest':
        exploreForest()

    elif action == 'stats':
        displayPlayerStats()

    elif action == 'camp':
        camp()

    elif action == 'town':
        town()

    elif action == 'townInn':
        inn()

    elif action == 'townBlacksmith':
        blacksmith()

    elif action == 'innStay':
        print('You head to your room. Its not much and there is a funny smell, but it will suffice.')
        saveGame()
        sys.exit()

    elif action == 'innDrink':
        innDrink()

    elif action == 'innTownNews':
        innTownNews()
    
    elif action == 'help':
        showHelp()
        

#---------------------------
#       Game Start
#--------------------------

exitGame = False

artwork.showTitle()
textblocks.showIntro()

playerName = input('What is thy name? ')

if playerName == '' or len(playerName) < 1:
    sys.exit()

# Create player
p1 = Player(playerName, loadWeaponsFromJson())

# Load the enemy data
enemyData = loadEnemiesFromJson()

# Load Game -- TODO: if player.ini exists, load. If not, ask for name
#                     and create the file
#loadGame()

# Display Stats
displayPlayerStats()

#
# GAME LOOP
#
while exitGame == False:

    p1.UpdateLevel()

    if p1.Level >= 1 and p1.HasDiscoveredTown == True:
        print('''
    -= MENU =-
        
    [E]xplore the Forest           [S]tats
    [C]amp                         [H]elp
    [T]own

    [Q]uit.
        
        ''')
    else:
        print('''
    -= MENU =-
    
    [E]xplore the Forest         [S]tats
    [C]amp                       [H]elp

    [Q]uit.
        
        ''')


    command = input('Command: ').upper()

    if command == 'E':
        doAction('exploreForest')
        
    elif command == 'C':
        doAction('camp')

    elif command == 'S':
        doAction('stats')

    elif command == 'H':
        doAction('help')

    elif command == 'T' and p1.HasDiscoveredTown:
        doAction('town')

    elif command == 'Q':
        exitGame = True

    elif command == 'D':
            p1.AddXp(30)
            p1.Money += 30
            p1.HasDiscoveredTown = True
