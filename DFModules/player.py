import math

from DFModules.weapon import Weapon

class Player():
    """ Player """

    # any variables up here are class level and shared by every instance (static)
    _maxHealth = 100
    _maxArmor = 200

    def __init__(self, name, weaponData):
        self.Name = name    # specific to the created instance and public (instance)
        self.Level = 0
        self.MaxHealth = self._maxHealth
        self.Health = self._maxHealth # start with max
        self.MaxArmor = self._maxArmor
        self.Armor = 0
        self.Xp = 0
        self.Money = 2
        self.LastTimeCamped = None
        self.HasDiscoveredTown = False

        self.WeaponData = weaponData
        # Instantiate Weapon into a instance var in Player
        self.Weapon = self.GetWeapon('Stick')
        
    def GetWeapon(self, weaponName):
        """ Search OrderedDict of Weapons and return a Weapon object if found """
        for weapon in self.WeaponData['weapons']:
            if weapon['name'] == weaponName:
                return Weapon(weapon['name'],weapon['damage'],weapon['maxDamage'],weapon['cost'])

    
    def BuyWeapon(self, weaponName):
        """ Assigns the weapon to the Player if Player has enough Money """

        #if self.Money >= self.WeaponClass.GetWeapon(weaponName)['cost']:
        #    self.Weapon = self.WeaponClass.GetWeapon(weaponName)
        #    self.Money -= self.Weapon['cost']
        #    return True
        
        return False
    
    # Return bool if weapon was upgraded
    def UpgradeWeapon(self, damage):
        """ Upgrade damage on weapon, but no more than maxDamage allowed """
        #if damage < self.Weapon['maxDamage']:
        #    self.Weapon['damage'] += damage
        #    return True

        return False


    def CalculateDamage(self, damage): # health and armor
        # armor should take the brunt of the hit first, but health should still be affected
        if self.Armor == 0:
            self.Health = self.Health - damage
        else:
            self.Health = math.ceil((self.Health * 0.001)*100) - abs(self.Armor - damage)
    
    def UpdateArmor(self, amount):
        self.Armor += amount
        
        # make sure we don't go beyond min/max values
        if self.Armor < 0:
            self.Armor = 0
        elif self.Armor > self.MaxArmor:
            self.Armor = self.MaxArmor
    
    def UpdateHealth(self, amount):
        self.Health += amount

        # make sure we don't go over max value. Less than min == dead
        if self.Health > self.MaxHealth:
            self.Health = self.MaxHealth
        
    def AddXp(self, amount):
        self.Xp += amount
    
    def UpdateLevel(self):

        if self.Xp < 25:
            pass
        elif self.Xp >= 25 and self.Xp < 50:
            self.Level = 1
        elif self.Xp >= 50 and self.Xp < 150:
            self.Level = 2
        elif self.Xp >= 150 and self.Xp <= 500:
            self.Level = 3
        elif self.Xp >= 500 and self.Xp <= 750:
            self.Level = 4

        return self.Level

    def IsDead(self):
        return True if (self.Health <= 0) else False

# DEBUG/TEST: python player.py
"""
debugPlayer = Player("Bjork")
print('Player has weapon and money: ')
print(debugPlayer.Weapon) # stick
print(debugPlayer.Money) # 2
print(debugPlayer.Weapon['cost']) # 0
# playerClass.WeaponClassInstance.Method(string) returns a Weapon object, call [cost]
if debugPlayer.Money >= debugPlayer.WeaponClass.GetWeapon('Wood Bat')['cost']:
    debugPlayer.BuyWeapon('Wood Bat')
else:
    print('You don\'t have enough money for that')

print(debugPlayer.Money) # -8
print(debugPlayer.Weapon)
debugPlayer.UpgradeWeapon(10)
print(debugPlayer.Weapon['damage'])
"""