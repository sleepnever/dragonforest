
import time
import random

# Game Modules
from DFModules import artwork
from DFModules import common

#
# Functions for Blacksmith
#

def blacksmith(p1):

    artwork.show_blacksmith()

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
            common.do_action('blacksmithWeapons', p1, None)

        elif action == 'A':
            common.do_action('blacksmithArmorUpgrade', p1, None)

        elif action == "GUINEVERE":
            common.do_action('blacksmithSpecialAction', p1, None)

        elif action == 'L':
            return

def blacksmith_weapons(p1):

    print(f'"Welcome to my Armory wall. This is what I have for purchase. Coin only."')
    print(f'You have {p1.Money} coin.')
    print()
    print('<===|- WEAPONS -|===>')
    print()
    
    print('NAME                    DAMAGE   COST')
    
    weaponDict = {}
    for idx, weapon in enumerate(p1.WeaponData['weapons']):
        
        # don't show the default 'stick'
        if idx == 0:
            continue

        weaponDict[idx] = weapon['name']
        print(f'[{idx}] {weapon["name"]:<20} {weapon["damage"]}       {weapon["cost"]}')

    print('\n[E]xit Buy Menu')

    command = input('\nCommand: ').upper()

    if command == 'E':
        pass

    elif int(command) in range(1,len(p1.WeaponData['weapons'])):
        
        weaponName = weaponDict.get(int(command))

        # player can purchase
        if p1.buy_weapon(weaponName):
            print(f'You purchased a {weaponName}')
        else:
            print('You do not have enough money.')

def blacksmith_armor_upgrade(p1):

    print('''   
             __________
             |  ARMOR  |
             |         |
              \\______/
    ''')
    print(f'Current Coin : {p1.Money}')
    print(f'Current Armor: {p1.Armor}')

    if p1.Armor != p1.MaxArmor:
        
        # BUG: 432 coin for 218 AP, current AP=2 --way too much, and max Armor = 200
        # FIX: Change formula
        #   Ex: Cost -> ((10 XP * 0.2)*2) = 4 * random(1-3) = 4, 8, 12
        #       Armor Amount -> 10 + 3 = 13
        upgradeCost = int((((p1.Xp * 0.2)*2) * random.randint(1,3)))
        upgradeAmount = ((p1.Xp + p1.Armor) // 2)
        
        print(f'Upgrade Cost : {upgradeCost} coin for {upgradeAmount} AP')

        action = input('\nDo you want to upgrade? Y/N: ').upper()    

        if action == 'Y':
            if p1.upgrade_armor(upgradeCost, upgradeAmount):
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

def blacksmith_special(p1):
    
    if p1.BlacksmithSpecialReceived == False:
        print('''
        The Blacksmith gives you a wide grin, which quickly turns to a scowl. He steps forward and grabs
        your tunic with his dirty hand and asks "What did she tell you?!"

        "Sh..she told me you were the best Blacksmith the land has seen!", you exclaim, hoping that is the
        answer he is looking for and doesn't pummel you.

        He releases your tunic and starts to laugh, muttering something under his breath. "That's right. I
        am."
        ''')
        if p1.Armor == 0:
            print('\t"Here, take this." he says, handing you a shiny set of armor worth 75 AP.')
            p1.Armor = 75

        elif p1.Armor >= 1:
            print('\t"Here, let me fix up that armor for you." he says. +20 AP gained.')
            p1.Armor = 20

        p1.BlacksmithSpecialReceived = True
        
    else:
        print('You quit talking to that woman you hear me? She\'s nothing but trouble, for both of us.')
