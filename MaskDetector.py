from tkinter import *
from tensorflow import expand_dims
from tensorflow.keras.models import load_model
from PIL import ImageTk, Image
from tkinter import messagebox
import cv2 as cv
import numpy as np
import HomePage as hp

class MaskDetector():
    def __init__(self, window, source=0,color_code=0):
        self.window = window
        self.colorTheme(color_code)

        # creating menu for back to Home Page
        main_menu = Menu(self.window,
                         bg=self.header_clr,
                         fg=self.bg_clr,
                         activebackground=self.bg_clr,
                         activeforeground=self.header_clr,
                         activeborderwidth=0,
                         font=('Helvetica', 11, 'bold'),
                         tearoff=0,
                         bd=0)

        main_menu.add_command(label='Back', command=lambda: self.back(color_code))

        self.window.config(menu=main_menu)

        # creating VideoCapture object
        self.cap = cv.VideoCapture(source)
        
        # Loading Face Mask Detector pretrained model
        self.model = load_model('models/pretrained_mask_detector.h5')
        
        # Loading Haar Cascade Classifier for detecting faces
        self.cascade = cv.CascadeClassifier('models/haarcascade_frontalface_default.xml')

        # Configure Window
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Checking for video source is correctly open or not
        if self.cap.isOpened():

            # Assigning the essential values
            self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

            # Defining the Label and placed it on the window
            self.screen = Label(self.window,
                                 bg=self.bg_clr,
                                 highlightbackground=self.bg_clr,
                                 highlightthickness=2,
                                 bd=0)
            self.screen.grid(row=0, column=0, sticky=NSEW)

            # Calling the updateFrame for showing the video feed continuously
            self.updateFrame()
        else:
            # Show the error
            messagebox.showerror('No Video Feed', 'Program can\'t open the camera or the video file :(')

            # destroy the main window and exit from the program
            self.window.destroy()

    def updateFrame(self):
        # taking the each frame numpy array mode
        ret, frame = self.cap.read()

        # Checking if frame is available or not
        if ret:
            # Predicting faces
            self.image = self.predictFace(frame)
            
            # Resize the frame 
            self.image = cv.resize(self.image, (225*4,225*3))
            
            # Convert frame array to a pyImage
            self.image = ImageTk.PhotoImage(Image.fromarray(self.image))
            
            # Place it one the label
            self.screen.config(image=self.image)
            
            # again we need to anchor it to the label for some reason
            self.screen.image = self.image
						
            # Calling the this function after 5 milliseconds
            self.video = self.window.after(5, self.updateFrame)
        else:
            # destroy the main window and exit from the program
            self.window.destroy()

    def predictFace(self,img):
        # detecting faces from the image or frame
        faces = self.cascade.detectMultiScale(img, 1.15, 5)
        
        # change color channels to BGR to RBG
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
        # iterate though each faces
        for (x, y, w, h) in faces:
            # Cropping the faces from images and resize to 128x128
            img_arr = cv.resize(img[y:y+h,x:x+w], (128, 128))

            # expanding dimension for prediction
            img_arr = expand_dims(img_arr, 0)
						
            # make prediction
            predict_val = self.model.predict(img_arr)

            if predict_val[0][0] < 0.5:
                color = (83,255,84)
                text = 'Mask'
            else:
                color = (255,84,83)
                text = 'No Mask'
            cv.rectangle(img, (x, y), (x + w, y + h), color, 3, cv.LINE_AA)
            cv.putText(img,
                       text=text,
                       org=(x, y - 10),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=.7,
                       color=color,
                       thickness=1,
                       lineType=cv.LINE_AA)

        return img
     
    def colorTheme(self, code=0):
        # for Light Theme
        if code == 0:
            self.bg_clr = '#f8f8f8'
            self.text_clr = '#010101'
            self.header_clr = '#0b73b8'
            self.border_clr = '#282828'

        # for Warm Theme
        elif code == 1:
            self.bg_clr = '#fff9db'
            self.text_clr = '#010101'
            self.header_clr = '#ff4b0f'
            self.border_clr = '#282828'

        # for Dark Theme
        elif code == 2:
            self.bg_clr = '#282828'
            self.text_clr = '#f8f8f8'
            self.header_clr = '#c880f8'
            self.border_clr = '#a8a8a8'

    def back(self,color_code):
        # Stoping the animation loop
        self.window.after_cancel(self.video)

        # Releasing the VideoCapture object
        self.cap.release()

        # Clearing the window widgets
        for widgets in self.window.winfo_children():
            widgets.destroy()

        # Calling the Mask Detector
        hp.HomePage(self.window, color_code)



if __name__ == '__main__':
    root = Tk()
    root.config(bg='#222')
    root.title('Mask Detector')
    root.geometry('1000x600')

    app = MaskDetector(root,)

    root.mainloop()
