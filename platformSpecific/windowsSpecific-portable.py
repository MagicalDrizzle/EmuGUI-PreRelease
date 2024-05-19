import os
import sqlite3
from pathlib import Path



def setupWindowsBackend():
    connection = None

    try:
        connection = sqlite3.connect(f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\virtual_machines.sqlite")
        print("Connection established.")
    
    except sqlite3.Error as e:
        print(f"The SQLite module encountered an error: {e}. Trying to create the file.")

        try:
            windowsCreEmuGUIFolder()
            file = open(f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\virtual_machines.sqlite", "w+")
            file.close()
        
        except:
            print("EmuGUI wasn't able to create the file.")

        try:
            connection = sqlite3.connect(f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\virtual_machines.sqlite")
            print("Connection established.")

        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")
    
    return connection

def windowsTempVmStarterFile():
    fileName = f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\vmstart.txt"
    return fileName

def windowsLanguageFile():
    fileName = f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\lang.txt"
    return fileName

def windowsUpdateFile():
    fileName = f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\update.txt"
    return fileName

def windowsExportFile():
    fileName = f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\vmdef.txt"
    return fileName

def windowsErrorFile():
    fileName = f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\error.txt"
        
    return fileName

def windowsLogFile(logID):
    fileName = f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata\\log-{logID}.txt"
        
    return fileName

def windowsCreEmuGUIFolder():
    Path(f"{Path(Path( __file__ ).parent.absolute()).parent.absolute()}\\userdata").mkdir(parents=True, exist_ok=True)