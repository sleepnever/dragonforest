
class Enemy:

    def __init__(self, name, health, maxDamage):
        self.name = name
        self.level = 0
        self.totalHealth = health
        self.currentHealth = self.totalHealth
        self.maxDamage = maxDamage

    def isDead(self):
        return True if (self.currentHealth <= 0) else False