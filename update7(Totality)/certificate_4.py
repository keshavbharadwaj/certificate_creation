import sys
import os
import pyqrcode
import cv2
import urllib.parse
from bson.objectid import ObjectId
import pymongo
import requests
import json

from tkinter import *
from tkinter import messagebox, Tk
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from PIL import ImageTk, Image
import pandas as pd


import time
import numpy as np
import pyrebase

certino = 0
qrno = 0
l = []
serial = []
csvno = 0
sel = 0
pos = []
align = []
total = []
names = []
d = {}
img_paths = []
img_scl=[]
fonts_text = []
fontsscale_text = []
fontscolour_text = []
linetypes_text = []
thickness_text = []
imgdata=[]
Serialpresent=0

colour=(0,0,0)
def color_picker():
    global colour
    colour= colorchooser.askcolor()[0]
    colour=colour[-1::-1]

def fontchooser(fontype,fontsscale_text,fontscolour_text,linetypes_text,thickness_text,img1,align):
    try:
        x,y,_=img1.shape
        #print(fontype,fontsscale_text,fontscolour_text,linetypes_text,thickness_text)
        global colour
        colour=fontscolour_text
        toplevel = Toplevel()
        fontstyle=font.Font(family="Lucida Grande",size=10,weight="normal",underline=0,overstrike=0)
        toplevel.title("FONT SELECTOR")
        l=Label(toplevel,text="Select the required font attributes",bg="black",fg="white",font=fontstyle)
        toplevel.geometry("800x800")
        frame1=LabelFrame(toplevel,padx=20,pady=20,bg="black",fg="white",)
        frame2=LabelFrame(toplevel,padx=20,pady=20,bg="black",fg="white",)
        frame3=LabelFrame(toplevel,padx=20,pady=20,bg="black",fg="white",)
        frame4=LabelFrame(toplevel,padx=20,pady=20,bg="black",fg="white",)

        family=[ "FONT_HERSHEY_SIMPLEX" ,
            "FONT_HERSHEY_PLAIN",
            "FONT_HERSHEY_DUPLEX",
            "FONT_HERSHEY_COMPLEX",
            "FONT_HERSHEY_TRIPLEX" ,
            "FONT_HERSHEY_COMPLEX_SMALL",
            "FONT_HERSHEY_SCRIPT_SIMPLEX",
            "FONT_HERSHEY_SCRIPT_COMPLEX",
                          ]

        d={ "FONT_HERSHEY_SIMPLEX":cv2.FONT_HERSHEY_SIMPLEX ,
            "FONT_HERSHEY_PLAIN":cv2.FONT_HERSHEY_PLAIN,
            "FONT_HERSHEY_DUPLEX":cv2.FONT_HERSHEY_DUPLEX,
            "FONT_HERSHEY_COMPLEX":cv2.FONT_HERSHEY_COMPLEX,
            "FONT_HERSHEY_TRIPLEX":cv2.FONT_HERSHEY_TRIPLEX,
            "FONT_HERSHEY_COMPLEX_SMALL":cv2.FONT_HERSHEY_COMPLEX_SMALL,
            "FONT_HERSHEY_SCRIPT_SIMPLEX":cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            "FONT_HERSHEY_SCRIPT_COMPLEX":cv2.FONT_HERSHEY_SCRIPT_COMPLEX
                       }


        font_family=StringVar()
        font_family.set(list(d.keys())[list(d.values()).index(fontype)])
        drop=OptionMenu(frame1,font_family,*family)
        l1=Label(frame1,text="Select the font type",bg="black",fg="white",)
        lcol=Label(frame1,text="Select the colour of font",bg="black",fg="white",)
        bcolour=Button(frame1,text="colour Chooser",font=fontstyle,padx=5,pady=5,command=lambda:color_picker())

        l2=Label(frame2,text="Select the font scale",bg="black",fg="white",)
        scales=StringVar()
        thickness=IntVar()
        linetype=IntVar()
        linetype.set(linetypes_text)
        thickness.set(int(thickness_text))
        scales.set(fontsscale_text)
        e=Entry(frame2,text=scales)
        e2=Entry(frame2,text=thickness)
        l3=Label(frame2,text="Select the Thickness",bg="black",fg="white",)
        l4=Label(frame2,text="Select the linetype",bg="black",fg="white",)
        e3=Entry(frame2,text=linetype)

        l.grid(row=0,column=0,columnspan=2)

        frame1.grid(row=1,column=0)
        l1.grid(row=0,column=0)
        drop.grid(row=0,column=1)
        lcol.grid(row=1,column=0)
        bcolour.grid(row=1,column=1)

        frame2.grid(row=1,column=1)
        l2.pack()
        e.pack()
        l3.pack()
        e2.pack()
        l4.pack()
        e3.pack()




        sets=IntVar()
        sets.set(0)
        submits=IntVar()
        submits.set(0)
        button2=Button(toplevel,text="Done",command=lambda:{submits.set(1),sets.set(1)}).grid(row=3,column=1)
        button=Button(toplevel,text="Set",command=lambda:sets.set(1)).grid(row=2,column=1)
        while(1):
            pmag=img1.copy()
            try:
                fontsscale_text=float(e.get())
            except:
                pass
            try:
                thickness_text=int(e2.get())
            except:
                pass
            try:
                linetypes_text=int(e3.get())
            except:
                pass

            m="abcABCefcEFC0123456789"
            #a2=np.ones((x,y,3), np.uint8)*255
            fontype=d[font_family.get()]
            cv2.putText(pmag, m,align,fontype,fontsscale_text,colour,thickness_text,linetypes_text)
            #cv2.putText(a, names[i], align[p], font_text, fontscale_text, fontcolour_text, linetype_text)
            a2 = cv2.resize(pmag, (700, 700), cv2.INTER_AREA)
            a2 = cv2.cvtColor(a2, cv2.COLOR_BGR2RGB)
            ph = ImageTk.PhotoImage(image=Image.fromarray(a2))
            pdesc = Label(toplevel, image=ph)
            pdesc.grid(row=4, column=0,rowspan=2,columnspan=5)
            if submits.get() == 1:
                toplevel.destroy()
                return fontype, fontsscale_text, colour, linetypes_text, thickness_text

            toplevel.wait_variable(sets)
        toplevel.mainloop()
    except:
        return fontype, fontsscale_text, colour, linetypes_text, thickness_text






