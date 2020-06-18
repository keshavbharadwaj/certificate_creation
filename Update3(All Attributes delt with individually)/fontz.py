from tkinter import *
from tkinter import font
from tkinter import colorchooser
from tkinter import messagebox,Tk
from PIL import ImageTk,Image
import numpy as np
import cv2

colour=(0,0,0)
def color_picker():
    global colour
    colour= colorchooser.askcolor()[0]
    colour=colour[-1::-1]
def fontchooser(fontype,fontsscale_text,fontscolour_text,linetypes_text,thickness_text,img1,align):
    x,y,_=img1.shape
    #print(fontype,fontsscale_text,fontscolour_text,linetypes_text,thickness_text)
    global colour
    colour=fontscolour_text[-1::-1]
    toplevel = Toplevel()
    fontstyle=font.Font(family="Lucida Grande",size=10,weight="normal",underline=0,overstrike=0)
    toplevel.title("FONT SELECTOR")
    l=Label(toplevel,text="Select the required font attributes",font=fontstyle)
    toplevel.geometry("800x800")
    frame1=LabelFrame(toplevel,padx=20,pady=20)
    frame2=LabelFrame(toplevel,padx=20,pady=20)
    frame3=LabelFrame(toplevel,padx=20,pady=20)
    frame4=LabelFrame(toplevel,padx=20,pady=20)

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
    font_family.set(family[0])
    drop=OptionMenu(frame1,font_family,*family)
    l1=Label(frame1,text="Select the font type")
    lcol=Label(frame1,text="Select the colour of font")
    bcolour=Button(frame1,text="colour Chooser",font=fontstyle,padx=5,pady=5,command=lambda:color_picker())

    l2=Label(frame2,text="Select the font scale")
    scales=StringVar()
    thickness=IntVar()
    linetype=IntVar()
    linetype.set(linetypes_text)
    thickness.set(int(thickness_text))
    scales.set(fontsscale_text)
    e=Entry(frame2,text=scales)
    e2=Entry(frame2,text=thickness)
    l3=Label(frame2,text="Select the Thickness")
    l4=Label(frame2,text="Select the linetype")
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
    button2=Button(toplevel,text="Done",command=lambda:submits.set(1)).grid(row=3,column=1)
    button=Button(toplevel,text="Set",command=lambda:sets.set(1)).grid(row=2,column=1)
    while(1):
        pmag=img1.copy()
        if submits.get()==1:
            toplevel.destroy()
            return fontype,fontsscale_text,colour,linetypes_text,thickness_text
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
        a2 = cv2.resize(pmag, (600, 600), cv2.INTER_AREA)
        a2 = cv2.cvtColor(a2, cv2.COLOR_BGR2RGB)
        ph = ImageTk.PhotoImage(image=Image.fromarray(a2))
        pdesc = Label(toplevel, image=ph)
        pdesc.grid(row=4, column=0,rowspan=2,columnspan=5)
        toplevel.wait_variable(sets)
    toplevel.mainloop()
# def fontchooser2():
#     fontype=cv2.FONT_HERSHEY_COMPLEX_SMALL
#     fontsscale_text=2
#     fontscolour_text=(0,0,0)
#     linetypes_text=1
#     thickness_text=2
#     fontchooser(fontype,fontsscale_text,fontscolour_text,linetypes_text,thickness_text)
#
# root=Tk()
# l=Label(root,text="hello")
# b=Button(root,text="buts",command=lambda:fontchooser2())
# l.pack()
# b.pack()
# root.mainloop()