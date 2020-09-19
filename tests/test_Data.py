from pathlib import Path, PureWindowsPath

# Tests that validate the JSON data files in \Data exist

def test_WeaponsJsonFileExists():
    filename = PureWindowsPath("..\\Data\\weapons.json")
    correctPath = Path(filename)

    assert correctPath.exists()

def test_EnemiesJsonFileExists():
    filename = PureWindowsPath("..\\Data\\enemies.json")
    correctPath = Path(filename)

    assert correctPath.exists()
