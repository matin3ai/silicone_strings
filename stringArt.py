import os
import time
import math
import cv2 as cv
import numpy as np
import tkinter as tk
from PIL import ImageTk,Image
from tkinter import StringVar, filedialog as fd


"""tkinter windows"""
winStr = tk.Tk()
winStr.title("StringArt Machine")
winStr.geometry("1000x550")
winStr.config(background="#111111")


"""Upload Button Function"""
filetypes = (('Png files', '*.png'),('All files', '*.*'))
def uploadbtn():
    global filename
    filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
    return filename


"""row colume weight"""
winStr.columnconfigure(2,weight=1)
winStr.rowconfigure(0,weight=1)
winStr.rowconfigure(1,weight=1)
winStr.rowconfigure(2,weight=1)
winStr.rowconfigure(3,weight=1)
winStr.rowconfigure(4,weight=1)
winStr.rowconfigure(5,weight=1)


"""Pin number Entry and Label"""
txtPin = tk.Label(winStr,text="Number of Pins")
txtPin.config(bg="#111111",fg="#f1f1f1",font=("Verdana", 14),padx=20,pady=20)
txtPin.grid(row=0,column=0,rowspan=1,columnspan=1,sticky=tk.W) 
entPin = tk.Entry(winStr)
entPin.config(bg="#393E46",fg="#66fcf1",font=("Verdana", 14),width=8,
              highlightbackground='#cccccc',bd=3)
entPin.grid(row=0,column=1,rowspan=1,columnspan=1,ipady = 2,ipadx=2)
entPin.insert(0,"324")


"""Line number Entry and Label"""
txtLine = tk.Label(winStr,text="Number of Lines")
txtLine.config(bg="#111111",fg="#f1f1f1",font=("Verdana", 14),
               padx=20,pady=20)
txtLine.grid(row=1,column=0,rowspan=1,columnspan=1,sticky=tk.W) 
entLine = tk.Entry(winStr)
entLine.config(bg="#393E46",fg="#66fcf1",font=("Verdana", 14),width=8,
               highlightbackground='#cccccc',bd=3)
entLine.grid(row=1,column=1,rowspan=1,columnspan=1,ipady = 2,ipadx=2)
entLine.insert(0,"4000")


"""Weight number Entry and Label"""
txtWeight = tk.Label(winStr,text="Line Weight")
txtWeight.config(bg="#111111",fg="#f1f1f1",font=("Verdana", 14),
    padx=20,pady=20)
txtWeight.grid(row=2,column=0,rowspan=1,columnspan=1,sticky=tk.W) 
entWeight = tk.Entry(winStr)
entWeight.config(bg="#393E46",fg="#66fcf1",font=("Verdana", 14),width=8,
                 highlightbackground='#cccccc',bd=3)
entWeight.grid(row=2,column=1,rowspan=1,columnspan=1,ipady = 2,ipadx=2)
entWeight.insert(0,"35")


"""Eye Machine Entry and Label"""
txtEye = tk.Label(winStr,text="Light Calibration")
txtEye.config(bg="#111111",fg="#f1f1f1",font=("Verdana", 14),
    padx=20,pady=20)
txtEye.grid(row=3,rowspan=1,column=0,columnspan=1,sticky=tk.W) 
entEye = tk.Entry(winStr)
entEye.config(bg="#393E46",fg="#66fcf1",font=("Verdana", 14),width=8,
              highlightbackground='#cccccc',bd=3)
entEye.grid(row=3,column=1,rowspan=1,columnspan=1,ipady = 2,ipadx=2)
entEye.insert(0,"0")


"""Pixel W Entry and Label"""
txtPixel = tk.Label(winStr,text="Line Thickness")
txtPixel.config(bg="#111111",fg="#f1f1f1",font=("Verdana", 14),
    padx=20,pady=20)
txtPixel.grid(row=4,rowspan=1,column=0,columnspan=1,sticky=tk.W) 
entPixel = tk.Entry(winStr)
entPixel.config(bg="#393E46",fg="#66fcf1",font=("Verdana", 14),width=8,
                highlightbackground='#cccccc',bd=3)
entPixel.grid(row=4,column=1,rowspan=1,columnspan=1,ipady = 2,ipadx=2)
entPixel.insert(0,"7")


"""photo Inter"""
"""Opencv pic"""
fileresized = 'Fsize.png'
dim = (500,500)
pathimage = uploadbtn()
img = cv.imread(pathimage,cv.IMREAD_UNCHANGED)
resixed = cv.resize(img,dim,interpolation = cv.INTER_AREA)
cv.imwrite(fileresized,resixed)
icon = tk.PhotoImage(master=winStr, file=fileresized)
imgShow = tk.Label(winStr,image=icon)
imgShow.grid(row=0,column=2,rowspan=6,padx=20,pady=30)



