import pyrebase
from getpass import getpass
import tkinter
from tkinter import *

firebaseConfig ={
    'apiKey': "AIzaSyDe7D_QG3wBS_Yj-JLrF_6yv-G0tvJYnzM",
    'authDomain': "certifie-80c18.firebaseapp.com",
    'databaseURL': "https://certifie-80c18.firebaseio.com",
    'projectId': "certifie-80c18",
    'storageBucket': "certifie-80c18.appspot.com",
    'messagingSenderId': "327741687552",
    'appId': "1:327741687552:web:1f11760de0d8840f7ad5e5",
    'measurementId': "G-MGPVGXRZCZ"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def signup():
    email=input("Email-Id:")
    password=getpass("Password:")
    admin_key=getpass("Admin-Key:")
    if(admin_key=="certify@rnsit2020"):
       try:
           user=auth.create_user_auth_email_and_passowrd(email,password)
           print("Successfully created account!")
       except:
           print("Email already exists!")
           
    else:
        print("Invalid Admin-Key")
        

def login():
    email=input("Email-Id:")
    password=getpass("Password:")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        auth.send_email_verification(login['idToken'])
        print("Logged In")
    except:
        print("Invalid Email-Id or Password")
            


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



