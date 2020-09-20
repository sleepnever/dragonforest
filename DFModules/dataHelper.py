
import os
import configparser
import json
from collections import OrderedDict
from pathlib import Path, PureWindowsPath

GAMESAVE_FILE = 'playerSave.ini'

def LoadDataFromJson(filepath, openMode, isOrderedDict=True):

    # use a Windows path
    filename = PureWindowsPath(filepath)

    correctPath = Path(filename)

    with open(correctPath, mode=openMode) as json_file:
        if isOrderedDict:
            jsonData = json.load(json_file, object_pairs_hook=OrderedDict)
        else:
            jsonData = json.load(json_file)

    return jsonData


def LoadGame(p1):

    # TODO: Update to use PathLib
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),GAMESAVE_FILE))

    p1.Name = config['PLAYER']['Name']
    p1.Level = config['PLAYER']['Level']
    p1.MaxHealth = config['PLAYER']['MaxHealth']
    p1.Health = config['PLAYER']['Health']
    p1.MaxArmor = config['PLAYER']['MaxArmor']
    p1.Armor = config['PLAYER']['Armor']
    p1.Xp = config['PLAYER']['Xp']
    p1.Weapon.Name = config['PLAYER']['Weapon']
    p1.Money = config['PLAYER']['Money']
    p1.LastTimeCamped = config['PLAYER']['LastTimeCamped']
    p1.HasDiscoveredTown = config['PLAYER']['HasDiscoveredTown']
    p1.StayedAtInn = config['PLAYER']['StayedAtInn']
    p1.Level1BonusReceived = config['PLAYER']['Level1BonusReceived']
    p1.Level2BonusReceived = config['PLAYER']['Level2BonusReceived']
    p1.Level3BonusReceived = config['PLAYER']['Level3BonusReceived']
    p1.Level4BonusReceived = config['PLAYER']['Level4BonusReceived']

def SaveGame(p1):

    print('< Saving Game >')
    # allow_no_value bug: https://github.com/ralphbean/bugwarrior/pull/600
    config = configparser.ConfigParser(allow_no_value=True)

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
        'LastTimeCamped':p1.LastTimeCamped, # can have no value
        'HasDiscoveredTown':p1.HasDiscoveredTown,
        'StayedAtInn':p1.StayedAtInn, # did the player stay at the inn (save game)? reset to False on load
        'Level1BonusReceived':p1.Level1BonusReceived,
        'Level2BonusReceived':p1.Level2BonusReceived,
        'Level3BonusReceived':p1.Level3BonusReceived,
        'Level4BonusReceived':p1.Level4BonusReceived
        }
    
    # TODO: Update to use PathLib
    with open(os.path.join(os.getcwd(),GAMESAVE_FILE),'w') as saveFile:
        config.write(saveFile)
