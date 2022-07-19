
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
wincap = WindowCapture('Runelite - Vessacks')


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

#setup
#1 put clean herbs in inventory (dumb, I know, but you must)
#2 make sure dirty herbs are visible in the opening bank tab
#3 set bank options to one click deposit/withdraw all, unnoted
#4 make sure no herbs appear as bank tags-- it will click them thinking they're items
#5 make sure you are in private chat and that nothing has been said (it expects a blank chat window when checking for in_bank)
#6 take new bank needle image each time; orientations change

print('welcome to herbcleaner! I will find whatever herb you have fed me an image of, clean it, and replace it it.')

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
    
    #pause
    time.sleep(np.random.normal(.5,.07))

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

    #2 check its in bank
    screenshot = wincap.get_screenshot()
    in_bankWindow = in_bank_vision.find(screenshot, 0.99, 'rectangles')
    if in_bankWindow == []:
        print('not in bank when expected, exiting')
        exit()

    #pause
    time.sleep(np.random.normal(.6,.07))

    #3 find clean herbs
    screenshot = wincap.get_screenshot()
    clean_herbWindow = clean_herb_vision.find(screenshot, 0.99, 'rectangles')
    if clean_herbWindow == []:
        print('expected clean herbs to bank, none found. exiting')
        exit()

    #dump clean herbs
    clean_herbScreen = wincap.get_screen_position(clean_herbWindow)
    clean_herbClickpoint = clean_herb_action.click(clean_herbScreen)

    #pause
    time.sleep(np.random.normal(.6,.07))

    #4 find dirty herbs
    screenshot = wincap.get_screenshot()
    dirty_herbWindow = dirty_herb_vision.find(screenshot, 0.99, 'rectangles')
    if dirty_herbWindow == []:
        print('expected to find dirty herbs in bank, none found. exiting')
        exit()
    
    #5 click dirty herb in bank
    dirty_herbScreen = wincap.get_screen_position(dirty_herbWindow)
    dirty_herbClickPoint = dirty_herb_action.click(dirty_herbScreen)

    #pause
    time.sleep(np.random.normal(.6,.07))

    #6 find bank exit
    screenshot = wincap.get_screenshot()
    bank_xWindow = bank_x_vision.find(screenshot, 0.99, 'rectangles')
    if bank_xWindow == []:
        print('couldn\'t find bank exit button. exiting program')
        exit()
    
    #7 click bank exit
    bank_xScreen = wincap.get_screen_position(bank_xWindow)
    bank_xClickpoint = bank_x_action.click(bank_xScreen)

    #8 check you're outside the bank by checking for bank entrance
    screenshot = wincap.get_screenshot()
    bankWindow = bank_vision.find(screenshot, 0.99, 'rectangles')
    if bankWindow == []:
        print('expected to be outside bank, exiting')
        exit()

    #pause
    time.sleep(np.random.normal(.6,.07))

    #9 find dirty herb in inventory
    screenshot = wincap.get_screenshot()
    dirty_herbWindow = dirty_herb_vision.find(screenshot, 0.99, 'rectangles')
    if dirty_herbWindow == []:
        print('expected to find dirty herbs in inventory, none found. exiting')
        exit()

    #10 click dirty herb in inventory
    dirty_herbScreen = wincap.get_screen_position(dirty_herbWindow)
    dirty_herbClickPoint = dirty_herb_action.click(dirty_herbScreen)

    #11 dirty herb counting loop
    num_dirty_herbs = 0
    change_time = time.time()
    loop_time = time.time()

    while True:
        screenshot = wincap.get_screenshot()
        dirty_herbs_all = dirty_herb_vision.find(screenshot, 0.99,return_mode = 'allPoints')

        #checking for change, reset change timer if so
        if num_dirty_herbs != len(dirty_herbs_all):
            change_time = time.time()
        
        #reset num_dirty_herbs to len(dirty_herbs_all)
        num_dirty_herbs = len(dirty_herbs_all)

        #check for timeout, attempt reclick
        if time.time() - change_time > HERB_RECLICK_TIMER:
            print('WARNING: no change in num_dirty_herbs in %s, attempting reclick'% (time.time() - change_time))
            screenshot = wincap.get_screenshot()
            dirty_herbWindow = dirty_herb_vision.find(screenshot, 0.99, 'rectangles')
            if dirty_herbWindow == []:
                print('expected to find dirty herbs in inventory, none found. reclick failed, not exiting')
                
            else:
                print('found reclickable herb, attempting reclick')
                dirty_herbScreen = wincap.get_screen_position(dirty_herbWindow)
                dirty_herbClickPoint = dirty_herb_action.click(dirty_herbScreen)

        #check for unrecoverable problem, ie timeout
        if time.time() - change_time > HERB_LOGOUT_TIMER:
            print('WARNING: no change in num_dirty_herbs, logout timer reached. exiting')
            exit()
        

        # debug the loop rate
        print('dirty_herbs = ' + str(num_dirty_herbs) + '| runTime = '+str(round(time.time() - startTime))+ ' | change_timer = '+ str(time.time() - change_time) + '| FPS {}'.format(1 / ((time.time() - loop_time))))
        loop_time = time.time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        
        #checks to see if you're out of dirty_herbs
        if num_dirty_herbs == 0:
            print('I see no more dirty herbs, going to get more')
            #pause
            time.sleep(np.random.normal(.6,.07))
            break

    
     


