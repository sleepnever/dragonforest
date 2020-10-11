import random
import sys

# Game Modules
from DFModules import blacksmith
from DFModules import forest
from DFModules import inn
from DFModules import town
from DFModules import dragon
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

    elif action == 'townTalkToNpc':
        town.TalkTownNpc()

    elif action == 'townBlacksmith':
        blacksmith.Blacksmith(playerObj)

    elif action == 'blacksmithWeapons':
        blacksmith.BlacksmithWeapons(playerObj)

    elif action == 'blacksmithArmorUpgrade':
        blacksmith.BlacksmithArmorUpgrade(playerObj)
    
    elif action == 'blacksmithSpecialAction':
        blacksmith.BlacksmithSpecial(playerObj)

    elif action == 'innGamble':
        inn.InnGamble(playerObj)

    elif action == 'innStay':
        print('You head to your room. Its not much and there is a funny smell, but it will suffice.')
        playerObj.StayedAtInn = True
        dataHelper.SaveGame(playerObj)

        sys.exit()

    elif action == 'innDrink':
        inn.InnDrink(playerObj)

    elif action == 'innTownNews':
        inn.InnTownNews(playerObj)
    
    elif action == 'innTalkInnkeeper':
        inn.TalkInnkeeper(playerObj)
    
    elif action == 'dragoncave':
        dragon.cave(playerObj)

    elif action == 'help':
        DisplayHelp()


def DisplayPlayerStats(p1):
    
    print()
    print('-=-=-=-=-=-=-=-=-=-STATS=-=-=-=-=-=-=-=-=-=-=-')
    print('|')
    print(f'| Player Name     :  {p1.Name}')
    print(f'| Health (HP)     :  {p1.Health}/{p1.MaxHealth}')
    print(f'| Armor  (AP)     :  {p1.Armor}/{p1.MaxArmor}')
    print(f'| Weapon / Damage :  {p1.Weapon.Name} / {p1.Weapon.Damage}')
    print(f'| Experience (XP) :  {p1.Xp}')
    print(f'| Gold Coins      :  {p1.Money}')
    print('|')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print()

def DisplayHelp():

    print('''
    -=-=-= GAME HELP =-=-=-

    -Forest
        Exploring the Forest allows you to gain eXPerience points and level up. Random events may
        occur to help or hinder.

    -Camping
        Regain some Health Points by taking a short snooze.

    -Town
        Explore the offerings, including the Inn and Blacksmith. The Inn will allow you to Save your
        Game by purchasing a night's stay, while the Blacksmith will help you upgrade your Weapons
        and Armor.

        --The Inn
            The Inn offers a variety of things to do, including the ability to stay the night (Save).
        
        --Blacksmith
            Upgrade your Armor and buy new Weapons.
    
    -Leveling Up
        You start the game with no Level. Exploring the forest will gain you XP. Levels are at XP of 25,
        75 and 250. Each time you level up you will receive bonuses to help you along.

    -Dying
        If you die in battle, your Save file is retained from the last time you saved (Quit/Inn Stay), but
        nothing you've earned since then is kept.

    -Quitting
        The game will also save your Player when you quit, but not with the same comfort as a night at the Inn.
    
    ''')

def LoadSavedGamesMenu():

    # Check for Saves
    saves = list(dataHelper.GetGameSaves())

    if saves == 0:
        return None

    print('-=-=-= SAVED GAMES =-=-=-')
    print()
    print('SLOT #\t\tSAVE NAME')

    for idx, save in enumerate(saves):
        print(f"[{idx}]\t\t{save.split('_')[0]}")
    
    print('\n[Q]uit')
    print()

    loadAnswer = input('Command: ').upper()

    if loadAnswer == 'Q' or loadAnswer.isdigit() == False:
        return None

    elif int(loadAnswer) > -1 and int(loadAnswer) <= len(saves):
        # returns a Player object
        return dataHelper.LoadGame(saves[int(loadAnswer)])
