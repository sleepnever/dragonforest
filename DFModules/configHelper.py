#
# Game Config File IO Module
#

import configparser from os

def filepathExists(filepath):
    return path.exists(filepath)

def createSaveGame(filepath):
    file = open(filepath, 'x')
    file.close()

def deleteSaveGame(filepath)
    os.remove(filepath)

def loadGame():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),GAMESAVE_FILE))

    p1.name = config['PLAYER']['name']
    p1.level = config['PLAYER']['level']
    p1.totalHealth = config['PLAYER']['totalHealth']
    p1.currentHealth = config['PLAYER']['currentHealth']
    p1.totalArmor = config['PLAYER']['totalArmor']
    p1.currentArmor = config['PLAYER']['currentArmor']
    p1.xp = config['PLAYER']['xp']
    p1.weapon = config['PLAYER']['weapon']
    p1.money = config['PLAYER']['money']
    p1.lastTimeCamped = config['PLAYER']['lastTimeCamped']


def saveGame():
    config = configparser.ConfigParser()

    config['PLAYER'] = {
        'name':p1.name,
        'level':p1.level,
        'totalHealth':p1.totalHealth,
        'currentHealth':p1.currentHealth,
        'totalArmor':p1.totalArmor,
        'currentArmor':p1.currentArmor,
        'xp':p1.xp,
        'weapon':p1.weapon,
        'money':p1.money,
        'lastTimeCamped':p1.lastTimeCamped
        }
    
    with open(os.path.join(os.getcwd(),GAMESAVE_FILE),'w') as configFile:
        config.write(configFile)
