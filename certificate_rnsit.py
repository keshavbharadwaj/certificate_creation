import random
import string
import os
import pyqrcode
import cv2
from pyqrcode import QRCode
import csv
import time
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import time

certino=0
qrno=0
l=[]
dates=[]
department=[]
category=[]
sems=[]
titles=[]
name1=[]
name2=[]
name3=[]
name4=[]
usn1=[]
usn2=[]
usn3=[]
usn4=[]
serial=[]
csvno=0
sel=0
pos=[]
align=[]
total=[]
#img2=cv2.imread("x.jpg")
#sample=img2.copy()


def draw_circle(event,x,y,flags,param):
    global sel
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(sample,(x,y),10,(255,0,0),-1)
        mouseX,mouseY=x,y
        #print (mouseX,mouseY)
        align.append((mouseX,mouseY))
        sel=sel-1
        return(mouseX,mouseY)
def selectiononcertificate():
    global sel,sample
    sel=sel+1
    sample=img1.copy()
    root.update()
    cv2.namedWindow('sample',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('sample',draw_circle)
    while(1):
        cv2.imshow('sample',sample)
        k =cv2.waitKey(20) & 0xFF
        #print(mouseX,mouseY)
        if sel==0:
            cv2.destroyAllWindows()
            a=messagebox.showinfo("slection done","You have completed the selection process")
            if a=="ok":
                break
            
    show_sel()
    
   
def show_sel():
    global align,frames2
    global scl,frames1
    frames.destroy()
    frames1=Label(root,padx=100,pady=100)
    l8=Label(frames1,text="Default certificate")
    a=img1.copy()
    font=cv2.FONT_HERSHEY_COMPLEX
    fontscale=2
    fontcolour=(0,0,0)
    linetype=2
    p=0
    s1="date"
    s2="department"
    s3="category"
    s4="sems"
    s5="title"
    s6="name1"
    s7="name2"
    s8="name3"
    s9="name4"
    s10="usn1"
    s11="usn2"
    s12="usn3"
    s13="usn4"
    s=[s1,s2,s3,s4,s5,s10,s6,s11,s7,s12,s8,s13,s9]
    #print(pos)
    for i in pos:              
         cv2.putText(a,s[i],align[p],font,fontscale,fontcolour,linetype)
         p=p+1
    l9=Label(frames1,text="choose scale of qr code between 1-9",font=fontstyle5)
    clicked=IntVar()
    clicked.set(3)
    drop1=OptionMenu(frames1,clicked,1,2,3,4,5,6,7,8,9)
    l9.grid(row=0,column=0)
    drop1.grid(row=0,column=1)
    frames1.pack()
    var=IntVar()
    var.set(0)
    button4=Button(frames1,text="submit",font=fontstyle2,padx=100,pady=10,command=lambda:var.set(1)).grid(row=1,column=1)
    frames1.wait_variable(var)
    scl=clicked.get()
    #print(scl)
    url=pyqrcode.create(serial[0])
    url.png("/home/keshav/qrcodes/sample.png", scale = scl)
    
    b=cv2.imread("/home/keshav/qrcodes/sample.png")
    x,y,_=b.shape
    try:
        a[align[-1][1]:align[-1][1]+y,align[-1][0]:align[-1][0]+x]=b
    except:
        k=messagebox.showerror("Error","QR Code is overflowing out of the image Please choose the scale again")
        if(k=="ok"):
            frames1.destroy()
            show_sel()
            return
    a=cv2.resize(a,(600,600),cv2.INTER_AREA)
    a=cv2.cvtColor(a,cv2.COLOR_BGR2RGB)
    photo=ImageTk.PhotoImage(image=Image.fromarray(a))
    p1=Label(frames1,image=photo)
    p1.grid(row=2,column=0)
    root.update()
    ask=messagebox.askyesno("alignment","are you satisfied with the alignment?")
    #print(ask)
    if ask==False:
       align.clear()
       pos.clear()
       global sample
       sample=img1.copy()
       frames1.destroy()
       selection()
    elif ask==True:
        frames1.destroy()
        frames2=Label(root,padx=100,pady =100)
        l10=Label(frames2,text="selection confirmed generating the certificates",font=fontstyle3,padx=60,pady=60).pack()
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
        frames=Label(root,padx=100,pady=100)
        frames.pack()
        l5=Label(frames,text="Welcome to the certificate formating screen",padx=10,pady=10)
        l5.pack()
        sel=0
        s=''
        if dates[0]!='':
            sel=sel+1
            pos.append(0)
            s= s+"dates\r"
        if department[0]!='':
            sel=sel+1
            pos.append(1)
            s=s+"department\r"
        if category[0]!='':
            sel=sel+1
            pos.append(2)
            s=s+"category\r"
        if sems[0]!='':
            sel=sel+1
            pos.append(3)
            s=s+"sems\r"
        if titles[0]!='':
            sel=sel+1
            pos.append(4)
            s=s+"title\r"
        if usn1[0]!='':
            sel=sel+1
            pos.append(5)
            s=s+"us1\r"
        if name1[0]!=0:
            sel=sel+1
            pos.append(6)
            s=s+"name1\r"
        if usn2[0]!='':
            sel=sel+1
            pos.append(7)
            s=s+"usn2\r"
        if name2[0]!='':
            sel=sel+1
            pos.append(8)
            s=s+"name2\r"
        if usn3[0]!='':
            sel=sel+1
            pos.append(9)
            s=s+"usn3\r"
        if name3[0]!='':
            sel=sel+1
            pos.append(10)
            s=s+"name3\r"
        if usn4[0]!='':
            sel=sel+1
            pos.append(11)
            s=s+"usn4\r"
        if name4[0]!='':
            sel=sel+1
            pos.append(12)
            s=s+"name4\r"
        s="Please choose by double clicking on the certificate the location of\r "+s+"QRCODE\r in the same order"
        l6=Label(frames,text=s,font=fontstyle4,padx=10,pady=10)
        l6.pack()
        selectiononcertificate()
    except:
        root.destroy()
        

def segmentation(img,initialx,initialy,s):
    x=initialx
    y=initialy
    font=cv2.FONT_HERSHEY_PLAIN
    fontscale=0.5
    linetype=1
    thickness=1
    for m in s:
        fontcolour=img[x,y]
        b=int(fontcolour[0])
        g=int(fontcolour[1])
        r=int(fontcolour[2])
        r=ragecalc(r)
        g=ragecalc(g)
        b=ragecalc(b)
        
        cv2.putText(img,m,(y,x),font,fontscale,(b,g,r),thickness,linetype)
        y=y+6
    x=x+10
    return(x,y)       

def ragecalc(r):
    if r > 0:
        return (r-1)
    else:
        return(r+1)
def qrmadu(no): 
    s = serial[no]
    url = pyqrcode.create(s)  
    url.png("urls/"+str(no)+".png", scale = scl)
    
def certificate(csvno,c):
    a=img1.copy()
    font=cv2.FONT_HERSHEY_DUPLEX
    fontscale=2
    fontcolour=(0,0,0)
    linetype=2	
    if c==0:
        g=0
        #print(total)
        #print(pos)
        #print(csvno)
        for i in pos:
            cv2.putText(a,total[i][csvno],align[g],font,fontscale,fontcolour,linetype)
            g=g+1
        qrmadu(csvno)
        b=cv2.imread("urls/"+str(csvno)+".png")
        x,y,_=b.shape
        a[align[-1][1]:align[-1][1]+y,align[-1][0]:align[-1][0]+x]=b
        cv2.imwrite("Certificates/"+str(csvno)+".png",a)


def steganography():
    x=50
    y=50
    x,y=segmentation(img1,x,y,"2K16")
    x,y=segmentation(img1,x,y,"KB")
    x,y=segmentation(img1,x,y,"VA")
    x,y=segmentation(img1,x,y,"CJ")
    x,y=segmentation(img1,x,y,"VU")
    x,y=segmentation(img1,x,y,"SA")
    x,y=segmentation(img1,x,y,"SH")
    x,y=segmentation(img1,x,y,"SP")
    #cv2.imwrite("1.png",img1)
    
	

def certificategenerator(csvno,c):
    qrmadu(csvno)
    certificate(csvno,c)
def log():
    total=[]
    file = open("log.txt","a")
    for i in range(len(l)):
        total.append(l[i]+'-'+names[i])
    b='\n'.join(total)
    file.write(b)

def main():
    try:
        steganography()
        frame2.destroy()
        global frame3
        frame3=Label(root,padx=100,pady=100)

        response1=messagebox.askyesno("csv?","Do you want to generate certificates through csv file?")    
        if(response1==1):
            l4=Label(frame3,text="\r\rPlease shoose the location of the csv file",font=fontstyle3,padx=30,pady=30)
            frame3.pack()
            l4.pack()
            path2=filedialog.askopenfilename(initialdir=" ",title="select the csv",filetypes=(("csv files","*.csv"),))
        
            with open(path2,newline = '') as file:
                read=csv.reader(file)
                for row in read:
                    dates.append(row[0])
                    department.append(row[1])
                    category.append(row[2])
                    sems.append(row[3])
                    titles.append(row[4])
                    name1.append(row[6])
                    usn1.append(row[5])
                    name2.append(row[8])
                    usn2.append(row[7])
                    name3.append(row[10])
                    usn3.append(row[9])
                    name4.append(row[12])
                    usn4.append(row[11])
                    serial.append(row[13])
         
            selection()    
            global csvno
            cno=len(serial)
            total.append(dates)
            total.append(department)
            total.append(category)
            total.append(sems)
            total.append(titles)
            total.append(usn1)
            total.append(name1)
            total.append(usn2)
            total.append(name2)
            total.append(usn3)
            total.append(name3)
            total.append(usn4)
            total.append(name4)
        #print(total[5])
       
            for csvno in range(cno):
                c=0
                certificategenerator(csvno,c)
            frames2.destroy()
            l12=Label(root,text="ALL certificates have been generated !!",font=fontstyle,padx=50,pady=50).pack()       
            root.after(2000,root.destroy)
            
                
        elif(response1 == 0):
           g=messagebox.showinfo("csv","Please create the csv file with the necessary requirment first,for more information refer to the read me file")
           if g=="ok":
               root.destroy()
           
    except:
        root.destroy()#log()
    

def main2():
    frame1.destroy()
    frame2=Label(root,padx=800,pady=800)
    frame2.pack()
    l2=Label(frame2,text="Please Enter the login password",font=fontstyle5).grid(row=0,column=0)
    e=Entry(frame2)
    e.grid(row=0,column=1)
    button3=Button(frame2,text="  EXIT    ",font=fontstyle2,padx=32,pady=20,command=root.destroy).grid(row=1,column=0)
    v=IntVar()
    v.set(0)
    submit=Button(frame2,text="  SUBMIT  ",padx=30,pady=30,font=fontstyle2,command=lambda:v.set(1)).grid(row=1,column=1)
    frame2.wait_variable(v)
    if e.get()!="gaanekano2016":
        messagebox.showerror("password","password inccorect")
        frame2.destroy()
        main2()
    else:
        messagebox.showinfo("password","password correct")
        frame2.destroy()
        frame3=Label(root,padx=800,pady=800)
        frame3.pack()
        l3=Label(frame3,text="\r\rcongradulations you have logged on",font=fontstyle5).grid(row=0,column=0)
        mark=cv2.imread("mark.jpg")
        mark=cv2.resize(mark,(400,400),cv2.INTER_AREA)
        mark=cv2.cvtColor(mark,cv2.COLOR_BGR2RGB)
        photo=ImageTk.PhotoImage(image=Image.fromarray(mark))
        p1=Label(frame3,image=photo)
        p1.grid(row=1,column=0)
        path1=filedialog.askopenfilename(initialdir=" ",title="select the originalcertificate",filetypes=(("png files","*.png"),("jpg files","*.jpg")))
        path2=filedialog.askopenfilename(initialdir=" ",title="select the certificate to be decoded",filetypes=(("png files","*.png"),("jpg files","*.jpg")))
        img1=cv2.imread(path1)
        img2=cv2.imread(path2)
        img3=(img1-img2)*(255,255,255)
        cv2.imwrite("decoded.png",img3)
        l4=Label(frame3,text="DECODING COMPLETE!!",font=fontstyle5)
        l4.grid(row=3,column=0)
        root.after(2000,root.destroy)

def generate():
    try:
        global img1,frame2
        frame1.destroy()
        frame2 = Label(root,padx=100,pady=100)
        l2=Label(frame2,text="\r\rPlease choose the path of the certificate",font=fontstyle3,padx=20,pady=20)
        l2.pack()
        frame2.pack()
        path1=filedialog.askopenfilename(initialdir=" ",title="select the certificate",filetypes=(("png files","*.png"),("jpg files","*.jpg")))
    #print(path1)
        img1=cv2.imread(path1)
        main()
    except:
        root.destroy()
def DEVS():
    frame1.destroy()
    frame2=Label(root,padx=800,pady=800)
    frame2.pack()
    fontstyle=font.Font(family="Lucida Grande",weight="normal",slant="italic",underline=1,size=20)
    var=IntVar()
    var.set(0)
    dev=Label(frame2,text="LEGENDS 2k16",font=fontstyle).pack()
    fontstyle=font.Font(family="Lucida Grande",weight="normal",slant="italic",underline=0,size=20)
    dev2=Label(frame2,text="V KESHAV BHARADWAJ\rVIVEK ADI\rCHIRANJIT PATEL\rVIVEK URANKAR\rSHANKAR ANBALAGAN\rSAURAV P ADI",font=fontstyle).pack()
    pic=cv2.imread("crazy.jpg")
    pic=cv2.resize(pic,(400,400),cv2.INTER_AREA)
    pic=cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
    photo1=ImageTk.PhotoImage(image=Image.fromarray(pic))
    logo=Label(frame2,image=photo1).pack()
    button3=Button(frame2,text="  EXIT    ",padx=32,pady=20,font=fontstyle2,command=lambda : var.set(1)).pack()
    frame2.wait_variable(var)
    root.destroy()
    
    
                                                  
root = Tk()

if os.path.isdir("Certificates"):
    pass
else:
    os.mkdir("Certificates")
if  os.path.isdir("urls"):
    pass
else:
    os.mkdir("urls")
#top=Toplevel()
root.title("CERTIFICATE GENERATOR")
root.attributes("-fullscreen",True)

sc1=ImageTk.PhotoImage(Image.open("crazy.jpg"))
#root.iconbitmap('@high.xbm')

frame1 = Label(root,padx=800,pady=800)
fontstyle=font.Font(family="Lucida Grande",size=30,weight="bold",underline=1)
fontstyle2=font.Font(family="Lucida Grande",size=10,weight="bold",underline=0)
fontstyle3=font.Font(family="Lucida Grande",size=20,weight="bold",underline=0)
fontstyle4=font.Font(family="Lucida Grande",size=20,weight="normal",slant="italic",underline=0)
fontstyle5=font.Font(family="Lucida Grande",size=20,weight="normal",underline=0)
l1=Label(frame1,text="WELCOME TO CERTIFICATE GENERATOR",padx=10,pady=10,font=fontstyle,fg="BLUE")
#l2=Label(image=sc1)
button1=Button(frame1,text="GENERATION",font=fontstyle2,padx=20,pady=20,command=generate)
button2=Button(frame1,text="DECODING  ",font=fontstyle2,padx=22,pady=20,command=main2)
button3=Button(frame1,text="  EXIT    ",font=fontstyle2,padx=32,pady=20,command=root.destroy)
button4=Button(frame1,text="  DEVS    ",font=fontstyle2,padx=32,pady=20,command=DEVS)
pic=cv2.imread("rns1.jpg")
pic=cv2.resize(pic,(500,500),cv2.INTER_AREA)
pic=cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
photo1=ImageTk.PhotoImage(image=Image.fromarray(pic))
logo=Label(frame1,image=photo1)
frame1.pack()
logo.grid(row=1,column=0,columnspan=4)
l1.grid(row=0,column=0,columnspan=4)
#l2.pack()
button1.grid(row=3,column=1)
button2.grid(row=3,column=2)
button4.grid(row=4,column=1)
button3.grid(row=4,column=2)

root.mainloop()

