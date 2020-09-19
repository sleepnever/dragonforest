
from DragonForest import *

# Test the LoadDataFromJson method and argument options
# TODO: refactor when I move methods into different modules

def test_DataNotNone():
    data = LoadDataFromJson("..\\Data\\weapons.json","r")
    assert data != None

def test_DataTypeOrderedDictByDefault():
    data = LoadDataFromJson("..\\Data\\weapons.json","r")
    assert type(data) is OrderedDict