"""Qain-Programm"""
"""Point-GENERATION"""
def pointGenerate(center, circRadius, n=360):  # used in coords
    if n < 36:
        n = 360
    coords = []
    for point in range(n):  # defult 360
        angle = (2*math.pi * point) / n
        x = math.floor(center.x + circRadius * math.cos(angle))
        y = math.floor(center.y + circRadius * math.sin(angle))
        coords.append(Qoint(x, y, point))
    print(f"LOG ----->> generation {n} point in Circle  DONE <!>",)
    return coords


class Qoint:
    def __init__(self, x, y, p=-1):
        self.x, self.y, self.p = x, y, p

    def distance(self, pois):
        return math.sqrt((pois.x - self.x) ** 2 + (pois.y - self.y)**2)

    def __str__(self):

        return f"{self.p}"


def imgSAW(path):
    img = cv.imread(path, 0)
    return img


def imgSquare(img):
    print("LOG ----->> Squaring the image ... <!>", end="\r")
    height, width = img.shape[0], img.shape[1]
    length = min(height, width)
    center = Qoint(img.shape[0] / 2, img.shape[1] / 2)
    radius = length / 2 - 1 / 2
    print("LOG ----->> Squaring the image DONE  <!>")
    return center, radius, width, height, length


def imgShow(img):
    cv.imshow("IMAGE", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def imgCircle(width, height, radius, length, center, img):
    print("LOG ----->> Extract circle image ...  <!>", end="\r")
    for y in range(height):
        for x in range(width):
            if Qoint(x, y).distance(center) > radius:
                img[x, y] = 0xFF
    print("LOG ----->> Extract circle image DONE  <!>")


def drawLine(img, origin, end):
    global LINE_PIXEL
    LINE_PIXEL = int(entPixel.get())
    cv.line(img, (origin.x * 25, origin.y * 25),
            (end.x * 25, end.y * 25), color=(0, 0, 0), thickness=LINE_PIXEL, lineType=16)


def shrink_image(img, target_height, target_width):
    cv.resize(img, (target_width, target_height))


def getData(dict, pt, pt2):
    a, b = pt, pt2
    if pt.p > pt2.p:
        a, b = b, a

    if a not in dict:
        distance = int(a.distance(b))
        xs = np.linspace(a.x, b.x, distance, dtype=int)
        ys = np.linspace(a.y, b.y, distance, dtype=int)
        weight = 1
        dict[a] = {b: (xs, ys, distance, weight)}
    elif b not in dict[a]:
        distance = int(a.distance(b))
        xs = np.linspace(a.x, b.x, distance, dtype=int)
        ys = np.linspace(a.y, b.y, distance, dtype=int)
        weight = 1
        dict[a][b] = (xs, ys, distance, weight)
    return dict[a][b]


def main():
    entMachin = entEye.get()
    if entMachin == 0:
        IMG = pathimage
    elif entMachin == 1:
        IMG = './machinEdit1.png'
    elif entMachin == 2:
        IMG = './machinEdit2.png'
    elif entMachin == 3:
        IMG = './machinEdit3.png'
    elif entMachin == 4:
        IMG = './machinEdit4.png'
    else: 
        IMG = pathimage
    #IMG = fileresized
    
    
    DECOMPOSITION = False
    NUMBER_LINES = int(entLine.get())
    NUMBER_POINTS = int(entPin.get())
    WEIGHT = int(entWeight.get())
    
    
    tic = time.time()
    number_points = NUMBER_POINTS
    number_lines = NUMBER_LINES
    image = imgSAW(IMG)
    center, radius, width, height, length = imgSquare(image)
    imgCircle(width, height, radius, length, center, image)


    coords = pointGenerate(center, radius, number_points)
    lines = {}
    error = np.ones(image.shape) * 0xFF - image.copy()
    result = np.ones(
        (image.shape[0] * 25, image.shape[1] * 25), np.uint8) * 0xFF
    mask = np.zeros(image.shape, np.float64)

    order_points = [coords[0]]
    last = coords[0]

    for l in range(number_lines):
        print(f"Drawing {number_lines} lines...{l}/{number_lines}", end="\r")
        
        ressemblance = -math.inf
        best_choice = last
        for candidat in coords:
            xs, ys, dist, weight = getData(lines, last, candidat)
            line_ressemblance = np.sum(error[ys, xs]) * weight

            if line_ressemblance > ressemblance:
                ressemblance = line_ressemblance
                best_choice = candidat

        order_points.append(best_choice)
        xs, ys, dist, weight = getData(lines, best_choice, last)
        weight *= WEIGHT
        if dist == 0:
            break

        mask.fill(0)
        mask[ys, xs] = weight
        error -= mask
        error.clip(0, 255)

        drawLine(result, last, best_choice)
        last = best_choice
        if DECOMPOSITION:

            name = str(l) + ".png"
            cv.imwrite(name, result)

    print(f"LOG ----->> Drawing {number_lines} point in Circle  DONE <!>")
    print(f"LOG ----->> Create awsome pic ... ")

    name = os.path.splitext(IMG)[0] + "-Qstring.png"
    #nameMedium = os.path.splitext(IMG)[0] + "-Qstring(Medium).png"
    nameSmall = os.path.splitext(IMG)[0] + "-Qstring(Small).png"
    

    Swidth, Sheight = 5030, 5030  # Small Pic Size
    #Mwidth, Mheight = 6000, 6000  # Medium Pic Size
    #mediumPic = cv.resize(result, (Mwidth, Mheight))
    smallPic = cv.resize(result, (Swidth, Sheight))
    cv.imwrite(name, result)
    #cv.imwrite(nameMedium, mediumPic)
    cv.imwrite(nameSmall, smallPic)
    timer = time.time() - tic
    print(f"Program ended successfully in {timer} seconds")

    def fileHandy(order_points, name, timer):
        listPin = []
        for i in order_points:
            xstrt = str(i)
            listPin.append(int(xstrt.strip(' ')))
        nameFile = f"{name}-pinLocate.txt"
        detailFile = f"{name}-DesignDetails"
        pinLocate = open(nameFile, "w")
        designDetails = open(detailFile, "w")
        
        manyLine = len(listPin)
        timers = round(timer)
        
        pinLocate.write(f"{listPin},")
        header = f""" 
           {name} DesignDetails
           Number of Pins : {NUMBER_POINTS}
           Number of Lines :  {NUMBER_LINES}
           Number of Lines Draw : {manyLine}
           Line Weight : {WEIGHT}
           Light Calibration : {entMachin}
           Line Thickness : {LINE_PIXEL}
           Program ended successfully in {timers} seconds
            
            pins :>
            
            {listPin}
           
        """
        

        designDetails.write(header)
        pinLocate.write(f"{listPin}")
        pinLocate.close()
        #for i in listPin:
            #pinLocate.write(f"{i},")
            #print(len(listPin))
        #pinLocate.close()
        print(listPin, len(listPin))
    
    fileHandy(order_points, name, timer)


"""FILTER SECTIONS"""
path =pathimage  # image path
pathBright = "./st-pic.png"
bright = 170
contre = 115
imgCat = cv.imread(path, 1)  # read img Flag 1
lab = cv.cvtColor(imgCat, cv.COLOR_BGR2LAB)  # convert image to L A B
l, a, b = cv.split(lab)  # split it
clah1 = cv.createCLAHE(clipLimit=2.0, tileGridSize=(2, 3))
clah2 = cv.createCLAHE(clipLimit=2.0, tileGridSize=(2, 6))
clah3 = cv.createCLAHE(clipLimit=3.0, tileGridSize=(3, 3))
clah4 = cv.createCLAHE(clipLimit=3.0, tileGridSize=(3, 6))
cl1= clah1.apply(l)
cl2 = clah2.apply(l)
cl3 = clah3.apply(l)
cl4 = clah4.apply(l)
limg1 = cv.merge((cl1, a, b))
limg2 = cv.merge((cl2, a, b))
limg3 = cv.merge((cl3, a, b))
limg4 = cv.merge((cl4, a, b))
inal1 = cv.cvtColor(limg1, cv.COLOR_LAB2BGR)
inal2 = cv.cvtColor(limg2, cv.COLOR_LAB2BGR)
inal3 = cv.cvtColor(limg3, cv.COLOR_LAB2BGR)
inal4 = cv.cvtColor(limg4, cv.COLOR_LAB2BGR)
cv.imwrite("./machinEdit1.png", inal1)
cv.imwrite("./machinEdit2.png", inal2)
cv.imwrite("./machinEdit3.png", inal3)
cv.imwrite("./machinEdit4.png", inal4)
# save on pathname
# Finish CLAHE WORK


def BrightnessContrast(brightness=0):
    brightness = bright  # brightness value
    contrast = contre  # contrast value
    effect = controller(img, brightness,
                        contrast)
    cv.imwrite(pathBright, effect)


def controller(img, brightness=255,
               contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness

        al_pha = (max - shadow) / 255
        ga_mma = shadow
        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv.addWeighted(img, al_pha,
                             img, 0, ga_mma)
    else:
        cal = img
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv.addWeighted(cal, Alpha,
                             cal, 0, Gamma)
    # putText renders the specified text string in the image.
    cv.putText(cal, 'B:{},C:{}'.format(brightness,
                                       contrast), (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return cal
BrightnessContrast(127)
""" ^^ FILTER SECTIONS ^^ """


"""BUTTON START Tkinter GUI"""
btnStart = tk.Button(winStr,text="Start",bg="#19181a",fg="#f1f1f1",
font=("Verdana", 14),activebackground="#99FF99",bd=0,width=30,command= main)
btnStart.grid(row=5,column=0,rowspan=1,columnspan=2,pady=20,padx=20,ipady=6,ipadx=6)


winStr.mainloop()
