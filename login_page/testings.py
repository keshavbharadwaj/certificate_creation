import tkinter
from tkinter import *
import tkinter.font as font

root = Tk(className='Testing')

xfont = font.Font(family='helvetica', size=8, weight='bold')

#top=Toplevel()
#top.title("Testings")
#top.configure(background="blue")


#grid System
# label1=Label(root, text="Hello World").grid(row=0,column=0)
# label2=Label(root, text="3x").grid(row=8,column=5)
# label3=Label(root, text="4x").grid(row=3,column=2)
# label4=Label(root, text="5x").grid(row=6,column=4)

#input field
e1=Entry(root, width=20, font=xfont, borderwidth=5, bg='yellow', fg='black').grid(row=0,column=0)
e1=Entry(root, width=20, font=xfont, borderwidth=5, bg='yellow', fg='black')
e1.grid(row=0,column=0)
e1.insert(0,"Enter Email Id: \t")



#buttons
#def enterin():
#     label1=Label(root, text=e1.get()).grid(row=3,column=3)
#
# button1=Button(root,text="clock", padx=50, pady=20, command=enterin, font=xfont, bg="orange").grid(row=2,column=3)
#button1=Button(root,text="Login", padx=50, pady=20, command=enterin, font=xfont, bg="orange").grid(row=2,column=3)
# button2=Button(root,text="date",state=DISABLED).grid(row=0,column=0)




root.mainloop()

