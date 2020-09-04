import pymongo
from pymongo import MongoClient
import urllib.parse

import tkinter
from tkinter import *
import tkinter.font as font

username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('rnsit')

client = pymongo.MongoClient(
    "mongodb+srv://%s:%s@rnsit-ecert.7ufby.mongodb.net/test?retryWrites=true&w=majority" % (username, password))
db = client.get_database("test")
collections = db.certificates

count = collections.count_documents({})
print(count)

c = collections.find({"data.Name": "Ibrar Jahan M A"})
print(c)
for a in c:
    print(a['data']['Name'])


# def count_certificates():
#     count = collections.count_documents({})


# root = Tk(className='Data Access')
# root.title('Certify Login')
# root.iconbitmap('icon_no_bg.ico')
#
# v = StringVar()
#
# p1 = PhotoImage(file='logo.png')
# l1font = font.Font(family='helvetica', size=11, weight='bold')
# e1font = font.Font(family='courier', size=10, weight='bold')
# l2font = font.Font(family='helvetica', size=11, weight='bold')
# e2font = font.Font(family='courier', size=10, weight='bold')
# l3font = font.Font(family='helvetica', size=11, weight='bold')
# key_font = font.Font(family='courier', size=10, weight='bold')
# l4font = font.Font(family='helvetica', size=12, weight='bold')
# b1font = font.Font(family='helvetica', size=12, weight='bold')
# b2font = font.Font(family='helvetica', size=12, weight='bold')
#
# p1_l = Label(root, image=p1)
# l1 = Label(root, text='Search Keys', font=l1font)
# e1 = Entry(root, width=35, font=e1font, borderwidth=5, bg='yellow')
# l2 = Label(root, text='Search Values', font=l2font)
# e2 = Entry(root, show='*', width=35, font=e2font, borderwidth=5, bg='yellow')
# l3 = Label(root, text='Admin-Key', font=l3font)
# key1 = Entry(root, show='*', width=35, font=key_font, borderwidth=5, bg='yellow')
# l4 = Label(root, textvariable=v, font=l4font)
# b1 = Button(root, text="Login", padx=85, pady=25, font=b1font, bg="green")
# b2 = Button(root, text="Sign Up", padx=10, pady=10, font=b2font, bg="orange")
# b3 = Button(root, text="Reset Password", padx=10, pady=10, font=b2font, bg="red")
#
# p1_l.grid(row=0, column=0, padx=120, pady=10, columnspan=2)
# l1.grid(row=1, column=0)
# e1.grid(row=1, column=1, columnspan=3, padx=12, pady=12, ipady=5)
# l2.grid(row=2, column=0)
# e2.grid(row=2, column=1, columnspan=3, padx=12, pady=12, ipady=5)
# l3.grid(row=3, column=0)
# key1.grid(row=3, column=1, columnspan=3, padx=12, pady=12, ipady=5)
# l4.grid(row=4, column=1)
# b1.grid(row=5, column=1, padx=80, pady=10, rowspan=2)
# b2.grid(row=5, column=0, padx=5, pady=5)
# b3.grid(row=6, column=0, padx=5, pady=5)
#
# root.mainloop()
