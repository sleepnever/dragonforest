
import time
import random

# Game Modules
from DFModules import artwork
from DFModules import common

#
# Functions for Blacksmith
#

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
            common.DoAction('blacksmithWeapons', p1, None)
        elif action == 'A':
            common.DoAction('blacksmithArmorUpgrade', p1, None)
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
