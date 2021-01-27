import glob, os, sys

def printFiles(path, extension):
    os.chdir(path)
    for file in glob.glob("*." + extension):
        print(file)

if __name__ == "__main__":
    path = str(sys.argv[1])
    ext = str(sys.argv[2])
    printFiles(path, ext)