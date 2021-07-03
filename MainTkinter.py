from tkinter import *
from firstpage import *
from MainWin import *
from config import CONFIG
from Ncnu import *
from Moodle import *
from NcnuMainWin import *
from api.moodle import MoodleAPI
from api.ncnu import NcnuAPI

win=Tk()
firstWin(win)
def checkJson():
    moodle = MoodleAPI(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
    ncnu = NcnuAPI(CONFIG['NCNU']['username'], CONFIG['NCNU']['password'])
    if  moodle.status and ncnu.status:
        mainWin=Tk()
        createMainWin(mainWin,ncnu,moodle)
    else:
        mainWin=Tk()
        loginwin(mainWin)

win.protocol("WM_DELETE_WINDOW",checkJson())
    
    
