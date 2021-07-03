from api.courseTable.courseTable import CourseTable
from tkinter import * 
from Moodle import createMoodleWin as moodleWin
from Ncnu import createNcnuWin as ncnuWin 
from NcnuMainWin import createNcnuMainWin as ncnuMainWin
from courseTable import callTable

def createMainWin(win,ncnu,moodle):
    '''
    用綠色校園作為基底色
    以暨大的三大特色
    1.穿山甲-moodle
    2.櫻花-暨大官網 #ffcccc
    3.國際性-教務系統
    去做三個網頁的底色
    '''
    
    

    win.configure(bg="#b2ffa6")


    createMoodleWin=Button(win,text="Moodle",font="Helvetica 30",bg="#888084",fg="white",relief=GROOVE)
    createNcnuMainWin=Button(win,text="暨大官網",font="Helvetica 30",bg="#ffcccc",fg="white",relief=GROOVE)
    createNcnuWin=Button(win,text="暨大教務系統",font="Helvetica 30",bg="#df99ff",fg="white",relief=GROOVE)
    createTable=Button(win,text="自己課表自己排",font="Helvetica 30",bg="blue",fg="white",relief=GROOVE,command=lambda:callTable())

    createMoodleWin.config(command=lambda:moodleWin(moodle) )
    createNcnuMainWin.config(command=lambda:ncnuMainWin() )
    createNcnuWin.config(command=lambda:ncnuWin(ncnu) )

    
    createMoodleWin.pack(fill="x")
    createNcnuMainWin.pack(fill="x")
    createNcnuWin.pack(fill="x")
    createTable.pack(fill="x")

    win.mainloop()


