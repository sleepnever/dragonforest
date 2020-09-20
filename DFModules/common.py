
import sys

# Game Modules
from DFModules import blacksmith
from DFModules import forest
from DFModules import inn
from DFModules import town
from DFModules import dataHelper

#
# Functions that are common to all modules
#

def DoAction(action, playerObj, enemyData):

    if action == 'talk':
        # do something.. need function/module for NPCs
        print('TODO: run into random NPC in forest, hear a story/get info')
        
    elif action == 'exploreForest':
        forest.ExploreForest(playerObj, enemyData)

    elif action == 'stats':
        DisplayPlayerStats(playerObj)

    elif action == 'camp':
        forest.Camp(playerObj)

    elif action == 'town':
        town.Town(playerObj)

    elif action == 'townInn':
        inn.Inn(playerObj)

    elif action == 'townBlacksmith':
        blacksmith.Blacksmith(playerObj)

    elif action == 'blacksmithWeapons':
        blacksmith.BlacksmithWeapons(playerObj)

    elif action == 'blacksmithArmorUpgrade':
        blacksmith.BlacksmithArmorUpgrade(playerObj)

    elif action == 'innStay':
        print('You head to your room. Its not much and there is a funny smell, but it will suffice.')
        playerObj.StayedAtInn = True
        dataHelper.SaveGame(playerObj)

        sys.exit()

    elif action == 'innDrink':
        inn.InnDrink(playerObj)

    elif action == 'innTownNews':
        inn.InnTownNews(playerObj)
    
    elif action == 'help':
        showHelp()


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