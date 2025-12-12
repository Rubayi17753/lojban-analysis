from src.classes.lockedval import LockedVal

# Tests LockedVal

def main():
    val = LockedVal()
    val.x = 5
    print(val.x)

    val.lock = 1
    val.x = 6
    print(val.x)

    val.lock = 0
    val.x = 7
    print(val.x)

    val._x = 8
    print(val.x)
    print(val._x)