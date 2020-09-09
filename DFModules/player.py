import math

from DFModules.weapon import Weapon

class Player():
    """ Player """

    # any variables up here are class level and shared by every instance (static)
    _maxHealth = 100 # TODO: need to fix these to upper(name) constant and then below for scoping
    _maxArmor = 200

    def __init__(self, name, weaponData):
        self._name = name
        self._level = 0
        self._maxHealth = self._maxHealth # rename this, add scope
        self._health = self._maxHealth # rename this, add scope
        self._maxArmor = self._maxArmor # rename this, add scope
        self._armor = 0
        self._xp = 0
        self._money = 2
        self._lastTimeCamped = None
        self._hasDiscoveredTown = False

        self.WeaponData = weaponData
        # Instantiate Weapon into a instance var in Player
        self.Weapon = self.GetWeapon('Stick')
    
    # ########################
    # PROPERTIES
    # ########################

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        self._name = value

    @property
    def Level(self):
        return self._level
    
    @Level.setter
    def Level(self, value):
        self._level = value
    
    @property
    def MaxHealth(self):
        return self._maxHealth

    @property
    def Health(self):
        return self._health

    @Health.setter
    def Health(self, value):
        self._health += value

        if self._health > self._maxHealth:
            self._health = self._maxHealth


    @property
    def MaxArmor(self):
        return self._maxArmor
    
    @property
    def Armor(self):
        return self._armor

    @Armor.setter
    def Armor(self, value):
        self._armor += value

        # Validate min/max values and re/set appropriately
        if self._armor < 0:
            self._armor = 0
        elif self._armor > self._maxArmor:
            self._armor = self._maxArmor

    @property
    def Xp(self):
        return self._xp

    @Xp.setter
    def Xp(self, value):
        self._xp += value

    @property
    def Money(self):
        return self._money

    @Money.setter
    def Money(self, value):
        self._money += value

    @property
    def LastTimeCamped(self):
        return self._lastTimeCamped

    @LastTimeCamped.setter
    def LastTimeCamped(self, value):
        self._lastTimeCamped = value

    @property
    def HasDiscoveredTown(self):
        return self._hasDiscoveredTown

    @HasDiscoveredTown.setter
    def HasDiscoveredTown(self, value):
        self._hasDiscoveredTown = value

    # ########################
    # METHODS
    # ########################

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

    # TODO: refactor this to a static helper for player and enemy use
    def CalculateDamageTaken(self, damage):
        # armor should take the brunt of the hit first, but health should still be affected
        if self._armor == 0:
            self._health = self._health - damage
        else:
            self._health = math.ceil((self._health * 0.001)*100) - abs(self._armor - damage)

    def UpdateLevel(self):

        if self._xp < 25:
            pass
        elif self._xp >= 25 and self._xp < 50:
            self._level = 1
            self._money += 5
        elif self._xp >= 50 and self._xp < 150:
            self._level = 2
            self._money += 10
        elif self._xp >= 150 and self._xp <= 500:
            self._level = 3
            self._money += 25
        elif self._xp >= 500 and self._xp <= 750:
            self._level = 4
            self._money += 50

        return self._level

    def IsDead(self):
        return True if (self._health <= 0) else False
