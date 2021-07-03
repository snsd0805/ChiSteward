from tkinter import *
from wins.firstpage  import *
from wins.MainWin import *
from config  import CONFIG
from wins.Ncnu import *
from wins.Moodle import *
from wins.NcnuMainWin import *
from api.moodle import MoodleAPI
from api.ncnu import NcnuAPI
import threading

moodle = None
ncnu = None

win=Tk()
firstWin(win)
def checkJson():
    def login():
        global moodle, ncnu
        moodle = MoodleAPI(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
        ncnu = NcnuAPI(CONFIG['NCNU']['username'], CONFIG['NCNU']['password'])
        tempWin.destroy()
    
    tempWin = Tk()
    Label(tempWin, text="登入中...", font="50").pack()
    t = threading.Thread(target=login)
    t.start()

    tempWin.mainloop()

    if  moodle.status and ncnu.status:
        mainWin=Tk()
        createMainWin(mainWin,ncnu,moodle)
    else:
        mainWin=Tk()
        loginwin(mainWin)

win.protocol("WM_DELETE_WINDOW",checkJson())
    
    
