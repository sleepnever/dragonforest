
import os
from os import listdir
import configparser
import json
import datetime
from collections import OrderedDict
from pathlib import Path, PureWindowsPath

from DFModules.player import Player

GAMESAVE_BASEFILE = '_playerSave.ini'

# distutils.util depreciated in 3.12
# Replacement function
def strtobool(value: str) -> bool:
    value = value.lower()
    if value in ("y", "yes", "on", "1", "true", "t"):
        return True
    return False

def get_files_from_dir(directory, extension):
    return (f for f in listdir(directory) if f.endswith('.' + extension))

def load_data_from_json(filepath, openMode, isOrderedDict=True):

    # use a Windows path
    filename = PureWindowsPath(filepath)

    correctPath = Path(filename)

    with open(correctPath, mode=openMode) as json_file:
        if isOrderedDict:
            jsonData = json.load(json_file, object_pairs_hook=OrderedDict)
        else:
            jsonData = json.load(json_file)

    return jsonData

def get_game_saves():
    
    return get_files_from_dir(os.getcwd(), 'ini')


def load_game(playerSaveFile):

    weaponData = load_data_from_json("Data\\weapons.json", "r")
    
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),playerSaveFile))

    p1 = Player('temp', weaponData)

    p1.Name = config['PLAYER']['Name']
    p1.Level = int(config['PLAYER']['Level'])
    p1.Health = int(config['PLAYER']['Health'])
    p1.Armor = int(config['PLAYER']['Armor'])
    p1.Xp = int(config['PLAYER']['Xp'])
    p1.Weapon = p1.get_weapon(config['PLAYER']['Weapon'])
    p1.Money = int(config['PLAYER']['Money'])
    p1.LastTimeCamped = datetime.datetime.strptime(config['PLAYER']['LastTimeCamped'], "%Y-%m-%d %H:%M:%S.%f") # 2020-10-06 22:37:50.819024
    p1.HasDiscoveredTown = strtobool(config['PLAYER']['HasDiscoveredTown'])
    p1.StayedAtInn = strtobool(config['PLAYER']['StayedAtInn'])
    p1.BlacksmithSpecialReceived = strtobool(config['PLAYER']['BlacksmithSpecialReceived'])
    p1.HadDragonDiscussion = strtobool(config['PLAYER']['HadDragonDiscussion'])
    p1.Level1BonusReceived = strtobool(config['PLAYER']['Level1BonusReceived'])
    p1.Level2BonusReceived = strtobool(config['PLAYER']['Level2BonusReceived'])
    p1.Level3BonusReceived = strtobool(config['PLAYER']['Level3BonusReceived'])

    return p1

def save_game(p1):

    print('< Saving Game >')
    
    config = configparser.ConfigParser()
    
    # Must set a lastTimeCamped, cannot be None. Time won't matter by next LoadGame
    p1.LastTimeCamped = datetime.datetime.now() - datetime.timedelta(minutes=10)

    config['PLAYER'] = {
        'Name':p1.Name,
        'Level':p1.Level,
        'MaxHealth':p1.MaxHealth,
        'Health':p1.Health,
        'MaxArmor':p1.MaxArmor,
        'Armor':p1.Armor,
        'Xp':p1.Xp,
        'Weapon':p1.Weapon.Name,
        'Money':p1.Money,
        'LastTimeCamped':p1.LastTimeCamped,
        'HasDiscoveredTown':p1.HasDiscoveredTown,
        'StayedAtInn':p1.StayedAtInn,
        'BlacksmithSpecialReceived':p1.BlacksmithSpecialReceived,
        'HadDragonDiscussion':p1.HadDragonDiscussion,
        'Level1BonusReceived':p1.Level1BonusReceived,
        'Level2BonusReceived':p1.Level2BonusReceived,
        'Level3BonusReceived':p1.Level3BonusReceived,
        }
    
    # TODO: Update to use PathLib
    playerSaveFile = p1.Name + GAMESAVE_BASEFILE
    with open(os.path.join(os.getcwd(),playerSaveFile),'w') as saveFile:
        config.write(saveFile)

def delete_save_game(playerName):

    playerSaveFile = playerName + GAMESAVE_BASEFILE
    if os.path.exists(playerSaveFile):
        os.remove(playerSaveFile)