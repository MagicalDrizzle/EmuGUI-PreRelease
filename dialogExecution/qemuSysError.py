from uiScripts.ui_QemuI386NotInstalled import Ui_Dialog
from PySide6.QtWidgets import *
from PySide6 import QtGui
import platform
import platformSpecific.windowsSpecific
import platformSpecific.unixSpecific
import translations.de
import translations.uk
import translations.en
import locale
import sqlite3

class QemuSysMissing(QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("EmuGUI - Component is missing")
        
        try:
            self.setWindowIcon(QtGui.QIcon("EmuGUI.png"))

        except:
            pass
        
        self.connectSignalsSlots()
        self.vmSpecs = self.readTempVmFile()
        self.langDetect()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.close)

    def readTempVmFile(self):
        # Searching temporary files
        if platform.system() == "Windows":
            tempVmDef = platformSpecific.windowsSpecific.windowsTempVmStarterFile()
        
        else:
            tempVmDef = platformSpecific.unixSpecific.unixTempVmStarterFile()

        vmSpecs = []

        with open(tempVmDef, "r+") as tempVmDefFile:
            vmSpecsRaw = tempVmDefFile.readlines()

        for vmSpec in vmSpecsRaw:
            vmSpecNew = vmSpec.replace("\n", "")
            vmSpecs.append(vmSpecNew)

        return vmSpecs

    def langDetect(self):
        select_language = """
        SELECT name, value FROM settings
        WHERE name = "lang";
        """

        if platform.system() == "Windows":
            connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            connection = platformSpecific.unixSpecific.setupUnixBackend()

        cursor = connection.cursor()

        try:
            cursor.execute(select_language)
            connection.commit()
            result = cursor.fetchall()

            # Language modes
            # system: language of OS
            # en: English
            # de: German
            langmode = "system"

            try:
                qemu_img_slot = str(result[0])               

                if result[0][1] == "en":
                    langmode = "en"

                elif result[0][1] == "de":
                    langmode = "de"

                elif result[0][1] == "uk":
                    langmode = "uk"

                elif result[0][1] == "system":
                    langmode = "system"

                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot already is in the database.")

            except:
                langmode = "system"
                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot has been created.")
        
        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

    def setLanguage(self, langmode):
        if langmode == "system" or langmode == None:
            languageToUse = locale.getlocale()[0]

        else:
            languageToUse = langmode

        if languageToUse != None:
            if languageToUse.startswith("de"):
                translations.de.translateQemuSysMissingDE(self, self.vmSpecs[1])

            elif languageToUse.startswith("uk"):
                translations.uk.translateQemuSysMissingUK(self, self.vmSpecs[1])

            else:
                translations.en.translateQemuSysMissingEN(self, self.vmSpecs[1])
        
        else:
            if platform.system() == "Windows":
                langfile = platformSpecific.windowsSpecific.windowsLanguageFile()
            
            else:
                langfile = platformSpecific.unixSpecific.unixLanguageFile()
            
            try:
                with open(langfile, "r+") as language:
                    languageContent = language.readlines()
                    languageToUse = languageContent[0].replace("\n", "")
                
                if languageToUse != None:
                    if languageToUse.startswith("de"):
                        translations.de.translateQemuSysMissingDE(self, self.vmSpecs[1])

                    elif languageToUse.startswith("uk"):
                        translations.uk.translateQemuSysMissingUK(self, self.vmSpecs[1])

                    else:
                        translations.en.translateQemuSysMissingEN(self, self.vmSpecs[1])
            
            except:
                print("Translation can't be figured out. Using English language.")
                translations.en.translateQemuSysMissingEN(self, self.vmSpecs[1])