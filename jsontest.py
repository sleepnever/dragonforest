import json
from collections import OrderedDict

# JSON + PYTHON TEST CODE

with open('weapons.json') as json_file:
    #data = json.load(json_file, object_pairs_hook=OrderedDict) # unordered
    data = json.load(json_file, object_pairs_hook=OrderedDict) # ordered
    print('Blacksmith Weapons Available:\n')
    #print(data['longsword']['maxDamage'])

    # loop through data and extract information
    for weapon in data:
        #print("{} | Damage: {} / Max {} | Cost: {}".format(wep,data[wep]['damage'],data[wep]['maxDamage'],data[wep]['cost']))
        #print(names) # prints the "text": { .. }, not the actual property name
        print("{} | Damage: {} / Max {} | Cost: {}".format(weapon,data[weapon]['damage'],data[weapon]['maxDamage'],data[weapon]['cost']))

# data is accessible outside of with open() as
print(data['Battle Stick']['damage'])

# put weapon names in a list, for key lookup
weaponNames = []
for weaponName in data:
    weaponNames.append(weaponName)

print(weaponNames)
