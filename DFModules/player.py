import math

class Player:
    """ Player """

    # any variables up here are class level and shared by every instance
    _maxHealth = 100
    _maxArmor = 200

    def __init__(self, name):
        self.Name = name    # instance level, specific to the created instance and public
        self.Level = 0
        self.MaxHealth = self._maxHealth
        self.Health = self._maxHealth # start with max
        self.MaxArmor = self._maxArmor
        self.Armor = 0
        self.Xp = 0
        # Weapon should come from a/the Weapon class so this can be updated properly
        self.Weapon = 'Stick'
        self.WeaponDamage = 5
        self.Money = 2
        self.LastTimeCamped = None
        self.HasDiscoveredTown = False

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