#click dist. tester


#main.py
import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
from action import Action



# initialize the WindowCapture class
wincap = WindowCapture('click_dist_tester.PNG - Paint')


# initialize the Vision class
clean_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\clean_herb.png')
dirty_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_herb.png')
bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank.png')
in_bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\in_bank.png')
bank_x_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank_x.png')

#initialize the action class
dirty_herb_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_herb.png')
clean_herb_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\clean_herb.png')
bank_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank.png')
bank_x_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank_x.png')





startTime = time.time()
STOP_AFTER = float(input('please type the number of seconds you would like to run the script, then press enter. '))
HERB_RECLICK_TIMER = 5
HERB_LOGOUT_TIMER = 20


while True:
    
    #0 check if runtime elapsed
    runTime = time.time() - startTime
    if runTime > STOP_AFTER:
        print('completed run. final runtime was %s' % runTime)
        exit()
    


    #1 open bank
    #take a screenshot
    screenshot = wincap.get_screenshot()

    # get an updated image of the game and look for object of interest
    bankWindow = bank_vision.find(screenshot, 0.99, 'rectangles')

    #check it found bank
    if bankWindow == []:
        print('failed to find bank, exiting')
        exit()

    #once it's found the object, translate to screen coords and click
    bankScreen = wincap.get_screen_position(bankWindow)
    bankClickpoint = bank_action.click(bankScreen)


    #6 find bank exit
    screenshot = wincap.get_screenshot()
    bank_xWindow = bank_x_vision.find(screenshot, 0.99, 'rectangles')
    if bank_xWindow == []:
        print('couldn\'t find bank exit button. exiting program')
        exit()
    
    #7 click bank exit
    bank_xScreen = wincap.get_screen_position(bank_xWindow)
    bank_xClickpoint = bank_x_action.click(bank_xScreen)

    #9 find dirty herb in inventory
    screenshot = wincap.get_screenshot()
    dirty_herbWindow = dirty_herb_vision.find(screenshot, 0.99, 'rectangles', return_mode = 'allPoints')


    for x in dirty_herbWindow:
        dirty_herbScreen = wincap.get_screen_position(x)
        dirty_herbClickPoint = dirty_herb_action.click(dirty_herbScreen)

    
     


