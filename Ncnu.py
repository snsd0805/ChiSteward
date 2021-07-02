from tkinter import *
from api.ncnu import NcnuAPI
from config import CONFIG
from tkinter import messagebox
from tkhtmlview import HTMLLabel

def createNcnuWin():
    ncnu = NcnuAPI(CONFIG['NCNU']['username'], CONFIG['NCNU']['password'])
    if ncnu.status:
        def dlCurriculum(sem):
            if ncnu.getCourseTable(sem):
                messagebox.showinfo(message="{} 課表已經儲存到 ./{}課表.pdf".format(sem,sem))
            else:
                messagebox.showwarning(message="無法存取 {} 課表".format(sem))
        win=Tk()
        leftframe=Frame(win)
        leftframe.pack(fill=BOTH,side=LEFT)
        rightframe=Frame(win)
        rightframe.pack(side=RIGHT)
        
        textlb=Label(leftframe,text="我的學習紀錄",font="Helvetica 20")
        options=["各學期成績總覽","指定學期的成績列表","缺曠課記錄","獎懲紀錄","加選課程狀態"]
        optionsListbox=Listbox(leftframe)
        optionsListbox.insert(END,*options)
        chooseSemesterLb=Label(leftframe,text="指定學期",font="Helvetica 10")
        
        chooseSemesterEntry=Entry(leftframe)
        chooseSemesterEntry.insert(0,"1092")
        downloadBtn=Button(leftframe,text="下載課表",command=lambda:dlCurriculum(chooseSemesterEntry.get()))
        

        textlb.pack(fill=BOTH,expand=True)
        optionsListbox.pack(fill=BOTH)
        chooseSemesterLb.pack(fill=BOTH)
        chooseSemesterEntry.pack(fill=BOTH)
        downloadBtn.pack()
        
        htmlLb=HTMLLabel(rightframe,html="")
        htmlScrollbar=Scrollbar(rightframe)
        htmlLb.configure(yscrollcommand=htmlScrollbar.set)
                   
        htmlScrollbar.pack(fill=Y,side=RIGHT)
        htmlLb.pack()
        
        def itemSelected(event):
            obj = event.widget
            Index = obj.curselection()
            
            Html=''''''
            if str( obj.get(Index) ) == options[0]:
                scores = ncnu.getScoreSummary()
                for c in scores['semesters']:
                    Html+='''<tr> <td>學期:{}</td> <td>修課數:{}</td> <td>通過數:{}</td> <td>學分數:{}</td> <td>平均分數:{}</td> <td>排名:{}</td></tr><p>'''.format(c.get("semester"),
                            c.get("select_num"),c.get("pass_Num"),c.get("pass_credit"),c.get("average"),c.get("rank") ) 
                c=scores['sum']
                Html+='''<tr> <td>學期{}</td> <td>修課數:{}</td> <td>通過數:{}</td> <td>學分數:{}</td> <td>{}</td> <td>{}</td></tr>'''.format(c.get("semester"),
                        c.get("select_num"),c.get("pass_Num"),c.get("pass_credit"),c.get("average"),c.get("rank") )
                htmlLb.set_html(Html)        

            elif str( obj.get(Index) ) == options[1]:
                scores = ncnu.getScore(chooseSemesterEntry.get())
                for i in scores:
                    Html+="<tr><td>代號: {}</td> <td>班號: {}</td> <td>課程名稱: {}</td> <td>學分數: {}</td><td>老師: {}</td> <td>時間: {}</td> <td>地點: {}</td> <td>學分: {}</td> <td>分數: {}</td> <td>是否為必修?: {}</td></tr><p>".format(i.get("number"),
                            i.get("class"),i.get("name"),i.get("credit"),i.get("teacher"),i.get("time"),i.get("place"),i.get("credit"),i.get("score"),i.get("mandatary") ) 
                htmlLb.set_html(Html)
            elif str( obj.get(Index) ) == options[2]:
                absenceLogs = ncnu.getAbsenceLogs()
                if absenceLogs:
                    for log in absenceLogs:
                        Html+='''<tr> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td></tr>'''.format(log.get('id'),
                                log.get('semester'),log.get('classname'),log.get('date'),log.get('time'))
                    htmlLb.set_html(Html)            
                else:
                    Html+='''<h3>沒有任何缺曠課記錄</h3>'''
                    htmlLb.set_html(Html)
            elif  str( obj.get(Index) ) == options[3]:
                awardLogs = ncnu.getAwardLogs()
                if awardLogs:
                    for log in awardLogs:
                        Html+='''<tr> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td></tr>'''.format(log.get('id'),
                                log.get('semester'),log.get('award'),log.get('count'),log.get('content'))
                    htmlLb.set_html(Html)            
                else:
                    Html+='''<h3>沒有任何缺曠課記錄</h3>'''
                    htmlLb.set_html(Html)
            elif  str( obj.get(Index) ) == options[4]:
                logs = ncnu.getAddCourseLogs()
                if logs:
                    for log in logs:
                        Html+='''<tr> <td> {} </td> <td>學期: {} </td> <br> <td>課名: {} </td> <td>班別: {} </td> <td>加選狀態:{}</td></tr><p>'''.format(log.get('id'),
                                log.get('semester'),log.get('classname'),log.get('class'),log.get('check'))
                    htmlLb.set_html(Html)
        optionsListbox.bind("<<ListboxSelect>>", itemSelected)
    
        win.mainloop()
    
    else:
        print("NCNU 教務系統登入失敗")

createNcnuWin()
