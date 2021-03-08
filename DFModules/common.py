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

def do_action(action, playerObj, enemyData):

    if action == 'talk':
        # TODO: do something.. need function/module for NPCs
        pass
        
    elif action == 'exploreForest':
        forest.explore_forest(playerObj, enemyData)

    elif action == 'stats':
        display_player_stats(playerObj)

    elif action == 'camp':
        forest.camp(playerObj)

    elif action == 'town':
        town.town(playerObj)

    elif action == 'townInn':
        inn.inn(playerObj)

    elif action == 'townTalkToNpc':
        town.talk_town_npc()

    elif action == 'townBlacksmith':
        blacksmith.blacksmith(playerObj)

    elif action == 'blacksmithWeapons':
        blacksmith.blacksmith_weapons(playerObj)

    elif action == 'blacksmithArmorUpgrade':
        blacksmith.blacksmith_armor_upgrade(playerObj)
    
    elif action == 'blacksmithSpecialAction':
        blacksmith.blacksmith_special(playerObj)

    elif action == 'innGamble':
        inn.inn_gamble(playerObj)

    elif action == 'innStay':
        print('You head to your room. Its not much and there is a funny smell, but it will suffice.')
        playerObj.StayedAtInn = True
        dataHelper.save_game(playerObj)

        sys.exit()

    elif action == 'innDrink':
        inn.inn_drink(playerObj)

    elif action == 'innTownNews':
        inn.inn_town_news(playerObj)
    
    elif action == 'innTalkInnkeeper':
        inn.talk_inn_keeper(playerObj)
    
    elif action == 'dragoncave':
        dragon.cave(playerObj, enemyData)

    elif action == 'help':
        display_help()


def display_player_stats(p1) -> None:
    
    print()
    print('-=-=-=-=-=-=-=-=-=-STATS=-=-=-=-=-=-=-=-=-=-=-')
    print('|')
    print(f'| Player Name     :  {p1.Name}')
    print(f'| Health (HP)     :  {p1.Health}/{p1.MaxHealth}')
    print(f'| Armor  (AP)     :  {p1.Armor}/{p1.MaxArmor}')
    print(f'| Weapon / Damage :  {p1.Weapon.Name} / {p1.Weapon.Damage}')
    print(f'| Level           :  {p1.Level}')
    print(f'| Experience (XP) :  {p1.Xp}')
    print(f'| Gold Coins      :  {p1.Money}')
    print('|')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print()

def display_help() -> None:

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

def load_saved_games_menu():

    # Check for Saves
    saves = list(dataHelper.get_game_saves())

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
        return dataHelper.load_game(saves[int(loadAnswer)])
