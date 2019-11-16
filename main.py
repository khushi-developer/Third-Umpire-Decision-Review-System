import tkinter
import cv2 #pip install opencv-python
import PIL
from PIL import ImageTk,Image #pip install pillow
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("clip.mp4")

#width and height for main screen
SET_WIDTH = 900
SET_HEIGHT = 368

def out():
    thread = threading.Thread(target=pending , args=("out",))
    thread.daemon=1
    thread.start()
    print("you are out")

def pending(decision):
    # 1.Display decision pending image
    # convert png image to jpg
    im = Image.open('decision.jpg')
    im = im.save('decision.png')
    frame = cv2.cvtColor(cv2.imread("decision.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    # 2.wait for 1 second
    time.sleep(1)
    
    # 3.Display sponser image
    im = Image.open('sponser.jpg')
    im = im.save('sponser.png')
    frame = cv2.cvtColor(cv2.imread("sponser.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 4.wait for 1.5 second
    time.sleep(1.5)
    # 5.Display out/not-out image
    im = Image.open("out.jpg")
    im = im.save("out.png")

    im = Image.open("notout.jpg")
    im = im.save("notout.png")

    if decision=='out':
        decisionImg = "out.png"
    else:
        decisionImg = "notout.png"

    frame = cv2.cvtColor(cv2.imread(decisionImg),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

def notout():
    thread = threading.Thread(target=pending , args=("not out",))
    thread.daemon=1
    thread.start()
    print("you are not out")

flag = True
def play(speed):
    # play the video
    global flag
    print(f"you click on play. speed is {speed}")
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)  #cv2.CAP_PROP_POS_FRAMES which frame
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame , anchor=tkinter.NW)
    if flag:
        canvas.create_text(129,20,fill="black",font="times 26 bold",text="Decision pending")
    flag = not flag

# tkinter gui
window = tkinter.Tk()
window.title("DRS system")

im = Image.open('welcome.jpg')
im = im.save('welcome.png')

cv_img = cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
canvas=tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
img_on_canvas=canvas.create_image(0,0,ancho=tkinter.NW,image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window,text="<< previous(fast)", width = 50,command=partial(play,-25))
btn.pack()

btn = tkinter.Button(window,text="<< previous(slow)", width = 50,command=partial(play,-2))
btn.pack()

btn = tkinter.Button(window,text=" next(slow) >>", width = 50,command=partial(play,2))
btn.pack()

btn = tkinter.Button(window,text=" next(fast) >>", width = 50,command=partial(play,25))
btn.pack()

btn = tkinter.Button(window,text=" Give out", width = 50,command=out)
btn.pack()

btn = tkinter.Button(window,text=" Give not out", width = 50,command=notout)
btn.pack()


window.mainloop()