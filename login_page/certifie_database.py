import pymongo
from pymongo import MongoClient
import urllib.parse
from bson.objectid import ObjectId

import tkinter
from tkinter import *
import tkinter.font as font

username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('rnsit')

client = pymongo.MongoClient(
    "mongodb+srv://%s:%s@rnsit-ecert.7ufby.mongodb.net/test?retryWrites=true&w=majority" % (username, password))
db = client.get_database("test")
collections = db.hoge

root = Tk(className='Data Access')
root.title('Certify Login')
root.iconbitmap('icon_no_bg.ico')

v = StringVar()


l1font = font.Font(family='helvetica', size=11, weight='bold')
e1font = font.Font(family='courier', size=10, weight='bold')
l2font = font.Font(family='helvetica', size=11, weight='bold')
e2font = font.Font(family='courier', size=10, weight='bold')
l3font = font.Font(family='helvetica', size=11, weight='bold')
e3font = font.Font(family='courier', size=12, weight='bold')
l4font = font.Font(family='helvetica', size=11, weight='bold')
e4font = font.Font(family='courier', size=10, weight='bold')
l5font = font.Font(family='helvetica', size=12, weight='bold')
b1font = font.Font(family='helvetica', size=12, weight='bold')
b2font = font.Font(family='helvetica', size=12, weight='bold')
b3font = font.Font(family='helvetica', size=12, weight='bold')
e6font = font.Font(family='courier', size=10, weight='bold')


def count_certificates():
    count = collections.count_documents({})
    count = str(count)
    e3.insert(0, count)


def find_details():
    attrib1_key = e1.get()
    attrib1_val = e2.get()

    e1.delete(0, END)
    e2.delete(0, END)

    c = collections.find({"data." + attrib1_key: attrib1_val, "data." + "Name": "Shiv Swarup"})
    for a in c:
        print(a['_id'])
        print(a['data'])


def delete_certificate():
    id_no = e4.get()
    id_no = str(id_no)
    e4.delete(0, END)

    #collections.delete_one({'_id': "ObjectId("+id_no+")"})
    collections.delete_one({'_id': ObjectId(id_no)})

l1 = Label(root, text='Search Keys', font=l1font)
e1 = Entry(root, width=35, font=e1font, borderwidth=5, bg='yellow')
l2 = Label(root, text='Search Values', font=l2font)
e2 = Entry(root, width=35, font=e2font, borderwidth=5, bg='yellow')
l3 = Label(root, text='Count', font=l3font)
e3 = Entry(root, width=15, font=e3font, borderwidth=5, bg='yellow')
l4 = Label(root, text='ID No.', font=l4font)
e4 = Entry(root, width=35, font=e4font, borderwidth=5, bg='yellow')
l5 = Label(root, textvariable=v, font=l5font)
b1 = Button(root, text="Search", padx=10, pady=10, font=b1font, bg="green", command=find_details)
b2 = Button(root, text="Count", padx=10, pady=10, font=b2font, bg="orange", command=count_certificates)
b3 = Button(root, text="Delete", padx=10, pady=10, font=b3font, bg="red", command=delete_certificate)
e6 = Entry(root, width=35, font=e6font, borderwidth=5, bg='yellow')


l1.grid(row=0, column=0)
e1.grid(row=0, column=1, padx=2, pady=2, ipady=5)
l2.grid(row=1, column=0)
e2.grid(row=1, column=1, padx=2, pady=2, ipady=5)
l3.grid(row=0, column=2, padx=10, pady=10)
e3.grid(row=0, column=3, padx=2, pady=2, ipady=5)
l4.grid(row=0, column=4)
e4.grid(row=0, column=5, padx=2, pady=2, ipady=5)
l5.grid(row=3, column=2)
b1.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
b2.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
b3.grid(row=1, column=4, columnspan=2, padx=5, pady=5)

root.mainloop()




#5ef04cc809df29002907e2d3
