from DFModules import artwork

def cave(p1):
    
    artwork.showDragonCave()

    print('''
    There is no sound, except the crackle of a few burning trees. The landscape in front of the cave
    is scorched black. Bones lay at the entrance. The mighty Dragon lives within.
    ''')
    print(f'\nYou hold your {p1.Weapon} in one hand, bang on your armor with the other. You are ready.')
    print()

    dragonAnswer = input("Fight the Dragon (Y/N): ").upper()

    if dragonAnswer == 'Y':
        fightDragon(p1)
    else:
        print('No, today isn\'t the day for this. You sneak away.')

def fightDragon(p1):
    pass