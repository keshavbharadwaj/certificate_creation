# import pyrebase
# from getpass import getpass
#
# firebaseConfig = {
#     "apiKey": "AIzaSyCKG2dxYzwnDcpwA3oqFPLOCCmXzLjqHe4",
#     "authDomain": "certifie-95f4a.firebaseapp.com",
#     "databaseURL": "https://certifie-95f4a.firebaseio.com",
#     "projectId": "certifie-95f4a",
#     "storageBucket": "certifie-95f4a.appspot.com",
#     "messagingSenderId": "975182601964",
#     "appId": "1:975182601964:web:0c52767e369d024c430fc9",
#     "measurementId": "G-WKMPS5VF65"
# }
#
#
# firebase = pyrebase.initialize_app(firebaseConfig)

import tkinter
from tkinter import *


def command1(event):
    if entry1.get() == 'admin' and entry2 == 'password' or entry1 == 'test' and entry2 == 'pass':
        root.deiconify()
        top.destroy()


def command2():
    top.destroy()
    root.destroy()
    sys.exit()


root = Tk()
top = Toplevel()

top.geometry('300x260')
top.title('Certifie Login')
top.configure(background='white')
photo2 = PhotoImage(file='logo.png')
photo = Label(top, image=photo2, bg='white')
lbl1 = Label(top, text='Username:', font=('Helvetica', 10))
entry1 = Entry(top)
lbl2 = Label(top, text='Password:', font=('Helvetica', 10))
entry2 = Entry(top, show="*")
button2 = Button(top, text='Exit', command=lambda: command2())

entry2.bind('<Return>', command1)

lbl3 = Label(top, text='Copyright (c) 2020 Certifie', font=('Ariel', 9))

photo.pack()
lbl1.pack()
entry1.pack()
lbl2.pack()
entry2.pack()
button2.pack()
lbl3.pack()

root.title('Main Screen')
root.configure(background='white')
root.geometry('855x650')

root.withdraw()
root.mainloop()

