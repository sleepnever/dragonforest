
class Enemy():
    """ Enemy """

    def __init__(self, enemyData):
        self._name = enemyData['name']
        self._level = enemyData['level']
        self._health = enemyData['health']
        self._armor = enemyData['armor']
        self._damage = enemyData['damage']
        self._maxXp = enemyData['maxxp'] # max allowed XP that can be earned by defeating this enemy

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
    def Health(self):
        return self._health
    
    @Health.setter
    def Health(self, value):
        self._health += value
    
    @property
    def Armor(self):
        return self._armor
    
    @Armor.setter
    def Armor(self, value):
        self._armor += value

    @property
    def Damage(self):
        return self._damage

    @Damage.setter
    def Damage(self, value):
        self._damage = value

    @property
    def MaxXp(self):
        return self._maxXp
    
    @MaxXp.setter
    def MaxXp(self, value):
        self._maxXp = value

    # ########################
    # METHODS
    # ########################

    def IsDead(self):
        return True if (self._health <= 0) else False