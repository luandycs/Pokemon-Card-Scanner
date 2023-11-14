import cv2
import os
import numpy as np
import pyautogui as pg
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from PIL import Image, ImageTk
import json
import threading
import datetime
import imutils
import pathlib
import math

class CardScouter():
    def __init__(self, window) -> None:
        # PATH/MISC SETTINGS
        self.window = window
        self.window.title("Card Scouter")
        self.window['background'] = "gray"
        self.window.configure(bg='gray')
        self.pathDownloads = "C:\\Users\\PCAero\\Desktop\\sideprojs\\cardS\\photos"
        # RESOLUTIONS
        appWidth = 1600
        appHeight = 1000
        camWidth = int(appWidth*.3)
        camHeight = int(appHeight*.8)

        navbarWidth = int(appWidth*.3)
        navbarHeight = int(appHeight*.1)
        cambarWidth = int(appWidth*.7)
        cambarHeight = int(appHeight*.1)

        libWidth = int(appWidth*.7)
        libHeight = int(appHeight*.9)
        self.window.geometry(str(appWidth) + "x" + str(appHeight))

        colors = {
            "library": "steelblue3",
            "navBar": "royalblue3",
            "menuBar": "royalblue3",
            "canvas": "steelblue4",
            "libContainer": "deepskyblue3",
            "libLabel": "deepskyblue3",
            "dbText": "gray64"

        }
        # self.video = cv2.VideoCapture(0)
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
        self.currentImg = None

        # Main Components
        # Canvas for camera; highlightthickness used to remove weird whitespace around canvas 
        self.canvas = tk.Canvas(master=self.window, background=colors['canvas'], width = camWidth, height = camHeight, 
            borderwidth=8, relief='ridge', highlightthickness=0)
        self.navigationBar = tk.Frame(master=self.window, background=colors['navBar'], width = navbarWidth, height=navbarHeight,
            borderwidth=8, relief='ridge')
        self.camBar = tk.Frame(master=self.window, border=4, background=colors["menuBar"], width = cambarWidth, height=cambarHeight,
            borderwidth=8, relief='ridge')
        self.library = tk.Frame(master=self.window, background=colors['library'], width = libWidth, height=libHeight)

        self.navigationBar.grid(row=0, column=0, sticky="nsew")
        self.library.grid(row=0, column=1, sticky='nsew', rowspan=3)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.camBar.grid(row=2, column=0, sticky='nsew')
        self.library.grid_propagate(False)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=5)
        self.window.grid_rowconfigure(1, weight=1)

        # Component: Library
        self.library.grid_rowconfigure(1, weight=1)
        self.library.grid_columnconfigure(0, weight=1)
        # Library Subcomponents
        # Label Container
        self.libLabelContainer = tk.LabelFrame(master=self.library, width=libWidth, height=navbarHeight,
            borderwidth=8, relief='ridge', highlightthickness=0, background=colors['library'])
        self.libLabel = tk.Label(master=self.libLabelContainer,
            justify='center', font='arial', background=colors['library'], text='Library', highlightthickness=0, borderwidth=0)

        self.libLabelContainer.grid(row=0, column=0, sticky="nsew")
        self.libLabelContainer.grid_propagate(False)
        # Label Container > Label
        self.libLabel.place(relx=0.5, rely=0.45, anchor='center')

        # Library Content Container
        self.libContainer = tk.Frame(master=self.library, highlightthickness=0, borderwidth=0,
            width=libWidth, height=libHeight-(2*navbarHeight), background=colors["libContainer"])
        self.libContainer.grid(row=1, column=0, sticky="new")
        self.libContainer.propagate(False)
        self.libContainer.grid_columnconfigure(0, weight=1)
        self.libContainer.grid_rowconfigure(0, weight=1)
        # Scrolling Database
        rows=10
        imgW = 200 
        imgH = 200
        descW = 100
        descH = 100
        photoCount = self.countFiles()
        if rows < photoCount:
            rows = photoCount

        self.libContainerCanvas = tk.Canvas(master=self.libContainer, highlightthickness=0, borderwidth=0,
            width=libWidth, height=libHeight-(2*navbarHeight), background=colors["libContainer"], 
            scrollregion=(0,0,0,imgH*rows))

        for i in range(rows):
            pic = tk.Canvas(self.libContainer, width=imgW, height=imgH, borderwidth=4, relief='ridge')
            desc = tk.Frame(self.libContainer, width=imgW, height=imgH, borderwidth=4, relief='ridge')

            self.libContainerCanvas.create_window(0, imgH*i, anchor='nw', window=pic)
            self.libContainerCanvas.create_window(imgW+115, imgH*i, anchor='nw', window=desc)
            # desc.grid(row=i, column=0, sticky="nsew")

        self.libScroll = tk.Scrollbar(master=self.libContainer, orient='vertical', highlightthickness=0, width=25)
        self.libScroll.pack(fill='y', side='right', expand=True)
        self.libScroll.config(command=self.libContainerCanvas.yview)

        self.libContainerCanvas.config(yscrollcommand=self.libScroll.set)
        self.libContainerCanvas.pack(side='top', fill='both', expand=True)

        # Subcomponent: Camera Bar
        self.buttonScreenshot = tk.Button(master=self.camBar, text="Capture", command = self.screenshot())
        # self.updateVideo()


    def updateVideo(self):
        ret, frame = self.video.read()

        if ret:
            self.currentImg = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.currentImg)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.window.after(10, self.updateVideo)

    def screenshot(self):
        if self.currentImg is not None:
            self.currentImg.save(self.pathDownloads)
            os.startfile(self.pathDownloads)

    def saveJson(self, dict):
        jsonObj = json.dump(dict, indent=3)
        with open("history.json", "w") as outfile:
            outfile.write(jsonObj)
        
    def countFiles(self):
        files = next(os.walk(self.pathDownloads), (None, None, []))[2]
        return len(files)
        
    # def getPath(self):
    #     return self.path
        
    # def start(self):
    #     cam = cv2.VideoCapture(0)
    #     camWidth, camHeight = 1080, 720
    #     cam.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
    #     cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
    #     while True:
    #         check, frame = cam.read()
    #         cv2.imshow('webcam capture', frame)

    #         key = cv2.waitKey(1)
    #         if key == 27:
    #             break
    #         elif key == 32:
    #             img_name = "s{}.png".format(self.img_counter)
    #             frame_mod = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
    #             cv2.imwrite(img_name, frame_mod)
    #             print("{} saved!".format(img_name))
    #             self.img_counter += 1
    #         else:
    #             continue
    
            
    #     cam.release()
    #     cv2.destroyAllWindows()

    # def startCardLookup(self):
    #     driver = webdriver.Chrome(executable_path="C://Users//PCAero//Desktop//sideprojs//cardS//chromedriver.exe")
    #     driver.get("https://images.google.com")
    #     # driver.get("https://www.tcgplayer.com")