def add_data(path):
    try:
        login_url='https://rnsit-ecert.herokuapp.com/users/login'
        login_data={
                    "userName":"admin",
                    "password":"password"
        }
        session = requests.session()

        r = session.post(login_url,data=login_data)
        user_token = (json.loads(r.text))['data']['userToken']
        #print(user_token)
        #print(path)
        datagram = pd.read_csv(path)
        datagram['verifyUrl']=np.nan
        datagram.drop(datagram.index,inplace=True)
        #print(r.text)
        #print(user_token)
        file_data = {
            'file': (path, open(path, 'rb'))
        }
        form_data = {
            'file': path,
            'usertoken': user_token
        }
        response = requests.post('https://rnsit-ecert.herokuapp.com/data/add-files', files=file_data, data=form_data)
        #print(response.text)
        l=[]
        #print("here")
        for i in json.loads(response.text)['data']['result']:

            k = pd.DataFrame(i, index=[0])
            datagram=datagram.append(k)
           # datagram.append(k)
            #datagram.append(i)

        logout_url = 'https://rnsit-ecert.herokuapp.com/users/logout/' + user_token
        logout_response = requests.get(logout_url)

        datagram.rename(columns={'verifyUrl':'serial'},inplace=True)
        datagram.drop(datagram.columns[datagram.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
        datagram.to_csv(path,index=False)

    except:
        #print("Unexpected error:", sys.exc_info()[0])
        #print("error")
        logout_url = 'https://rnsit-ecert.herokuapp.com/users/logout/' + user_token
        logout_response = requests.get(logout_url)
        #print(logout_response.text)



def image_resizer(src,scale):

    scale=scale*100
    width = int(src.shape[1] * scale / 100)
    height = int(src.shape[0] * scale / 100)
    dsize = (width, height)
    output = cv2.resize(src, dsize)
    return output




def draw_circle(event, x, y, flags, param):
    global sel
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(sample, (x, y), 10, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        align.append((mouseX, mouseY))
        sel = sel - 1
        return (mouseX, mouseY)


def selectiononcertificate():
    global sel, sample
    sel = sel + 1
    sample = img1.copy()
    root.update()
    cv2.namedWindow('sample', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('sample', draw_circle)
    while (1):
        cv2.imshow('sample', sample)
        k = cv2.waitKey(20) & 0xFF
        if sel == 0:
            cv2.destroyAllWindows()
            a = messagebox.showinfo("slection done", "You have completed the selection process")
            if a == "ok":
                break

    show_sel()


def fonter(i):
    global fonts_text, fontsscale_text, fontscolour_text, linetypes_text, thickness_text, img1, align
    #print(i)
    p = 0
    for j in pos:
        if j == i:
            break
        p = p + 1

    fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i] = fontchooser(
        fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i], img1, align[p])


def show_sel():
    global align, frames2, serial, font_text, fontscale_text, fontcolour_text, linetype_text
    global scl, frames1, pos,img_paths,imgdata

    frames.destroy()
    frames1 = Canvas(root)

    filename = PhotoImage(file=".img\\t3_2.png")
    background_label = Label(frames1, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    a = img1.copy()
    p = 0
    if Serialpresent==1:
        l9 = Label(frames1, text="choose scale of qr code between 1-9    ", font=fontstyle5,bg="black",fg="white")
        clicked = IntVar()
        clicked.set(3)
        drop1 = OptionMenu(frames1, clicked, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        drop1.configure(bg="black",fg="white")
        l9.grid(row=0, column=0, columnspan=4)
        drop1.grid(row=0, column=4)


    row_no=1
    img_drop=[]
    for i in range(len(img_paths)):
        k = DoubleVar()
        k.set(1.0)
        img_drop.append(k)

    #creating radio buttons for all images with value
    try:
        for i in range(len(img_paths)):
            limg = Label(frames1, text="choose scale of " + imgdata.columns[i] + " between 10-150%", font=fontstyle5,bg="black",fg="white").grid(row=row_no,
                                                                                                                 column=0,
                                                                                                                 columnspan=4)
            imgscale = OptionMenu(frames1,img_drop[i], 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,1.3,1.4,1.5)
            imgscale.configure(bg="black",fg="white")
            imgscale.grid(row=row_no, column=4)
            row_no += 1


    except:
        print("Oops!", sys.exc_info(), "occurred.")


    row_no+=1
    lattri = Label(frames1, text="Font selection for Each Attribute", font=fontstyle5_2,bg="black",fg="white")
    lattri.grid(row=row_no, column=1, columnspan=5)
    r = row_no+1
    c = 0
    b = []
    global fonts_text, fontsscale_text, fontscolour_text, linetypes_text, thickness_text
    fonts_text = [cv2.FONT_HERSHEY_PLAIN] * (len(names))
    fontsscale_text = [10] * (len(names))
    fontscolour_text = [(0, 0, 0)] * (len(names))
    linetypes_text = [10] * (len(names))
    thickness_text = [5] * (len(names))

    for i in range(len(names)):
        if names[i] == "serial":
            continue
        if names[i].startswith("img"):
            continue
        b = Button(frames1, text=names[i], padx=40, pady=10,bg="black",fg="white")
        b.configure(command=lambda j=b['text']: fonter(names.index(j)))
        b.grid(row=r, column=c,columnspan=2)
        c += 2
        if c > 6:
            c = 0
            r += 1
    frames1.pack(expand=True,fill=BOTH)
    var = IntVar()
    var.set(0)

    button4 = Button(frames1, text="submit", font=fontstyle2, padx=100, pady=10, command=lambda: var.set(1),bg="black",fg="white").grid(
        row=r + 2,
        column=2, columnspan=2)
    back = Button(frames1, text="Back", font=fontstyle2, padx=100, pady=10, command=lambda: mainframe(frames1),bg="black",fg="white").grid(
        row=r + 2, column=0, columnspan=2)
    frames1.wait_variable(var)

    for i in range(len(img_paths)):
        img_scl.append(img_drop[i].get())
    m=0
    #print(img_scl)
    for i in pos:
        if names[i].startswith("img"):

            sampleimg = cv2.imread(img_paths[m]+'/'+d[names[i]][0])
            sampleimg=image_resizer(sampleimg,img_scl[m])

            m=m+1


            try:
                global align

                x, y, _ = sampleimg.shape
                #print(x,y)
                #print(align[p],align[p][0] + x)
                a[align[p][1]:align[p][1] + x, align[p][0]:align[p][0] + y] = sampleimg



            except:
                #print("Oops!", sys.exc_info(), "occurred.")
                k = messagebox.showerror("Error", "Image " +names[i]+" is overflowing out of the certificate Please choose the scale again")
                if (k == "ok"):
                    frames1.destroy()
                    img_scl.clear()
                    show_sel()
                    return

        else:
            cv2.putText(a, names[i], align[p], fonts_text[i], fontsscale_text[i], fontscolour_text[i], thickness_text[i],
                        linetypes_text[i])
        p = p + 1

    if Serialpresent==1:
        scl = clicked.get()




    if Serialpresent==1:
        url = pyqrcode.create(serial[0])
        url.png('urls/sample.png', scale=scl)

        b = cv2.imread("urls/sample.png")
        x, y, _ = b.shape
        try:
            a[align[-1][1]:align[-1][1] + y, align[-1][0]:align[-1][0] + x] = b
        except:
            k = messagebox.showerror("Error", "QR Code is overflowing out of the image Please choose the scale again")
            if (k == "ok"):
                frames1.destroy()
                show_sel()
                return

    #print("SO we have made it to the end still not displaying")
    frames1.destroy()

    frames1=Canvas(root)

    filename = PhotoImage(file=".img\\t3_2.png")
    background_label = Label(frames1, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frames1.pack(expand=True, fill=BOTH)

    l8 = Label(frames1, text="Default certificate",font=fontstyle3,bg="black",fg="white")
    l8.grid(row=0,column=0)

    a = cv2.resize(a, (990, 660), cv2.INTER_AREA)
    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(image=Image.fromarray(a))
    p1 = Label(frames1, image=photo)
    p1.grid(row=1, column=0)
    root.update()
    ask = messagebox.askyesno("alignment", "are you satisfied with the alignment?")

    if ask == False:
        align.clear()
        pos.clear()
        img_scl.clear()
        global sample
        sample = img1.copy()
        frames1.destroy()
        selection()
    elif ask == True:
        frames1.destroy()
        frames2 = Canvas(root)

        filename = PhotoImage(file=".img\\t3_2.png")
        background_label = Label(frames2, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        frames2.pack(expand=True, fill=BOTH)

        l10 = Label(frames2, text="selection confirmed generating the certificates", font=fontstyle3,
                    bg="black",fg="white").place(x=200,y=50)

        root.update()


def selection():
    try:
        global sel
        global frames
        try:
            frame3.destroy()
        except:
            pass
        frames = Canvas(root)
        frames.pack(fill=BOTH, expand=True)

        filename = PhotoImage(file=".img\\t3_2.png")
        background_label = Label(frames, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        l5 = Label(frames, text="Welcome to the certificate formatting screen", font=fontstyle4,bg="black",fg="white")
        l5.place(x=200,y=30)
        sel = 0
        s = ''
        global names, d

        for i in range(len(names)):
            if names[i] == 'serial':
                continue
            sel = sel + 1
            pos.append(i)
            s = s + names[i] + "\r"
        if Serialpresent==1:
            s = "Please choose by double clicking on the certificate the location of\r " + s + "QRCODE\r in the same order"
        else:
            s = "Please choose by double clicking on the certificate the location of\r " + s +"in the same order"
            sel-=1
        l6 = Label(frames, text=s, font=fontstyle4_2,bg="black",fg="white")
        l6.place(x=200,y=150)

        back = Button(frames, text="Back", font=fontstyle2, padx=40, pady=20, command=lambda: mainframe(frames),bg="black",fg="white").place(x=450,y=600)
        selectiononcertificate()
    except:
        root.destroy()


def segmentation(img, initialx, initialy, s):
    x = initialx
    y = initialy
    font = cv2.FONT_HERSHEY_PLAIN
    fontscale = 0.5
    linetype = 1
    thickness = 1
    for m in s:
        fontcolour = img[x, y]
        b = int(fontcolour[0])
        g = int(fontcolour[1])
        r = int(fontcolour[2])
        r = ragecalc(r)
        g = ragecalc(g)
        b = ragecalc(b)

        cv2.putText(img, m, (y, x), font, fontscale, (b, g, r), thickness, linetype)
        y = y + 6
    x = x + 10
    return (x, y)


def ragecalc(r):
    if r > 0:
        return (r - 1)
    else:
        return (r + 1)


def qrmadu(no):
    global serial
    s = serial[no]
    url = pyqrcode.create(s)
    url.png("urls/" + str(no) + ".png", scale=scl)


def certificate(csvno, c):
    global align, d, pos
    a = img1.copy()
    global fonts_text, fontsscale_text, fontscolour_text, linetypes_text, thickness_text
    if c == 0:
        g = 0
        m=0
        for i in pos:
            if names[i].startswith("img"):
                addimg=cv2.imread(img_paths[m]+'/'+d[names[i]][csvno])
                addimg=image_resizer(addimg,img_scl[m])
                x,y,_=addimg.shape
                a[align[g][1]:align[g][1] + x, align[g][0]:align[g][0] + y]=addimg
                m+=1


            else:
                # print(d[names[i]][csvno], align[g],fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i])
                # print(fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i])
                cv2.putText(a, str(d[names[i]][csvno]), align[g], fonts_text[i], fontsscale_text[i], fontscolour_text[i],
                             thickness_text[i],linetypes_text[i])
            g = g + 1
        if Serialpresent==1:
            b = cv2.imread("urls/" + str(csvno) + ".png")
            x, y, _ = b.shape
            a[align[-1][1]:align[-1][1] + y, align[-1][0]:align[-1][0] + x] = b

        cv2.imwrite("Certificates/" + d[names[0]][csvno] + "_"+str(csvno)+ ".png", a)


def steganography():
    x = 50
    y = 50
    x, y = segmentation(img1, x, y, "2K16")
    x, y = segmentation(img1, x, y, "KB")
    x, y = segmentation(img1, x, y, "VA")
    x, y = segmentation(img1, x, y, "CJ")
    x, y = segmentation(img1, x, y, "VU")
    x, y = segmentation(img1, x, y, "SA")
    x, y = segmentation(img1, x, y, "SH")
    x, y = segmentation(img1, x, y, "SP")


def steganography2(steg):
    x = 50
    y = 50
    for a in steg:
        x, y = segmentation(img1, x, y, a)
    segmentation(img1, x, y, "V2")


def certificategenerator(csvno, c):
    if Serialpresent==1:
        qrmadu(csvno)
    certificate(csvno, c)


def log():
    total = []
    file = open("log.txt", "a")
    for i in range(len(l)):
        total.append(l[i] + '-' + names[i])
    b = '\n'.join(total)
    file.write(b)


def main():
    frame2.destroy()
    steg = '0'
    global frame3, d, names, serial,imgdata,Serialpresent

    try:
        frame3 = Canvas(root)
        frame3.pack(fill=BOTH, expand=True)

        C = Canvas(frame3, height=1000, width=700)
        filename = PhotoImage(file=".img\\t3_2.png")
        background_label = Label(frame3, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        r = messagebox.askyesno("steganography", "Do you want to perform steganography?")
        if r == True:
            back="black"
            fore="white"
            l2 = Label(frame3, text="Please Enter the login password", font=fontstyle5,bg=back,fg=fore).place(x=300,y=50)
            e = Entry(frame3,bd=10,bg=fore,fg=back,width=30,show="*")
            e.place(x=700,y=50)
            button3 = Button(frame3, text="  Back    ", font=fontstyle2, padx=45, pady=10,
                             command=lambda: mainframe(frame3),bg=back,fg=fore).place(x=500,y=100)
            v = IntVar()
            v.set(0)
            submit = Button(frame3, text="  SUBMIT  ", padx=40, pady=10, font=fontstyle2, command=lambda: v.set(1),bg=back,fg=fore).place(
                x=700,y=100)
            frame3.wait_variable(v)
            if e.get() != "gaanekano2016":
                messagebox.showerror("password", "password inccorect")
                frame3.destroy()
                main()
            else:
                messagebox.showinfo("password", "password correct")
                frame3.destroy()

                frame10 = Canvas(root)
                frame10.pack(fill=BOTH,expand=True)

                C = Canvas(frame10, height=1000, width=800)
                filename = PhotoImage(file=".img\\t3_2.png")
                background_label = Label(frame10, image=filename)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)

                stega = IntVar()
                stega.set(1)

                back="black"
                fore="White"
                l10 = Label(frame10, text="Enter alpha code", font=fontstyle3,bg=back,fg=fore).place(x=400,y=50,anchor="center")
                e = Entry(frame10,bd=10,fg=back,bg=fore)
                e.place(x=600,y=50,anchor="center")
                submit = Button(frame10, text="submit", font=fontstyle2, padx=80, pady=20, command=lambda: stega.set(1),bg=back,fg=fore)
                submit.place(x=550,y=120,anchor="center")
                root.update()
                frame10.wait_variable(stega)
                steg = e.get()
                frame10.destroy()
        elif r == False:
            frame3.destroy()
            pass

        if steg != '0':
            steganography2(steg)
        else:
            steganography()

        frame3 = Canvas(root)
        frame3.pack(fill=BOTH, expand=True)


        filename = PhotoImage(file=".img\\t3_2.png")
        background_label = Label(frame3, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        var = IntVar()
        var.set(0)
        back = Button(frame3, text="Back", font=fontstyle2, padx=40, pady=10, command=lambda: var.set(1),bg="black",fg="white")
        response1 = messagebox.askyesno("CSV?", "Do you want to generate certificates through CSV file?")
        if (response1 == 1):
            l4 = Label(frame3, text="Please choose the location of the CSV file", font=fontstyle4,bg="black",fg="white")

            l4.place(x=200,y=50)
            back.place(x=450,y=170)
            path2 = filedialog.askopenfilename(initialdir=" ", title="select the csv",
                                               filetypes=(("csv files", "*.csv"),))

            response2 = messagebox.askyesno("QR Code?", "Do you want QR Code authentication in certificate?")
            if response2==1:
                Serialpresent=1
                lwait= Label(frame3, text="Please wait.................................", font=fontstyle4,bg="black",fg="white")
                lwait.place(x=200,y=100)
                back.destroy()
                root.update()
                add_data(path2)
            else:
                Serialpresent=0
                d=pd.read_csv(path2)
                d['serial']=''
                d.to_csv(path2,index=False)

            d = pd.read_csv(path2)
            d.drop(d.columns[d.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
            names = list(d.columns)


            try:
                serial = d['serial']
            except:
                response = messagebox.showerror("No serial in csv", "There is no serial in csv")
                exit()

            imgdata = d.filter(regex='img')
            #print(imgdata)
            if imgdata.empty:
                pass
            else:
                #print("YO BOIS")
                # imglist=0
                for i in imgdata.columns:
                    frame3.destroy()
                    #print("YO here we are")
                    frame3 = Canvas(root)
                    frame3.pack(fill=BOTH, expand=True)

                    C = Canvas(frame3, height=1000, width=700)
                    filename = PhotoImage(file=".img\\t3_2.png")
                    background_label = Label(frame3, image=filename)
                    background_label.place(x=0, y=0, relwidth=1, relheight=1)

                    img_paths.append(
                        filedialog.askdirectory(title="Select the folder where the " + i + " images are stored"))


            #print(img_paths)

            selection()
            global csvno
            cno = len(serial)
            for i in names:
                total.append(d[i])

            for csvno in range(cno):
                c = 0
                certificategenerator(csvno, c)
            frames2.destroy()

            frames3 = Canvas(root)
            frames3.pack(expand=True,fill=BOTH)

            filename = PhotoImage(file=".img\\t3_2.png")
            background_label = Label(frames3, image=filename)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)


            l12 = Label(frames3, text="ALL certificates have been generated !!", font=fontstyle, bg="black",fg="white"
                        ).pack()
            root.update()
            root.after(2000)
            frames3.destroy()



        elif (response1 == 0):
            g = messagebox.showinfo("csv",
                                    "Please create the csv file with the necessary requirment first,for more information refer to the read me file")
            if g == "ok":
                root.destroy()

    except:
        frame3.wait_variable(var)
        mainframe(frame3)


def main2():
    frame1.destroy()
    frame2 = Canvas(root)
    frame2.pack(fill=BOTH, expand=True)

    filename = PhotoImage(file=".img\\t3_2.png")
    background_label = Label(frame2, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    l2 = Label(frame2, text="Please Enter the login password", font=fontstyle5,bg="black",fg="white").place(x=80, y=10)
    e = Entry(frame2,show="*",width=45, borderwidth=5,)
    e.place(x=500,y=10)
    button3 = Button(frame2, text="  Back    ", font=fontstyle2, padx=60, pady=10,
                     command=lambda: mainframe(frame2),bg="black",fg="white").place(x=80,y=60)
    v = IntVar()
    v.set(0)
    submit = Button(frame2, text="  SUBMIT  ", padx=60, pady=10, font=fontstyle2, command=lambda: v.set(1),bg="black",fg="white").place(x=600,y=60)

    frame2.wait_variable(v)
    if e.get() != "gaanekano2016":
        messagebox.showerror("password", "password inccorect")
        frame2.destroy()
        main2()
    else:
        messagebox.showinfo("password", "password correct")
        frame2.destroy()

        frame3 = Canvas(root)
        frame3.pack(fill=BOTH, expand=True)

        filename = PhotoImage(file=".img\\t3_2.png")
        background_label = Label(frame3, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        l3 = Label(frame3, text="Decoding Selection Screen", font=fontstyle5,bg="black",fg="white")
        l3.place(x=300,y=50)
        mark = cv2.imread(".img\\decodelogo.png")
        mark = cv2.resize(mark, (400, 400), cv2.INTER_AREA)
        mark = cv2.cvtColor(mark, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(mark))
        p1 = Label(frame3, image=photo)
        p1.place(x=300, y=150)
        button3 = Button(frame3, text="  Back    ", font=fontstyle2, padx=32, pady=20,
                         command=lambda: mainframe(frame3),bg="black",fg="white")
        button3.place(x=400, y=600)
        path1 = filedialog.askopenfilename(initialdir=" ", title="select the originalcertificate",
                                           filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
        path2 = filedialog.askopenfilename(initialdir=" ", title="select the certificate to be decoded",
                                           filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
        img3 = (img1 - img2) * (255, 255, 255)
        cv2.imwrite("decoded.png", img3)
        l3.destroy()
        button3.destroy()
        l4 = Label(frame3, text="DECODING COMPLETE!!", font=fontstyle,bg="black",fg="white")
        l4.place(x=300,y=50)
        root.update()
        root.after(2000)
        mainframe(frame3)


def generate():
    try:
        global img1, frame2
        frame1.destroy()
        frame2 = Canvas(root)
        frame2.pack(fill=BOTH, expand=True)

        C = Canvas(frame2, height=1000, width=700)
        filename = PhotoImage(file=".img\\t3_2.png")
        background_label = Label(frame2, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back = "black"
        fore = "white"
        l2 = Label(frame2, text="Please choose the path of the certificate", font=fontstyle4, bg=back, fg=fore)
        l2.place(x=500, y=100, anchor="center")
        var = IntVar()
        var.set(0)
        back = Button(frame2, text="Back", font=fontstyle2, padx=40, pady=10, command=lambda: var.set(1), bg=back,
                      fg=fore).place(x=400, y=200)
        frame2.pack()

        path1 = filedialog.askopenfilename(initialdir=" ", title="select the certificate",
                                           filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))

        #print(path1)

        if path1==''or path1==" ":
            raise

        img1 = cv2.imread(path1)
        main()
        mainframe(frame)

    except:
        #print("HERE")
        frame2.wait_variable(var)
        mainframe(frame2)


def DEVS():
    frame1.destroy()

    frame2 = Canvas(root)
    frame2.pack(fill=BOTH, expand=True)

    C = Canvas(frame2, height=1000, width=700)
    filename = PhotoImage(file=".img\\t3_2.png")
    background_label = Label(frame2, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    fontstyle = font.Font(family="Lucida Grande", weight="normal", slant="italic", underline=1, size=30)

    var = IntVar()
    var.set(0)

    fore = "white"
    back = "black"
    dev = Label(frame2, text="LEGENDS 2k16", font=fontstyle, fg=fore, bg=back).place(x=600, y=50)
    fontstyle = font.Font(family="Lucida Grande", weight="normal", slant="italic", underline=0, size=20)
    dev2 = Label(frame2,
                 text="V KESHAV BHARADWAJ\rVIVEK ADI\rCHIRANJIT PATEL\rVIVEK URANKAR\rSHANKAR ANBALAGAN\rSOURAV P ADI",
                 font=fontstyle, fg=fore, bg=back).place(x=600, y=150)
    pic = cv2.imread(".img\\crazy.jpg")
    pic = cv2.resize(pic, (400, 400), cv2.INTER_AREA)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    photo1 = ImageTk.PhotoImage(image=Image.fromarray(pic))
    logo = Label(frame2, image=photo1).place(x=1200, y=300)
    button3 = Button(frame2, text="  Back    ", padx=30, pady=10, font=fontstyle2,
                     command=lambda: mainframe(frame2), fg=fore, bg=back).place(x=650, y=500)
    frame2.wait_variable(var)

def database():

    def count_certificates():
        e3.delete(0, "end")
        count = collections.count_documents({})
        count = str(count)
        e3.insert(0, count)

    def find_details():
        id_list = []
        data_list = []

        def delete_certificate(id_no):
            id_no = str(id_no)
            e4.delete(0, END)
            collections.delete_one({'_id': ObjectId(id_no)})

        def deletionmain():
            #print(listbox.curselection())
            #print(listbox.get(listbox.curselection()))

            for j in listbox.curselection():
                #print(j)
                #print(id_list[j])
                #print("Remaining_deleted ",data_list)
                delete_certificate(id_list[j])
                id_list.pop(j)
                data_list.pop(j)
                listbox.delete(j)


        attrib1_key = e1.get()
        attrib1_val = e2.get()

        e1.delete(0, END)
        e2.delete(0, END)

        if attrib1_key!="":
            attrib1_key=attrib1_key.split(',')
            attrib1_val=attrib1_val.split(',')


        s={}
        if attrib1_key!='':
            for i in range(len(attrib1_key)):
                s["data."+attrib1_key[i]]=attrib1_val[i]

        #print(s)
        c = collections.find(s)
        for a in c:
            id_list.append(a['_id'])
            data_list.append(a['data'])
        #print(len(data_list))

        if len(id_list) != 0:
            remove=["{","}","[","]"]
            for i in range(len(data_list)):
                data_list[i] = str(data_list[i])
                for j in remove:
                    data_list[i]=data_list[i].replace(j,"")


            scrollbar = Scrollbar(framedb,width=20,highlightthickness=10)
            scrollbar2 = Scrollbar(framedb,orient=HORIZONTAL,width=20)

            scrollbar.pack(side=RIGHT,fill=Y)
            scrollbar2.pack(side=BOTTOM,fill=X)


            listbox = Listbox(framedb,width=120,height=25,font=dbfont)
            listbox.place(x=0,y=100)

            for i in range(len(data_list)):
                listbox.insert(END, data_list[i])

            listbox.config(yscrollcommand=scrollbar.set)
            listbox.config(xscrollcommand=scrollbar2.set)
            scrollbar.config(command=listbox.yview)
            scrollbar2.config(command=listbox.xview)




            choice=IntVar()
            choice.set(0)

            b3 = Button(framedb, text="Delete", padx=40, pady=10, font=fontstyle2, command=deletionmain,bg="red",fg="black")
            b3.place(x=800,y=600)

            b4= Button(framedb, text="Done", padx=40, pady=10, font=fontstyle2, command=lambda:choice.set(1),bg="black",fg="white")
            b4.place(x=500,y=600)
            root.wait_variable(choice)
            #print("DONE!!!!!")
            listbox.destroy()
            scrollbar.destroy()
            scrollbar2.destroy()
            b3.destroy()
            b4.destroy()

        #print("done")








    frame1.destroy()
    username = urllib.parse.quote_plus('root')
    password = urllib.parse.quote_plus('root123')
    client = pymongo.MongoClient(
        "mongodb+srv://%s:%s@rnsit-ecert.7ufby.mongodb.net/test?retryWrites=true&w=majority" % (username, password))
    db = client.get_database("test")
    collections = db.certificates

    framedb = Canvas(root)
    framedb.pack(fill=BOTH, expand=True)

    C = Canvas(framedb, height=1000, width=700)
    filename = PhotoImage(file=".img\\t3_2.png")
    background_label = Label(framedb, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)



    l1 = Label(framedb, text='Search Keys', font=dbfont,bg="black",fg="white").place(x=10,y=10)
    e1 = Entry(framedb, width=35, borderwidth=5,font=dbfont)
    e1.place(x=120,y=10)
    l2 = Label(framedb, text='Search Values', font=dbfont,bg="black",fg="white").place(x=10,y=35)
    e2 = Entry(framedb, width=35,  borderwidth=5,font=dbfont)
    e2.place(x=120,y=35)

    l3 = Label(framedb, text='Count', font=dbfont,bg="black",fg="white").place(x=500,y=10)
    b2 = Button(framedb, text="Count", padx=30, pady=5, font=fontstyle2, command=count_certificates,bg="black",fg="white").place(x=500,y=45)

    e3 = Entry(framedb, width=15,borderwidth=5,font=dbfont)
    e3.place(x=570,y=10)
    l4 = Label(framedb, text='ID No.', font=fontstyle3)
    e4 = Entry(framedb, width=35,borderwidth=5,font=fontstyle3)

    b1 = Button(framedb, text="Search", padx=30, pady=5, font=fontstyle2,  command=find_details,bg="black",fg="white").place(x=5,y=65)

    finish=IntVar()
    finish.set(0)
    dbback=Button(framedb, text="Back", padx=30, pady=10, font=fontstyle2,  command=lambda:finish.set(1),bg="black",fg="white").place(x=30,y=600)
    root.wait_variable(finish)
    mainframe(framedb)






def mainframe(x):
    global frame1
    x.destroy()
    certino = 0
    qrno = 0
    l = []
    names = []
    csvno = 0
    sel = 0
    total = []
    fonts_text = []
    fontsscale_text = []
    fontscolour_text = []
    linetypes_text = []
    thickness_text = []
    imgdata=[]
    img_paths=[]
    align.clear()
    pos.clear()
    img_scl.clear()


    var = IntVar()
    var.set(0)

    WIDTH, HEIGTH = 1000, 700
    frame1 = Canvas(root,height=1000, width=700)
    frame1.pack(fill=BOTH, expand=True)
    #print("I can make it till here")
    filename = PhotoImage(file=".img\\t3_2.png")
    background_label = Label(frame1, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    fore = "white"
    back = "black"
    l1 = Label(frame1, text="WELCOME TO CERTIFICATE GENERATOR", padx=10, pady=10, font=fontstyle, fg=fore,
               background=back)
    l1.place(x=100, y=100)
    # logo=Label(frame1,text="",padx=100,pady=100)

    sizex = 0  # use this to change the size
    sizey = 0
    button1 = Button(frame1, text="GENERATION", font=fontstyle2, padx=21 + sizex, pady=20 + sizey, command=generate,
                     background=back, foreground=fore)
    button2 = Button(frame1, text="DECODING  ", font=fontstyle2, padx=21 + sizex, pady=20 + sizey, command=main2,
                     background=back, foreground=fore)
    button3 = Button(frame1, text="  EXIT    ", font=fontstyle2, padx=32 + sizex, pady=20 + sizey,
                     command=lambda: var.set(1), background=back, foreground=fore)
    button4 = Button(frame1, text="  DEVS    ", font=fontstyle2, padx=32 + sizex, pady=20 + sizey, command=DEVS,
                     background=back, foreground=fore)

    button5 = Button(frame1, text="DATABASE  ", font=fontstyle2, padx=32 + sizex, pady=20 + sizey, command=database,
                     background=back, foreground=fore)

    # pic = cv2.imread(".img\\rns1.jpg")
    # pic = cv2.resize(pic, (500, 500), cv2.INTER_AREA)
    # pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    # photo1 = ImageTk.PhotoImage(image=Image.fromarray(pic))
    # logo = Label(frame1, image=photo1)

    frame1.pack(fill=BOTH, expand=True)

    deltax = 400  # use this to change position
    deltay = 60
    button1.place(x=200 + deltax, y=200 + deltay)
    button2.place(x=340 + deltax, y=200 + deltay)
    button4.place(x=200 + deltax, y=295 + deltay)
    button3.place(x=340 + deltax, y=295 + deltay)
    button5.place(x=200 + deltax, y=390 + deltay)
    frame1.wait_variable(var)
    root.quit()
    root.destroy()

    os._exit(1)





def login():
    def logins():
        email = e1.get()
        password = e2.get()

        e2.delete(0, END)

        try:
            global login_complete
            auth.sign_in_with_email_and_password(email, password)
            v.set('Logged In')
            login_complete=1
            login.after(2000)
            login.destroy()

        except:
            v.set('Invalid Email-Id / Password')

    def reset_password():
        email = e1.get()

        try:
            auth.send_password_reset_email(email)
            v.set('Password reset link sent to mail')

        except:
            v.set('Email-Id Not registered')

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




    login=Tk()
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
    v = StringVar()
    p1 = PhotoImage(file='.img\\logo.png')

    l1font = font.Font(family='helvetica', size=11, weight='bold')
    e1font = font.Font(family='courier', size=10, weight='bold')
    l2font = font.Font(family='helvetica', size=11, weight='bold')
    e2font = font.Font(family='courier', size=10, weight='bold')
    l3font = font.Font(family='helvetica', size=11, weight='bold')
    key_font = font.Font(family='courier', size=10, weight='bold')
    l4font = font.Font(family='helvetica', size=12, weight='bold')
    b1font = font.Font(family='helvetica', size=12, weight='bold')
    b2font = font.Font(family='helvetica', size=12, weight='bold')

    p1_l = Label(login, image=p1)
    l1 = Label(login, text='Email-Id', font=l1font)
    e1 = Entry(login, width=35, font=e1font, borderwidth=5, bg='yellow')
    l2 = Label(login, text='Password', font=l2font)
    e2 = Entry(login, show='*', width=35, font=e2font, borderwidth=5, bg='yellow')
    l3 = Label(login, text='Admin-Key', font=l3font)
    key1 = Entry(login, show='*', width=35, font=key_font, borderwidth=5, bg='yellow')
    l4 = Label(login, textvariable=v, font=l4font)
    b1 = Button(login, text="Login", padx=85, pady=25, font=b1font, bg="green", command=logins)
    b2 = Button(login, text="Sign Up", padx=10, pady=10, font=b2font, bg="orange", command=signup)
    b3 = Button(login, text="Reset Password", padx=10, pady=10, font=b2font, bg="red", command=reset_password)

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
    login.mainloop()




login_complete=0
login()


#print("here")
if login_complete==0:
    exit()

root = Tk()
if os.path.isdir("Certificates"):
    pass
else:
    os.mkdir("Certificates")
if os.path.isdir("urls"):
    pass
else:
    os.mkdir("urls")

root.title("CERTIFICATE GENERATOR")
root.geometry("1000x700")

# C = Canvas(root, bg="blue", height=250, width=300)
# filename = PhotoImage(file = ".img\\white2.png")
# background_label = Label(root, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
# C.pack()
root.resizable(False, False)
#root.state('zoomed')
#root.attributes("-fullscreen", True)

fontstyle = font.Font(family="Lucida Grande", size=30, weight="bold", underline=1)
fontstyle2 = font.Font(family="Lucida Grande", size=10, weight="bold", underline=0)
fontstyle3 = font.Font(family="Lucida Grande", size=20, weight="bold", underline=0)
fontstyle4 = font.Font(family="Times", size=30, weight="normal", slant="italic", underline=0)
fontstyle4_2 = font.Font(family="Times", size=15, weight="normal", slant="italic", underline=0)
fontstyle5 = font.Font(family="Lucida Grande", size=20, weight="normal", underline=0)
fontstyle5_2 = font.Font(family="Times", size=40, weight="normal", underline=0)
dbfont = font.Font(family='helvetica', size=11, weight='bold')
frame = Label(root, padx=100, pady=100)
mainframe(frame)
root.mainloop()
