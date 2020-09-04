import pyrebase
from getpass import getpass
import tkinter
from tkinter import *
import tkinter.font as font

firebaseConfig = {
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

root = Tk(className='Certify')
root.title('Certify Login')
root.iconbitmap('icon_no_bg.ico')

v = StringVar()

p1 = PhotoImage(file='logo.png')
l1font = font.Font(family='helvetica', size=11, weight='bold')
e1font = font.Font(family='courier', size=10, weight='bold')
l2font = font.Font(family='helvetica', size=11, weight='bold')
e2font = font.Font(family='courier', size=10, weight='bold')
l3font = font.Font(family='helvetica', size=11, weight='bold')
key_font = font.Font(family='courier', size=10, weight='bold')
l4font = font.Font(family='helvetica', size=12, weight='bold')
b1font = font.Font(family='helvetica', size=12, weight='bold')
b2font = font.Font(family='helvetica', size=12, weight='bold')


def signup():
    email = e1.get()
    password = e2.get()
    admin_key = key1.get()

    e2.delete(0, END)
    key1.delete(0, END)

    if admin_key == "certify@rnsit2020":
        try:
            login = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(login['idToken'])
            v.set("Successfully created account! Please check mail ")
        except:
            v.set("Email already exists !")

    else:
        v.set("Invalid Admin-Key")


def login():
    email = e1.get()
    password = e2.get()

    e2.delete(0, END)

    try:
        auth.sign_in_with_email_and_password(email, password)
        v.set('Logged In')
    except:
        v.set('Invalid Email-Id / Password')


def reset_password():
    email = e1.get()

    try:
        auth.send_password_reset_email(email)
        v.set('Password reset link sent to mail')

    except:
        v.set('Email-Id Not registered')


p1_l = Label(root, image=p1)
l1 = Label(root, text='Email-Id', font=l1font)
e1 = Entry(root, width=35, font=e1font, borderwidth=5, bg='yellow')
l2 = Label(root, text='Password', font=l2font)
e2 = Entry(root, show='*', width=35, font=e2font, borderwidth=5, bg='yellow')
l3 = Label(root, text='Admin-Key', font=l3font)
key1 = Entry(root, show='*', width=35, font=key_font, borderwidth=5, bg='yellow')
l4 = Label(root, textvariable=v, font=l4font)
b1 = Button(root, text="Login", padx=85, pady=25, font=b1font, bg="green", command=login)
b2 = Button(root, text="Sign Up", padx=10, pady=10, font=b2font, bg="orange", command=signup)
b3 = Button(root, text="Reset Password", padx=10, pady=10, font=b2font, bg="red", command=reset_password)

p1_l.grid(row=0, column=0, padx=120, pady=10, columnspan=2)
l1.grid(row=1, column=0)
e1.grid(row=1, column=1, columnspan=3, padx=12, pady=12, ipady=5)
l2.grid(row=2, column=0)
e2.grid(row=2, column=1, columnspan=3, padx=12, pady=12, ipady=5)
l3.grid(row=3, column=0)
key1.grid(row=3, column=1, columnspan=3, padx=12, pady=12, ipady=5)
l4.grid(row=4, column=1)
b1.grid(row=5, column=1, padx=80, pady=10, rowspan=2)
b2.grid(row=5, column=0, padx=5, pady=5)
b3.grid(row=6, column=0, padx=5, pady=5)

root.mainloop()
