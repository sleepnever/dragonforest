
import time
import random

# Game Modules
from DFModules import artwork
from DFModules import common

#
# Functions
#

def town(p1):

    artwork.show_town()

    print('''
    Climbing over the rocks and pushing the branches out of the way, you see the town.
    As you walk towards the town, there\'s an Inn and a Blacksmith shop.
    People are bustling around doing chores, bartering for goods, yelling at each other.
    Children are playing games. One big kid is beating on another... ah, kids, what can you do?

    The rest of town is a blackened, charred, mess. A few buildings still smoldering...
    ''')

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
            common.do_action('townInn', p1, None)

        elif action == 'B':
            common.do_action('townBlacksmith', p1, None)

        elif action == 'T':
            common.do_action('townTalkToNpc', p1, None)

        elif action == 'L':
            return  # should go back to the main game loop with main menu

def talk_town_npc():

    npcTopics = ['Dragon Forest','Town History','Forest Secrets','Blacksmith','Inn']
    topic = random.choice(npcTopics)

    if topic == 'Dragon Forest':
        print('''
        You want to know about the mysterious stories of Dragon Forest do you? Well, I can only tell you
        what I've heard. No doubt you have seen the charred remains of the end of town, yes? That happened
        not long ago. I was buying some bread from the bakery, before that was burned too, when I heard a 
        screech and flapping of wings. Everyone on the street heard it. It got louder and louder and all 
        of a sudden through the mist, a giant stream of fire hit the roofs. Huge armored wings followed 
        behind and a great dragon appeared.

        The beast tore the roof off of the cattle barn, grabbed clawfuls of cows and flew off into the mist.
        About a month later, it came back, but smashed and burned the Bakery, but not before taking a clawful
        of buns and other items. It is the oddest thing I tell you. There is a man in town named J Klowd who
        has some very interesting theories on it.
        ''')

    elif topic == 'Town History':
        print('''
        The Town has been here as long as I can remember. It has drawn outsiders for the beauty
        of the forest, as well as the mysteries it holds. Many have also come in an attempt to slay that
        infernal beast that plagues the valley. Some years ago, a cocky bearded man came to the town and
        brought a slew of armor and weapons. He became the town's Blacksmith. He provides regular iron
        for the men here, but more specialized iron for those that dare hunt the beast. 
        ''')

    elif topic == 'Forest Secrets':
        print('''
        Our Forest is no mere forest. Many say it is magical and home to special creatures, many of whom
        if you are lucky enough to meet, they say will grant you wonderful things. 
        ''')
    
    elif topic == 'Blacksmith':
        print('''
        The Blacksmith is a man of few words, a bit cocky and thinks his jokes are funny. His name is
        M. Tiberius Chermakathau. Nobody knows that, so keep it to yourself. His iron is strong and you 
        will not find any better in this valley or the next. Tell him 'Guinevere' sent you.
        ''')
    
    elif topic == 'Inn':
        print('''
        Ahhh the Inn. A place of debauchery and good times. Owned by an Irish man named Scotty, who is
        a bit rough around the edges. Makes communicating with him a bit poor, but once you get to know 
        him, he's a good chap. Has some good stories too!
        ''')