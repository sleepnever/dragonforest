import random
import sys
import time

#
# Functions related to combat
#

def Attack(p1, enemyObj):

    while p1.IsDead() == False and enemyObj.IsDead() == False:
        print()
        print(f'You swing your {p1.Weapon.Name} at the {enemyObj.Name}')

        # Get random damage range values from 0 to upper values
        p1_damageGiven = random.randint(0, p1.Weapon.Damage) # how much player deals
        enemy_damageGiven = random.randint(0, enemyObj.Damage) # how much enemy deals

        # Enemy's damage taken from player
        # #TODO: enemy could have armor, so use the player function and generalize it
        enemyObj.Health = (-1 * p1_damageGiven)

        # Check if player or enemy is dead
        if (enemyObj.IsDead()):
            print(f'You hit the {enemyObj.Name} for {p1_damageGiven} damage, and killed it!')

            addedXp = random.randint(1, enemyObj.MaxXp)
            p1.Xp = addedXp
            print(f'\n\nYou have gained {addedXp} XP!')

            return
            
        else:
            print(f'You hit the {enemyObj.Name} for {p1_damageGiven} damage! It has {enemyObj.Health} HP.')

        # Calculate Player's Damage taken from enemy, factoring in armor
        enemy_damageGiven = p1.CalculateDamageTaken(enemy_damageGiven)

        if (p1.IsDead()):
            print(f'{p1.Name} is hit with {enemy_damageGiven} damage and has died! <<GAME OVER>>')
            sys.exit()
        else:
            print(f'You are hit with {enemy_damageGiven} damage and have {p1.Health} HP left.')

        time.sleep(1)