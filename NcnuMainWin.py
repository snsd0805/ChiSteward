from tkinter import *
from tkhtmlview import HTMLLabel
from api.ncnuMain import NcnuMainAPI

def createNcnuMainWin():
    win=Tk()
    win.title("暨大官網最新資訊!")
    win.geometry("600x600")
    textLb=Label(win,text="暨大校園最新資訊",font="Helvetica 20",bg="#ffcccc")
    
    sb=Scrollbar(win)
    htmlLable=HTMLLabel(win)
    htmlLable.configure(yscrollcommand=sb.set)
    textLb.pack(fill="x")

    sb.pack(side=RIGHT,fill="y")
    htmlLable.pack(fill="both",expand=True)
    win.update()
    #=====爬=====
    ht='''<span style="background-color:#ffcccc"><h5>讀取中</h5></span>'''
    htmlLable.set_html(ht)
    win.update()
            
    main = NcnuMainAPI()
    Link='''<span style="background-color:#ffcccc"><ul>'''
    for anno in main.getAnno():
        Link+='''<li> <a href={}> {}</a> </li>'''.format(anno.get("link"),anno.get("title") )
    Link=Link+'''</ul></span>'''
    htmlLable.set_html(Link)


    
        

    win.mainloop()

