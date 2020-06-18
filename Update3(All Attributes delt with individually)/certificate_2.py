import random
import string
import os
import pyqrcode
import cv2
import sys
from pyqrcode import QRCode
import csv
import time
from tkinter import *
from tkinter import messagebox, Tk
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from PIL import ImageTk, Image
import pandas as pd
from fontz import fontchooser
import time

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

fonts_text = []
fontsscale_text = []
fontscolour_text = []
linetypes_text = []
thickness_text = []



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
    global fonts_text, fontsscale_text, fontscolour_text, linetypes_text, thickness_text,img1,align
    print(i)
    p=0
    for j in pos:
       if j==i:
           break
       p=p+1

    fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i]=fontchooser(fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i],img1,align[p])

def show_sel():
    global align, frames2, serial, font_text, fontscale_text, fontcolour_text, linetype_text
    global scl, frames1,pos
    frames.destroy()
    frames1 = Label(root, padx=100, pady=100)
    l8 = Label(frames1, text="Default certificate")
    a = img1.copy()
    p = 0
    l9 = Label(frames1, text="choose scale of qr code between 1-9", font=fontstyle5)
    clicked = IntVar()
    clicked.set(3)
    drop1 = OptionMenu(frames1, clicked, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    l9.grid(row=0,column=0,columnspan=4)
    drop1.grid(row=0, column=4)
    lattri=Label(frames1,text="Font selection for Each Attribute",font=fontstyle5)
    lattri.grid(row=1,column=0,columnspan=3)
    r=2
    c=0
    b=[]
    global fonts_text,fontsscale_text,fontscolour_text,linetypes_text,thickness_text
    fonts_text = [cv2.FONT_HERSHEY_PLAIN]*(len(names))
    fontsscale_text = [10]*(len(names))
    fontscolour_text = [(0,0,0)]*(len(names))
    linetypes_text = [10]*(len(names))
    thickness_text = [5]*(len(names))

    for i in range(len(names)):
        if names[i]=="serial":
            continue

        b=Button(frames1,text=names[i],padx=60,pady=20)
        b.configure(command=lambda j=b['text']:fonter(names.index(j)))
        b.grid(row=r,column=c)
        c+=1
        if c>2:
            c=0
            r+=1
    frames1.pack()
    var = IntVar()
    var.set(0)

    button4 = Button(frames1, text="submit", font=fontstyle2, padx=100, pady=10, command=lambda: var.set(1)).grid(row=r+2,
                                                                                                                  column=2,columnspan=2)
    back = Button(frames1, text="Back", font=fontstyle2, padx=100, pady=10, command=lambda: mainframe(frames1)).grid(
        row=r+2, column=0,columnspan=2)
    frames1.wait_variable(var)

    for i in pos:
        cv2.putText(a, names[i], align[p], fonts_text[i], fontsscale_text[i], fontscolour_text[i], thickness_text[i],linetypes_text[i])
        p = p + 1
    scl = clicked.get()

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

    a = cv2.resize(a, (600, 600), cv2.INTER_AREA)
    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(image=Image.fromarray(a))
    p1 = Label(frames1, image=photo)
    p1.grid(row=2, column=0)
    root.update()
    ask = messagebox.askyesno("alignment", "are you satisfied with the alignment?")

    if ask == False:
        align.clear()
        pos.clear()
        global sample
        sample = img1.copy()
        frames1.destroy()
        selection()
    elif ask == True:
        frames1.destroy()
        frames2 = Label(root, padx=100, pady=100)
        l10 = Label(frames2, text="selection confirmed generating the certificates", font=fontstyle3, padx=60,
                    pady=60).pack()
        frames2.pack()
        root.update()


def selection():
    try:
        global sel
        global frames
        try:
            frame3.destroy()
        except:
            pass
        frames = Label(root, padx=100, pady=100)
        frames.pack()
        l5 = Label(frames, text="Welcome to the certificate formatting screen", font=fontstyle4, padx=10, pady=10)
        l5.pack()
        sel = 0
        s = ''
        global names, d

        for i in range(len(names)):
            if names[i] == 'serial':
                continue
            sel = sel + 1
            pos.append(i)
            s = s + names[i] + "\r"

        s = "Please choose by double clicking on the certificate the location of\r " + s + "QRCODE\r in the same order"
        l6 = Label(frames, text=s, font=fontstyle4, padx=10, pady=10)
        l6.pack()
        back = Button(frames, text="Back", font=fontstyle2, padx=20, pady=20, command=lambda: mainframe(frames)).pack()
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
    global align, d,pos
    a = img1.copy()
    global fonts_text, fontsscale_text, fontscolour_text, linetypes_text, thickness_text
    if c == 0:
        g = 0
        print(pos)
        for i in pos:
            #print(d[names[i]][csvno], align[g],fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i])
            #print(fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i])
            cv2.putText(a, str(d[names[i]][csvno]), align[g],fonts_text[i], fontsscale_text[i], fontscolour_text[i], linetypes_text[i], thickness_text[i])
            g = g + 1
        print("here")
        b = cv2.imread("urls/" + str(csvno) + ".png")
        x, y, _ = b.shape
        a[align[-1][1]:align[-1][1] + y, align[-1][0]:align[-1][0] + x] = b
        print("here2")
        cv2.imwrite("Certificates/" + d[names[0]][csvno] + ".png", a)
        print("here3")


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

    try:
        r = messagebox.askyesno("steganography", "Do you want to perform steganography?")
        if r == True:
            fram2 = Label(root, padx=800, pady=800)
            fram2.pack()
            l2 = Label(fram2, text="Please Enter the login password", font=fontstyle5).grid(row=0, column=0)
            e = Entry(fram2)
            e.grid(row=0, column=1)
            button3 = Button(fram2, text="  Back    ", font=fontstyle2, padx=32, pady=20,
                             command=lambda: mainframe(fram2)).grid(row=1, column=0)
            v = IntVar()
            v.set(0)
            submit = Button(fram2, text="  SUBMIT  ", padx=30, pady=30, font=fontstyle2, command=lambda: v.set(1)).grid(
                row=1, column=1)
            fram2.wait_variable(v)
            if e.get() != "gaanekano2016":
                messagebox.showerror("password", "password inccorect")
                fram2.destroy()
                main()
            else:
                messagebox.showinfo("password", "password correct")
                fram2.destroy()
                frame10 = Label(root, padx=100, pady=100)
                stega = IntVar()
                stega.set(1)
                frame10.pack()
                l10 = Label(frame10, text="\r\rEnter alpha code", font=fontstyle3, padx=30, pady=30).grid(row=0,
                                                                                                          column=0)
                e = Entry(frame10)
                e.grid(row=0, column=1)
                submit = Button(frame10, text="submit", font=fontstyle2, padx=20, pady=20, command=lambda: stega.set(1))
                submit.grid(row=1, column=1)
                root.update()
                frame10.wait_variable(stega)
                steg = e.get()
                frame10.destroy()
        elif r == False:
            pass

        if steg != '0':
            steganography2(steg)
        else:
            steganography()

        global frame3, d, names, serial
        frame3 = Label(root, padx=100, pady=100)
        var = IntVar()
        var.set(0)
        back = Button(frame3, text="Back", font=fontstyle2, padx=20, pady=20, command=lambda: var.set(1))
        response1 = messagebox.askyesno("csv?", "Do you want to generate certificates through csv file?")
        if (response1 == 1):
            l4 = Label(frame3, text="\r\rPlease choose the location of the csv file", font=fontstyle3, padx=30, pady=30)
            frame3.pack()
            l4.pack()
            back.pack()
            path2 = filedialog.askopenfilename(initialdir=" ", title="select the csv",
                                               filetypes=(("csv files", "*.csv"),))
            d = pd.read_csv(path2)
            d.dropna(1, inplace=True)
            names = list(d.columns)

            try:
                serial = d['serial']
            except:
                response = messagebox.showerror("No serial in csv", "There is no serial in csv")
                exit()

            selection()
            global csvno
            cno = len(serial)
            for i in names:
                total.append(d[i])

            for csvno in range(cno):
                c = 0
                certificategenerator(csvno, c)
            frames2.destroy()
            frames3 = Label(root, padx=100, pady=100)
            frames3.pack()
            l12 = Label(frames3, text="ALL certificates have been generated !!", font=fontstyle, padx=50,
                        pady=50).pack()
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
    frame2 = Label(root, padx=800, pady=800)
    frame2.pack()
    l2 = Label(frame2, text="Please Enter the login password", font=fontstyle5).grid(row=0, column=0)
    e = Entry(frame2)
    e.grid(row=0, column=1)
    button3 = Button(frame2, text="  Back    ", font=fontstyle2, padx=32, pady=20,
                     command=lambda: mainframe(frame2)).grid(row=1, column=0)
    v = IntVar()
    v.set(0)
    submit = Button(frame2, text="  SUBMIT  ", padx=30, pady=30, font=fontstyle2, command=lambda: v.set(1)).grid(row=1,
                                                                                                                 column=1)
    frame2.wait_variable(v)
    if e.get() != "gaanekano2016":
        messagebox.showerror("password", "password inccorect")
        frame2.destroy()
        main2()
    else:
        messagebox.showinfo("password", "password correct")
        frame2.destroy()
        frame3 = Label(root, padx=800, pady=800)
        frame3.pack()
        l3 = Label(frame3, text="\r\rcongradulations you have logged on", font=fontstyle5).grid(row=0, column=0)
        mark = cv2.imread(".img\\mark.jpg")
        mark = cv2.resize(mark, (500, 400), cv2.INTER_AREA)
        mark = cv2.cvtColor(mark, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(mark))
        p1 = Label(frame3, image=photo)
        p1.grid(row=1, column=0)
        button3 = Button(frame3, text="  Back    ", font=fontstyle2, padx=32, pady=20,
                         command=lambda: mainframe(frame3)).grid(row=2, column=0)
        path1 = filedialog.askopenfilename(initialdir=" ", title="select the originalcertificate",
                                           filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
        path2 = filedialog.askopenfilename(initialdir=" ", title="select the certificate to be decoded",
                                           filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
        img3 = (img1 - img2) * (255, 255, 255)
        cv2.imwrite("decoded.png", img3)
        l4 = Label(frame3, text="DECODING COMPLETE!!", font=fontstyle5)
        l4.grid(row=3, column=0)
        root.update()
        root.after(2000)
        mainframe(frame3)


def generate():
    try:
        global img1, frame2
        frame1.destroy()
        frame2 = Label(root, padx=100, pady=100)
        l2 = Label(frame2, text="\r\rPlease choose the path of the certificate", font=fontstyle3, padx=20, pady=20)
        l2.pack()
        var = IntVar()
        var.set(0)
        back = Button(frame2, text="Back", font=fontstyle2, padx=20, pady=20, command=lambda: var.set(1)).pack()
        frame2.pack()
        path1 = filedialog.askopenfilename(initialdir=" ", title="select the certificate",
                                           filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))

        img1 = cv2.imread(path1)
        main()
        mainframe(frame)
    except:
        frame2.wait_variable(var)
        mainframe(frame2)


def DEVS():
    frame1.destroy()
    frame2 = Label(root, padx=800, pady=800)
    frame2.pack()
    fontstyle = font.Font(family="Lucida Grande", weight="normal", slant="italic", underline=1, size=20)
    var = IntVar()
    var.set(0)
    dev = Label(frame2, text="LEGENDS 2k16", font=fontstyle).pack()
    fontstyle = font.Font(family="Lucida Grande", weight="normal", slant="italic", underline=0, size=20)
    dev2 = Label(frame2,
                 text="V KESHAV BHARADWAJ\rVIVEK ADI\rCHIRANJIT PATEL\rVIVEK URANKAR\rSHANKAR ANBALAGAN\rSOURAV P ADI",
                 font=fontstyle).pack()
    pic = cv2.imread(".img\\crazy.jpg")
    pic = cv2.resize(pic, (400, 400), cv2.INTER_AREA)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    photo1 = ImageTk.PhotoImage(image=Image.fromarray(pic))
    logo = Label(frame2, image=photo1).pack()
    button3 = Button(frame2, text="  back    ", padx=32, pady=20, font=fontstyle2,
                     command=lambda: mainframe(frame2)).pack()
    frame2.wait_variable(var)


# root.iconbitmap('@high.xbm')
def mainframe(x):
    global frame1
    x.destroy()
    certino = 0
    qrno = 0
    l = []
    names = []
    csvno = 0
    sel = 0
    pos = []
    align = []
    total = []
    fonts_text = []
    fontsscale_text = []
    fontscolour_text = []
    linetypes_text = []
    thickness_text = []
    var = IntVar()
    var.set(0)
    frame1 = Label(root, padx=800, pady=800)
    l1 = Label(frame1, text="WELCOME TO CERTIFICATE GENERATOR", padx=10, pady=10, font=fontstyle, fg="BLUE")

    button1 = Button(frame1, text="GENERATION", font=fontstyle2, padx=20, pady=20, command=generate)
    button2 = Button(frame1, text="DECODING  ", font=fontstyle2, padx=22, pady=20, command=main2)
    button3 = Button(frame1, text="  EXIT    ", font=fontstyle2, padx=32, pady=20, command=lambda: var.set(1))
    button4 = Button(frame1, text="  DEVS    ", font=fontstyle2, padx=32, pady=20, command=DEVS)
    pic = cv2.imread(".img\\rns1.jpg")
    pic = cv2.resize(pic, (500, 500), cv2.INTER_AREA)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    photo1 = ImageTk.PhotoImage(image=Image.fromarray(pic))
    logo = Label(frame1, image=photo1)
    frame1.pack()
    logo.grid(row=1, column=0, columnspan=4)
    l1.grid(row=0, column=0, columnspan=4)
    button1.grid(row=3, column=1)
    button2.grid(row=3, column=2)
    button4.grid(row=4, column=1)
    button3.grid(row=4, column=2)
    frame1.wait_variable(var)
    root.destroy()
    exit(0)


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
root.geometry("1000x800")
#root.attributes("-fullscreen", True)

fontstyle = font.Font(family="Lucida Grande", size=30, weight="bold", underline=1)
fontstyle2 = font.Font(family="Lucida Grande", size=10, weight="bold", underline=0)
fontstyle3 = font.Font(family="Lucida Grande", size=20, weight="bold", underline=0)
fontstyle4 = font.Font(family="Lucida Grande", size=20, weight="normal", slant="italic", underline=0)
fontstyle5 = font.Font(family="Lucida Grande", size=20, weight="normal", underline=0)
frame = Label(root, padx=100, pady=100)
mainframe(frame)
root.mainloop()


