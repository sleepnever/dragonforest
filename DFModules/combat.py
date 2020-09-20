import random
import sys
import time

#
# Functions related to combat
#

def Attack(p1, enemyObj):

    while p1.IsDead() == False and enemyObj.IsDead() == False:
        print()
        print('You swing your {} at the {}'.format(p1.Weapon.Name, enemyObj.Name))

        # Get random damage range values from 0 to upper values
        p1_damageGiven = random.randint(0, p1.Weapon.Damage) # how much player deals
        enemy_damageGiven = random.randint(0, enemyObj.Damage) # how much enemy deals

        # Enemy's damage taken from player
        # #TODO: enemy could have armor, so use the player function and generalize it
        enemyObj.Health = (-1 * p1_damageGiven)

        # Check if player or enemy is dead
        if (enemyObj.IsDead()):
            print('You hit the {} for {} damage, and killed it!'.format(enemyObj.Name, p1_damageGiven))

            addedXp = random.randint(1, enemyObj.MaxXp)
            p1.Xp = addedXp
            print('\n\nYou have gained {} XP!'.format(addedXp))

            return
            
        else:
            print('You hit the {} for {} damage! It has {} HP.'.format(enemyObj.Name, p1_damageGiven, enemyObj.Health))

        # Calculate Player's Damage taken from enemy, factoring in armor
        enemy_damageGiven = p1.CalculateDamageTaken(enemy_damageGiven)

        if (p1.IsDead()):
            print('{} is hit with {} damage and has died! <<GAME OVER>>'.format(p1.Name, enemy_damageGiven))
            sys.exit()
        else:
            print('You are hit with {} damage and have {} HP left.'.format(enemy_damageGiven, p1.Health))

        time.sleep(1)