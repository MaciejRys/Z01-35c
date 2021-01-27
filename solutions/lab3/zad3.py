import glob, os, sys

if __name__ == "__main__":
    list = []
    sys.argv.pop(0)
    for arg in sys.argv:
        list.append(int(arg))
    list.sort()
    print(list)
