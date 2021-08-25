from api.courseTable.courseTable import CourseTable
from tkinter import * 
from wins.Moodle import createMoodleWin as moodleWin
from wins.Ncnu import createNcnuWin as ncnuWin 
from wins.NcnuMainWin import createNcnuMainWin as ncnuMainWin
from wins.courseTable import callTable
from wins.rigestryWin import createRigestryWin as rigestryWin

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
    createRigestryWin=Button(win,text="查詢活動報名資料",font="Helvetica 30",bg="black",fg="white",relief=GROOVE)

    createMoodleWin.config(command=lambda:moodleWin(moodle) )
    createNcnuMainWin.config(command=lambda:ncnuMainWin() )
    createNcnuWin.config(command=lambda:ncnuWin(ncnu) )
    createRigestryWin.config(command=lambda:rigestryWin())

    
    createMoodleWin.pack(fill="x")
    createNcnuMainWin.pack(fill="x")
    createNcnuWin.pack(fill="x")
    createTable.pack(fill="x")
    createRigestryWin.pack(fill="x")

    win.mainloop()


