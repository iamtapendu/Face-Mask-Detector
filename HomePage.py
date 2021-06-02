from tkinter import *
import cv2 as cv
from PIL import ImageTk, Image
import webbrowser as wb
import MaskDetector as md



class HomePage:
    def __init__(self, window, color_code=0):
        # Configuring root Window
        self.window = window
        self.window.title('Face Mask Detector')
        self.colorTheme(color_code)
        self.window.geometry('1000x600')
        self.window.config(bg=self.bg_clr)
        intro_file = ['logo_n_intro/light_intro.mp4',
        							'logo_n_intro/warm_intro.mp4',
        							'logo_n_intro/dark_intro.mp4']

        # creating menu for Theme
        main_menu = Menu(self.window,
                         bg=self.header_clr,
                         fg=self.bg_clr,
                         activebackground=self.bg_clr,
                         activeforeground=self.header_clr,
                         activeborderwidth=0,
                         font=('Helvetica', 11, 'bold'),
                         tearoff=0,
                         bd=0)

        main_menu.add_command(label='Light Theme', command=lambda: self.restart(0))
        main_menu.add_command(label='Warm Theme', command=lambda: self.restart(1))
        main_menu.add_command(label='Dark Theme', command=lambda: self.restart(2))

        self.window.config(menu=main_menu)

        # Configure rows and columns for dynamic changes in widget
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=15)
        # self.window.rowconfigure(2, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Creating essential frames
        self.header_frame = Frame(self.window, bg=self.bg_clr)
        self.content_frame = Frame(self.window, bg=self.bg_clr)
        self.status_frame = Frame(self.window, bg=self.bg_clr)

        # Placed them on the main window
        self.header_frame.grid(row=0, column=0, sticky=NSEW, padx=0, pady=0)
        self.content_frame.grid(row=1, column=0, sticky=NSEW, padx=0, pady=0)
        self.status_frame.grid(row=2, column=0, sticky=EW, padx=0, pady=0)

        '''================================= Header Frame ================================='''
        # Configure header frame
        self.header_frame.rowconfigure(0, weight=1)
        self.header_frame.columnconfigure(0, weight=1)

        # Creating header label and Placed it on the header frame
        self.header = Label(self.header_frame,
                            text="FACE MASK DETECTOR",
                            font=('Helvetica', 36, 'bold'),
                            relief=FLAT,
                            bg=self.bg_clr, fg=self.header_clr,
                            highlightbackground=self.bg_clr,
                            highlightthickness=2,
                            anchor=CENTER)
        self.header.grid(row=0, column=0)

        '''============================== Header Frame End =============================='''


        '''================================= Content Frame ================================='''
        # Configure content frame
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

        # creating greet and About frame
        self.greet_frame = Frame(self.content_frame, bg=self.bg_clr)
        self.about_frame = Frame(self.content_frame, bg=self.bg_clr)

        # Placing them on content frame
        self.greet_frame.grid(row=0, column=0, sticky=NSEW)
        self.about_frame.grid(row=0, column=1, sticky=NSEW)

        # Creating label for Greeting Animation
        self.welcome = Label(self.greet_frame, anchor=CENTER,
                             bg=self.bg_clr,
                             highlightbackground=self.bg_clr)
        self.cap = cv.VideoCapture(intro_file[color_code])
        self.ret = True
        self.showAnimation()

        # Creating mask detector launch button
        self.btn = Button(self.greet_frame,
                          text='DETECT MASK',
                          font=('Helvetica', 30, 'bold'), relief=FLAT,
                          bg=self.bg_clr, fg=self.header_clr,
                          highlightbackground=self.header_clr,
                          highlightthickness=1, padx=10, pady=10,
                          activebackground=self.header_clr,
                          activeforeground=self.bg_clr,
                          anchor=CENTER,
                          command=lambda:self.maskDetect(color_code))

        # Creating about section
        # Author photo
        self.img = ImageTk.PhotoImage(Image.open('logo_n_intro/author.png').resize((200, 200), Image.ANTIALIAS))
        self.profile_photo = Label(self.about_frame,
                                   image=self.img,
                                   relief=FLAT,
                                   bg=self.bg_clr,
                                   bd=0,
                                   highlightbackground=self.bg_clr)
        self.profile_photo.image = self.img  # need to anchor the image

        # Author Contact
        self.contact = Label(self.about_frame,
                             text='CONTACT',
                             relief=FLAT,
                             bg=self.bg_clr,
                             fg=self.header_clr,
                             font=('Helvetica', 26, 'bold'),
                             highlightbackground=self.bg_clr)
        # Contact Information

        self.author_name = Label(self.about_frame,
                                 text='  Name :\tTapendu Karmakar',
                                 relief=FLAT,
                                 bg=self.bg_clr,
                                 fg=self.text_clr,
                                 font=('Helvetica', 15),
                                 highlightbackground=self.bg_clr,
                                 anchor=W)

        self.author_email = Label(self.about_frame,
                                  text='  Email :\ttape100kamar@gmail.com',
                                  relief=FLAT,
                                  bg=self.bg_clr,
                                  fg=self.text_clr,
                                  font=('Helvetica', 15),
                                  highlightbackground=self.bg_clr,
                                  anchor=W)

        # Create different account links
        self.git_btn, self.git_logo = self.createButton(self.about_frame,
                                                        'logo_n_intro/github_logo.png',
                                                        lambda: wb.open_new('https://github.com/iamtapendu'),
                                                        )

        self.kaggle_btn, self.kaggle_logo = self.createButton(self.about_frame,
                                                              'logo_n_intro/kaggle_logo.png',
                                                              lambda: wb.open_new('https://kaggle.com/iamtapendu'),
                                                              )

        self.linkedin_btn, self.linkedin_logo = self.createButton(self.about_frame,
                                                                  'logo_n_intro/linkedin_logo.png',
                                                                  lambda: wb.open_new('https://linkedin.com/in/iamtapendu'),
                                                                  )

        # Configure Frames
        self.greet_frame.rowconfigure(0, weight=1)
        self.greet_frame.rowconfigure(1, weight=1)
        self.greet_frame.columnconfigure(0, weight=1)

        self.about_frame.rowconfigure(0, weight=1)
        self.about_frame.rowconfigure(1, weight=1)
        self.about_frame.rowconfigure(2, weight=1)
        self.about_frame.rowconfigure(3, weight=1)
        self.about_frame.rowconfigure(4, weight=1)
        self.about_frame.columnconfigure(0, weight=1)
        self.about_frame.columnconfigure(1, weight=1)
        self.about_frame.columnconfigure(2, weight=1)

        # Placed them on the frames
        self.welcome.grid(row=0, column=0)
        self.btn.grid(row=1, column=0)
        self.profile_photo.grid(row=0, column=0, columnspan=3)
        self.contact.grid(row=1, column=0, sticky=EW, columnspan=3)
        self.author_name.grid(row=2, column=0, sticky=EW, columnspan=3)
        self.author_email.grid(row=3, column=0, sticky=EW, columnspan=3)
        self.git_btn.grid(row=4, column=0)
        self.kaggle_btn.grid(row=4, column=1)
        self.linkedin_btn.grid(row=4, column=2)

        '''============================== Content Frame Ends =============================='''


        '''================================= Status Frame ================================='''
        # Configure status frame
        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.columnconfigure(1, weight=1)

        # Creating version and copyright named two labels
        self.version = Label(self.status_frame,
                             text='Version\t\tv1.0  ',
                             font=('Helvetica', 12, 'bold'),
                             relief=FLAT,
                             bg=self.bg_clr,
                             fg=self.text_clr,
                             highlightbackground=self.border_clr,
                             highlightthickness=1,
                             anchor=E)
        self.copyright = Label(self.status_frame,
                               text='  Copyright (c) 2021 Tapendu Karmakar',
                               font=('Helvetica', 12, 'bold'),
                               relief=FLAT,
                               bg=self.bg_clr,
                               fg=self.text_clr,
                               highlightbackground=self.border_clr,
                               highlightthickness=1,
                               anchor=W)

        # Placing them on the status label
        self.copyright.grid(row=0, column=0, sticky=EW)
        self.version.grid(row=0, column=1, sticky=EW)
        '''============================== Status Frame Ends =============================='''

    def showAnimation(self):
        if self.ret:
            # Receiving frames from the video
            self.ret, frame = self.cap.read()

            # Converting BGR mode to RGB mode
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            # Resize the video frame to appropriate size
            frame = cv.resize(frame, (32*16, 32*9))

            # Converting array format to PyImage format
            self.anim_frame = ImageTk.PhotoImage(Image.fromarray(frame))

            # attaching to the label
            self.welcome.config(image=self.anim_frame)
            self.welcome.image = self.anim_frame    # need to anchor the image

            # calling the the function again
            self.anim_loop = self.window.after(1, self.showAnimation)

    def createButton(self, window, logo, command):
        # Loading and resize the button logo
        logo = Image.open(logo)
        logo = logo.resize((64, 64), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)

        # Defining and placing the button
        btn = Button(window,
                     image=logo,
                     relief=FLAT,
                     bg=self.bg_clr,
                     bd=0,
                     highlightbackground=self.bg_clr,
                     activebackground=self.bg_clr,
                     command=command,
                     )
        return btn, logo

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

    def restart(self, color_code=0):
        # Stoping the animation loop
        self.window.after_cancel(self.anim_loop)
        
        # Releasing the VideoCapture object
        self.cap.release()
        
        # Clearing the window widgets
        for widgets in self.window.winfo_children():
            widgets.destroy()
        
        # Reinitialize the HomePage with specified color code
        HomePage(self.window,color_code)

    def maskDetect(self,color_code):
        # Stoping the animation loop
        self.window.after_cancel(self.anim_loop)
        
        # Releasing the VideoCapture object
        self.cap.release()
        
        # Clearing the window widgets
        for widgets in self.window.winfo_children():
            widgets.destroy()
         
        # Calling the Mask Detector
        md.MaskDetector(self.window,0,color_code)



if __name__ == '__main__':
    root = Tk()
    HomePage(root)
    root.mainloop()
