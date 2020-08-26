#import json
#from collections import OrderedDict
#from pathlib import Path, PureWindowsPath

class Weapon:
    """ Weapon for Player """

    def __init__(self, name, damage, maxDamage, cost):
        self.Name = name
        self.Damage = damage
        self.MaxDamage = maxDamage
        self.Cost = cost
"""
    def GetWeaponNames(self):

        names = []
        for weapon in self.Data['weapons']:
            names.append(weapon['name'])

        return names

    def GetWeapon(self, name):
        return self.Data['weapons'][name]
"""

# DEBUG: python3 weapon.py
"""
w = Weapon()
print(type(w.Data))
#print(w.Data['weapons'][0]['name'])
print('Weapon Names: {}'.format(w.GetWeaponNames()))
#print('Get Weapon by Name (key): {}'.format(w.GetWeapon('Stick')))
"""