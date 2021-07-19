import cv2
import cv2 as cv
import pytesseract
import subprocess
import numpy
from datetime import datetime
import time

import numpy as np
import pyautogui
import imutils
import cv2

class watcher(object):
    def __init__(self):
        self.templates = []
        self.template_names = ["rewards"]
        self.load_templates()
    
    def load_templates(self):
        
        for Name in self.template_names:
            test = []
            test.append(Name)
            image = cv.imread("templates/"+Name+".png",cv.IMREAD_REDUCED_COLOR_2)
            test.append(image)
            self.templates.append(test)

    def log(self,info):
        now = datetime.now().time()
        now = str(now)
        print(now+" : "+info)

    def find_pos(self, template_name):
        ergebnis = []
        positon = self.template_names.index(template_name)
        template = self.templates[positon]

        name = template[0]
        image = template[1]
        ergebnis.append(name)
        screen = cv.imread("Bilder/screen.png",cv.IMREAD_REDUCED_COLOR_2)
        result = cv.matchTemplate(screen, image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
        image_w = int(image.shape[1]/2)
        image_h = int(image.shape[0]/2)
        self.log("Best match top left position: %s" % str(max_loc))
        self.log("Best match confidence: %s" %max_val)
        self.log("Found "+name)
        #x = (max_loc[0]+image_w)*2
        #y = (max_loc[1]+image_h)*2
        x = (max_loc[0])*2
        y = (max_loc[1])*2
        werte_pos = []
        werte_pos.append(x)
        werte_pos.append(y)
        ergebnis.append(werte_pos)
        ergebnis.append(max_val)

        return(ergebnis)
Watcher = watcher()       
pytesseract.pytesseract.tesseract_cmd = "tesseract/tesseract.exe"

def crop_prime_part(x, img):
    h = 45
    y = 415
    w = 230
    crop_img = img[y:y+h, x:x+w]
    text = pytesseract.image_to_string(crop_img)
    text = text.replace("","")
    text = text.replace("\n"," ")
    print(text)
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
    if text != "":
        print(text)
        file = open("found.txt","a")
        file.write("\n"+text)
        file.close()

def make_Screen():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("Bilder/screen.png", image)

def need_to_read():
    img = cv2.imread("Bilder/screen.png")
    position = Watcher.find_pos("rewards")
    max_val = position[2]

    if max_val >= 0.8:
        all_x = [800,1040,1285,1525]
        for x in all_x:
            crop_prime_part(x, img)
        
while True:
    make_Screen()
    need_to_read()
    

