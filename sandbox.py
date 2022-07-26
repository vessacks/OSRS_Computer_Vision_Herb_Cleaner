#sandbox.py

#Computer_Vision_Herb_Cleaner_FAST
#this one differs from the main herb cleaner because it clicks each herb individually, and fast

#main.py
import cv2 as cv
from cv2 import threshold
import numpy as np
import os
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
from action import Action



# initialize the WindowCapture class
wincap = WindowCapture('sandbox.PNG - Paint')


# initialize the Vision class
clean_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\clean_herb.png', method= cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)


print('welcome to herbcleaner! I will find whatever herb you have fed me an image of, clean it, and replace it it.')
DETECTION_THRESHOLD = .97

screenshot = wincap.get_screenshot()
screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)


#cv.imread('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\sandbox.png',cv.IMREAD_GRAYSCALE)

while True:
    clean_herbWindow = clean_herb_vision.find(screenshot, DETECTION_THRESHOLD, debug_mode='rectangles', return_mode = 'bestPoint')
    clean_herbConfidence = clean_herb_vision.find(screenshot, DETECTION_THRESHOLD, debug_mode='rectangles', return_mode = 'confidence')
    #clean_herbWindowAllPoints = clean_herb_vision.find(screenshot, DETECTION_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints')
    
    print('clean_herb confidence = %s | DETECTION_THRESHOLD = %s ' %(clean_herbConfidence[1], DETECTION_THRESHOLD))

    clean_herbClickPoint = wincap.get_screen_position(clean_herbConfidence[0])
    print('best herb at screencoords %s, %s ' % (str(clean_herbClickPoint[0]), str(clean_herbClickPoint[1])))
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()
