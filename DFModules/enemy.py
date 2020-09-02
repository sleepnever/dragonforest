
class Enemy():
    """ Enemy """

    def __init__(self, enemyData):
        self.Name = enemyData['name']
        self.Level = enemyData['level']
        self.Health = enemyData['health']
        self.Armor = enemyData['armor']
        self.Damage = enemyData['damage']
        self.MaxXp = enemyData['maxxp'] # max allowed XP that can be earned by defeating this enemy

    def IsDead(self):
        return True if (self.Health <= 0) else False