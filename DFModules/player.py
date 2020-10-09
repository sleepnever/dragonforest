import math
import random
import datetime

# Game Modules
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
        self._health = 0
        self._maxArmor = self._maxArmor # rename this, add scope
        self._armor = 0
        self._xp = 0
        self._money = 0
        self._lastTimeCamped = None
        self._hasDiscoveredTown = False
        self._stayedAtInn = False
        self._blacksmithSpecialReceived = False

        self.WeaponData = weaponData
        # Instantiate Weapon into a instance var in Player
        self.Weapon = self.GetWeapon('Stick')

        # self.LevelUp gets called and resets the values for the money+armor bonus
        # each time. So I need some kind of flag so the bonus is given but not taken.
        self._level1BonusReceived = False
        self._level2BonusReceived = False
        self._level3BonusReceived = False
        self._level4BonusReceived = False
    
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

    @property
    def StayedAtInn(self):
        return self._stayedAtInn
    
    @StayedAtInn.setter
    def StayedAtInn(self, value):
        self._stayedAtInn = value

    @property
    def BlacksmithSpecialReceived(self):
        return self._blacksmithSpecialReceived
    
    @BlacksmithSpecialReceived.setter
    def BlacksmithSpecialReceived(self, value):
        self._blacksmithSpecialReceived = value

    @property
    def Level1BonusReceived(self):
        return self._level1BonusReceived

    @Level1BonusReceived.setter
    def Level1BonusReceived(self, value):
        self._level1BonusReceived = value

    @property
    def Level2BonusReceived(self):
        return self._level2BonusReceived

    @Level2BonusReceived.setter
    def Level2BonusReceived(self, value):
        self._level2BonusReceived = value

    @property
    def Level3BonusReceived(self):
        return self._level3BonusReceived

    @Level3BonusReceived.setter
    def Level3BonusReceived(self, value):
        self._level3BonusReceived = value

    @property
    def Level4BonusReceived(self):
        return self._level4BonusReceived

    @Level4BonusReceived.setter
    def Level4BonusReceived(self, value):
        self._level4BonusReceived = value

    # ########################
    # METHODS
    # ########################

    # After new player is created, set default values
    def SetDefaultValues(self):
        self.Health = self._maxHealth
        self.Money = 10


    def GetWeapon(self, weaponName):
        """ Search OrderedDict of Weapons and return a Weapon object if found """

        for weapon in self.WeaponData['weapons']:
            if weapon['name'] == weaponName:
                return Weapon(weapon['name'],weapon['damage'],weapon['maxDamage'],weapon['cost'])

    
    def BuyWeapon(self, weaponName):
        """ Assigns the weapon to the Player if Player has enough Money """

        weapon = self.GetWeapon(weaponName)

        if self._money >= weapon.Cost:
            self.Weapon = self.GetWeapon(weaponName)
            self._money -= weapon.Cost
            return True
        
        return False
    
    def UpgradeWeapon(self, damage):
        """ Upgrade damage on weapon, but no more than maxDamage allowed """

        #if damage < self.Weapon['maxDamage']:
        #    self.Weapon['damage'] += damage
        #    return True

        return False

    def UpgradeArmor(self, cost, upgradeAmount):
        """ Upgrade Armor """
        
        if self._money >= cost:
            self._money -= cost
            self._armor += upgradeAmount
            return True
        
        return False

    # TODO: refactor this to a static helper for player and enemy use
    # Armor should take the brunt of the hit first, but health should still be affected
    def CalculateDamageTaken(self, damage):
        """ Calculates the damage taken, with and without armor """
        #print('DEBUG: CalculateDamageTaken(self, {})'.format(damage))

        if self._armor == 0:
            self._health -= damage
            healthDamage = damage
        else:
            # Ding the armor first by a little bit
            #print('DEBUG: Armor Before Hit = {}'.format(self._armor))
            damageMultiplier = random.uniform(0.001, 0.003)
            armorDamage = int(math.ceil((self._armor * damageMultiplier)*100))
            self._armor -= armorDamage
            #print('DEBUG: Armor After Hit = {}'.format(self._armor))

            # Take the amount of armor damage and and subtract it
            # from the incoming damage amount, to then get how much
            # damage will be taken  from the player's health
            #print('DEBUG: Health Before Hit = {}'.format(self._health))
            healthDamage = abs(damage - armorDamage)
            self._health -= healthDamage
            #print('DEBUG: Health After Hit/Armor absorb = {}'.format(self._health))

        return healthDamage

    def LevelUp(self):
        """ Level up the Player """

        if self._xp < 25:
            pass
        elif self._xp >= 25 and self._xp < 50:
            self._level = 1
            
        elif self._xp >= 50 and self._xp < 150:
            self._level = 2
            
        elif self._xp >= 150 and self._xp <= 500:
            self._level = 3
            
        elif self._xp >= 500 and self._xp <= 750:
            self._level = 4
        
        self.GiveLevelBonus()

    def GiveLevelBonus(self):
        """ Level Up Bonuses """

        if self._level == 1 and self._level1BonusReceived == False:
            self._level1BonusReceived = True
            self._money = 10
            self._armor = 10
            self._xp = 10
        
        elif self._level == 2 and self._level2BonusReceived == False:
            self._level2BonusReceived = True
            self._money = 15
            self._armor = 25
            self._xp = 20
        
        elif self._level == 3 and self._level3BonusReceived == False:
            self._level3BonusReceived = True
            self._money = 25
            self._armor = 45
            self._xp = 30

        elif self._level == 4 and self._level4BonusReceived == True:
            self._level4BonusReceived = True
            self._money = 35
            self._armor = 65
            self._xp = 40

    def IsDead(self):
        """ Check to see if the Player is Dead """

        return True if (self._health <= 0) else False
