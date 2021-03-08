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
        self._hadDragonDiscussion = False

        self.WeaponData = weaponData
        # Instantiate Weapon into a instance var in Player
        self.Weapon = self.get_weapon('Stick')

        # self.LevelUp gets called and resets the values for the money+armor bonus
        # each time. So I need some kind of flag so the bonus is given but not taken.
        self._level1BonusReceived = False
        self._level2BonusReceived = False
        self._level3BonusReceived = False
    
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
    def HadDragonDiscussion(self):
        return self._hadDragonDiscussion
    
    @HadDragonDiscussion.setter
    def HadDragonDiscussion(self, value):
        self._hadDragonDiscussion = value

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


    # ########################
    # METHODS
    # ########################

    # After new player is created, set default values
    def set_default_values(self):
        self.Health = self._maxHealth
        self.Money = 10


    def get_weapon(self, weaponName):
        """ Search OrderedDict of Weapons and return a Weapon object if found """

        for weapon in self.WeaponData['weapons']:
            if weapon['name'] == weaponName:
                return Weapon(weapon['name'],weapon['damage'],weapon['maxDamage'],weapon['cost'])

    
    def buy_weapon(self, weaponName):
        """ Assigns the weapon to the Player if Player has enough Money """

        weapon = self.get_weapon(weaponName)
        
        if self.Money >= weapon.Cost:
            self.Weapon = weapon
            self.Money = (-1 * weapon.Cost)
            return True
        
        return False
    
    def upgrade_weapon(self, damage):
        """ Upgrade damage on weapon, but no more than maxDamage allowed """

        #if damage < self.Weapon['maxDamage']:
        #    self.Weapon['damage'] += damage
        #    return True

        return False

    def upgrade_armor(self, cost, upgradeAmount):
        """ Upgrade Armor """
        
        if self.Money >= cost:
            self.Money = (-1 * cost)
            self.Armor = upgradeAmount
            return True
        
        return False

    # TODO: refactor this to a static helper for player and enemy use
    # Armor should take the brunt of the hit first, but health should still be affected
    def calculate_damage_taken(self, damage):
        """ Calculates the damage taken, with and without armor """

        if self.Armor == 0:
            self.Health = (-1 * damage)
            healthDamage = damage
        else:
            # Ding the armor first by a little bit
            #print('DEBUG: Armor Before Hit = {}'.format(self._armor))
            damageMultiplier = random.uniform(0.001, 0.003)
            armorDamage = int(math.ceil((self.Armor * damageMultiplier)*100))
            self.Armor = (-1 * armorDamage)
            #print('DEBUG: Armor After Hit = {}'.format(self._armor))

            # Take the amount of armor damage and and subtract it
            # from the incoming damage amount, to then get how much
            # damage will be taken  from the player's health
            #print('DEBUG: Health Before Hit = {}'.format(self._health))
            healthDamage = abs(damage - armorDamage)
            self.Health = (-1 * healthDamage)
            #print('DEBUG: Health After Hit/Armor absorb = {}'.format(self._health))

        return healthDamage

    def level_up(self):
        """ Level up the Player """

        if self.Xp < 25:
            pass
        elif self.Xp >= 25 and self.Xp < 75:
            self.Level = 1
            self.HasDiscoveredTown = True
            
        elif self.Xp >= 75 and self.Xp < 250:
            self.Level = 2
            
        elif self.Xp >= 250 and self.Xp <= 400:
            self.Level = 3
        
        self.give_level_bonus()

    def give_level_bonus(self):
        """ Level Up Bonuses """

        if self.Level == 1 and self.Level1BonusReceived == False:
            self.Level1BonusReceived = True
            self.Money = 20
            self.Armor = 25
            self.Xp = 10
        
        elif self.Level == 2 and self.Level2BonusReceived == False:
            self.Level2BonusReceived = True
            self.Money = 40
            self.Armor = 25
            self.Xp = 50
        
        elif self.Level == 3 and self.Level3BonusReceived == False:
            self.Level3BonusReceived = True
            self.Money = 60
            self.Armor = 50
            self.Xp = 100


    def is_dead(self):
        """ Check to see if the Player is Dead """
        return True if (self.Health <= 0) else False
