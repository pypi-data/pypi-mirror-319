import os

def Fileclen():
    try:
        os.system("cls")
        print("Enter file path")
        filep=input(">")
        notefile=open(filep,'w')
        notefile.truncate()
        os.system("cls")
        print("file cleared!")
    except (Exception,KeyboardInterrupt,ModuleNotFoundError):
        os.system("cls")
        print("System failed to format the file.")
Fileclen()