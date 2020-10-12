import sys

from DFModules import artwork
from DFModules.enemy import Enemy
from DFModules import combat
from DFModules import dataHelper

def cave(p1,enemyData):
    
    artwork.showDragonCave()

    print('''
    There is no sound, except the crackle of a few burning trees. The landscape in front of the cave
    is scorched black. Bones lay at the entrance. The mighty Dragon must live within.
    ''')
    print(f'\nYou hold your {p1.Weapon.Name} in one hand, bang on your armor with the other. You are ready.')
    print()

    caveAnswer = input("Enter the Cave (Y/N): ").upper()

    if caveAnswer == 'Y':
        dragonCave(p1, enemyData)
    else:
        print('No, today isn\'t the day for this. You sneak away.')

def dragonCave(p1, enemyData):
    
    print('''
    You stand on the corner, and peak your head around into the dark cave. Deep inside, you can hear
    a faint crackle and see a dim light. You slowly step into the cave.

    << CRUNCH >> You freeze. What did you just step on? Did the beast hear that? And why did you not
    think to bring a torch? *sigh*

    You proceed further. The light at the opening is beginning to fade and your eyes are trying to
    adjust.

    And then you hear it. Except you're not wanting to believe what you're hearing. Is.. is that a
    cow? Mooing? 

    "No, no.. nooooo!!" << SCREAM >> << FOOOOM >> The cave lights up bright and you can feel the
    heat. You see several cows, probably the ones from the town. And a stack of bread, likely
    from the bakery.  What the...? you think to yourself as it goes dark.

    You creep forward.

    << FOOOM >> Another burst of fire lights up the cave, and that's when you see it.

    A giant blue and and green dragon, with black spikes, and yellow eyes. His mouth is hanging
    open, while holding the most obscure thing in his claws, and his left eye is staring you
    down.

    ''')

    if p1.HadDragonDiscussion == False:
        print('''
        -= DRAGON CAVE MENU =-
        
        [A]ttack
        [T]alk it Out
        
        [L]eave the Cave

        ''')
    else:
        print('''
        -= DRAGON CAVE MENU =-
        
        [A]ttack
        
        [L]eave the Cave

        ''')


    answer = input('Command: ').upper()

    if answer == 'A':
        AttackDragon(p1, enemyData)
    elif answer == 'T':
        TalkToDragon(p1)
    elif answer == 'L':
        # TODO: 50/50 chance of getting away, otherwise die
        return

def AttackDragon(p1, enemyData):

    print(f'You raise your {p1.Weapon.Name}, scream like a mad man and run straight for it!!')
    
    dragonObj = Enemy.CreateEnemyByName('Dragon', enemyData)
    combat.Attack(p1, dragonObj)

def TalkToDragon(p1):
    
    print(f'The dragon\'s eyes shift and watch you closely. You lay your {p1.Weapon.Name} down to the side and back away.')
    print('''
    
    Well, here goes nothing, you think to yourself.

    "H..hey dragon. So I noticed that you have cows in here. An..And bread, from the bakery. Both of which you burned
    down. What does a dragon want with those things?" you ask, trying to sound confident, feeling anything but.
    
    The dragon lowers his snack. His long tongue slithers out of his mouth, licking his left nostril. There's a heavy
    sigh from the creature, which causes a bit of fire to drift out of his nostrils.

    "S'mores", says the dragon in a booming voice. "Cow. Bread. And huuuuuman for squishy part."

    You stand there wide-eyed. Did he just say s'mores? He did. A dragon that makes human s'mores. That's why he stole
    the cows, and the bread, and that's wh...wait. The last ingredient. A human. That's... me!!!
    ''')

    artwork.showDragonAmazement()

    p1.HadDragonDiscussion = True
    dataHelper.SaveGame(p1)

    sys.exit()


