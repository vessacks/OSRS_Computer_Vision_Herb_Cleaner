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
wincap = WindowCapture('Runelite - Vessacks')


# initialize the Vision class
clean_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\clean_herb.png',imread= cv.IMREAD_GRAYSCALE)
dirty_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_herb.png',imread= cv.IMREAD_GRAYSCALE)
dirty_bank_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_bank_herb.png',imread= cv.IMREAD_GRAYSCALE)
bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank.png',imread= cv.IMREAD_GRAYSCALE)
in_bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\in_bank.png',imread= cv.IMREAD_GRAYSCALE)
bank_x_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank_x.png',imread= cv.IMREAD_GRAYSCALE)

#initialize the action class
dirty_herb_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_herb.png')
dirty_bank_herb_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_bank_herb.png')
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
#7 make sure window mode is set to classic fixed layout



print('welcome to herbcleaner! I will find whatever herb you have fed me an image of, clean it, and replace it it.')
loop_time = time.time()
startTime = time.time()
numLoops = 0
STOP_AFTER = float(input('please type the number of seconds you would like to run the script, then press enter. Note: it chews about 1.75 herb/sec. 1h is 3600s, 6h is 21600 '))

HERB_RECLICK_TIMER = 5
HERB_LOGOUT_TIMER = 20
bank_entrance_threshold = .70
in_bank_threshold = .75
clean_herb_threshold = .65
dirty_bank_herb_threshold = .36
bank_exit_threshold = .6
dirty_herb_threshold = .6


while True:

    #pause
    time.sleep(np.random.normal(.5,.07))

    #1 open bank
    #take a screenshot
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    # get an updated image of the game and look for object of interest
    bankWindow = bank_vision.find(screenshot, bank_entrance_threshold, debug_mode='rectangles')
    bankWindowConfidence = bank_vision.find(screenshot, bank_entrance_threshold, debug_mode='rectangles', return_mode = 'confidence')
    bankWindowAllPoints = bank_vision.find(screenshot, bank_entrance_threshold, debug_mode='rectangles', return_mode = 'allPoints')
    #check it found bank
    if bankWindowConfidence[1] < bank_entrance_threshold:
        print('bankWindow confidence = %s | DETECTION_THRESHOLD = %s | exiting...' %(bankWindowConfidence[1], bank_entrance_threshold))
        exit()
    

    #once it's found the object, translate to screen coords and click
    bankScreen = wincap.get_screen_position(bankWindow)
    bankClickPoint = bank_action.click(bankScreen,speed =.7)
    print('num banks found = %s/1 | confidence best bank = %s | screencoords best bank=  %s' % (len(bankWindowAllPoints), bankWindowConfidence[1], bankClickPoint))


    #2 check its in bank
    time.sleep(abs(np.random.normal(2,.07))) #need to wait for bank to appear
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    #in_bankWindow = in_bank_vision.find(screenshot, in_bank_threshold, debug_mode='rectangles')
    in_bankConfidence = in_bank_vision.find(screenshot, in_bank_threshold, debug_mode='rectangles', return_mode = 'confidence')
    if in_bankConfidence[1] < in_bank_threshold:
        print('in_bank confidence = %s | DETECTION_THRESHOLD = %s | exitting...' %(in_bankConfidence[1], in_bank_threshold))
        exit()
    else: print('in_bank confidence = %s ... continuing...' % in_bankConfidence[1])

  
    #3 find clean herbs
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    clean_herbWindow = clean_herb_vision.find(screenshot, clean_herb_threshold, debug_mode='rectangles', return_mode = 'bestPoint')
    clean_herbConfidence = clean_herb_vision.find(screenshot, clean_herb_threshold, debug_mode='rectangles', return_mode = 'confidence')
    clean_herbWindowAllPoints = clean_herb_vision.find(screenshot, clean_herb_threshold, debug_mode='rectangles', return_mode = 'allPoints')
    if clean_herbConfidence[1] < clean_herb_threshold:
        print('clean_herb confidence = %s | DETECTION_THRESHOLD = %s | exiting...' %(clean_herbConfidence[1], clean_herb_threshold))
        exit()
    
    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #dump clean herbs
    clean_herbScreen = wincap.get_screen_position(clean_herbWindow)
    clean_herbClickPoint = clean_herb_action.click(clean_herbScreen, speed=.65)
    print('num clean herbs = %s/28 | confidence best herb = %s | screencoords best herb=  %s' % (len(clean_herbWindowAllPoints), clean_herbConfidence[1], clean_herbClickPoint))

    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #4 find dirty herbs
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    dirty_bank_herbWindow = dirty_bank_herb_vision.find(screenshot, dirty_bank_herb_threshold, debug_mode='rectangles')
    dirty_bank_herbConfidence = dirty_herb_vision.find(screenshot, dirty_bank_herb_threshold, debug_mode='rectangles', return_mode = 'confidence')
    dirty_bank_herbWindowAllPoints = dirty_herb_vision.find(screenshot, dirty_bank_herb_threshold, debug_mode='rectangles', return_mode = 'allPoints')
    if dirty_bank_herbConfidence[1] < dirty_bank_herb_threshold:
        print('dirty_bank_herb confidence = %s | DETECTION_THRESHOLD = %s | exiting...' %(dirty_bank_herbConfidence[1], dirty_bank_herb_threshold))
        exit()
    
    #5 click dirty herb in bank
    dirty_bank_herbScreen = wincap.get_screen_position(dirty_bank_herbWindow)
    dirty_bank_herbClickPoint = dirty_bank_herb_action.click(dirty_bank_herbScreen, .65)
    print('num dirty_bank_herbs = %s/1 | confidence best herb = %s | screencoords best herb=  %s' % (len(dirty_bank_herbWindowAllPoints), dirty_bank_herbConfidence[1], dirty_bank_herbClickPoint))



    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #6 find bank exit
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    bank_xWindow = bank_x_vision.find(screenshot, bank_exit_threshold, debug_mode='rectangles')
    bank_xWindowConfidence = bank_x_vision.find(screenshot, bank_exit_threshold, debug_mode='rectangles', return_mode = 'confidence')
    bank_xWindowAllPoints = bank_x_vision.find(screenshot, bank_exit_threshold, debug_mode='rectangles', return_mode = 'allPoints')
    if bank_xWindowConfidence[1] < bank_exit_threshold:
        print('bank_x confidence = %s | DETECTION_THRESHOLD = %s | exiting...' %(bank_xWindowConfidence[1], bank_exit_threshold))
        exit()
    
    #7 click bank exit
    bank_xScreen = wincap.get_screen_position(bank_xWindow)
    bank_xClickPoint = bank_x_action.click(bank_xScreen)
    print('num bank_x = %s/1 | confidence best bank_x = %s | screencoords best bank_x =  %s' % (len(bank_xWindowAllPoints), bank_xWindowConfidence[1], [round(bank_xClickPoint[0]),round(bank_xClickPoint[1])]))



    #8 check you're outside the bank by checking for bank entrance
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    bankWindow = bank_vision.find(screenshot, bank_entrance_threshold, debug_mode='rectangles')
    bankWindowConfidence = bank_vision.find(screenshot, bank_entrance_threshold, debug_mode='rectangles', return_mode = 'confidence')
    bankWindowAllPoints = bank_vision.find(screenshot, bank_entrance_threshold, debug_mode='rectangles', return_mode = 'allPoints')
    if bankWindowConfidence[1] < bank_entrance_threshold:
        print('bank entrance confidence = %s | DETECTION_THRESHOLD = %s | exiting...' %(bankWindowConfidence[1], bank_entrance_threshold))
        exit()
    else: 
        print('num bank = %s/1 | confidence best bank = %s | WINDOWCOORDS(!) best bank =  %s' % (len(bankWindowAllPoints), bankWindowConfidence[1], bankWindow))


    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #9 find dirty herb in inventory
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    dirty_herbWindow = dirty_herb_vision.find(screenshot, dirty_herb_threshold, debug_mode='rectangles')
    dirty_herbWindowAllPoints = dirty_herb_vision.find(screenshot, dirty_herb_threshold, debug_mode='rectangles',return_mode = 'allPoints')
    dirty_herbConfidence = dirty_herb_vision.find(screenshot, dirty_herb_threshold, debug_mode='rectangles', return_mode = 'confidence')
    if dirty_herbConfidence[1] < dirty_herb_threshold:
        print('dirty herb confidence = %s | DETECTION_THRESHOLD = %s | exiting...' %(dirty_herbConfidence[1], dirty_herb_threshold))
        exit()

    else: 
        print('num dirty_herbs = %s/28 | confidence best herb = %s' % (len(dirty_herbWindowAllPoints), dirty_herbConfidence[1]))
   
    #10 click dirty herb in inventory
    for herb in dirty_herbWindowAllPoints:
        dirty_herbScreen = wincap.get_screen_position(herb)
        time.sleep(abs(np.random.normal(.1,.06)))
        dirty_herbClickPoint = dirty_herb_action.click(dirty_herbScreen,speed=.5, wait=0)

    ''' #this part is redundant -- you check again later
    #10.5 check the herbs are clean now 
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    dirty_herbWindowAllPoints = dirty_herb_vision.find(screenshot, DETECTION_THRESHOLD,debug_mode= 'rectangles', return_mode = 'allPoints')
    clean_herbWindowAllPoints = clean_herb_vision.find(screenshot, DETECTION_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints')    
    print('num clean herbs = %s/28 | num dirty herbs = %s/0' % (len(clean_herbWindowAllPoints), len(dirty_herbWindowAllPoints)))
    '''
    #11 debugging data
    loop_time = round(time.time() - loop_time, 2)
    runTime = round(time.time() - startTime, 2)
    numLoops = numLoops +1
    print('cycle complete. loop_time = %s | runTime = %s | numLoops = %s' % (loop_time, runTime, numLoops))
    loop_time = time.time() #resetting loop time
    
        
    #12 check if runtime elapsed
    if runTime > STOP_AFTER:
        print('completed run. final runtime was %s' % runTime)
        exit()
    '''
#I think this adds time
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    #somehow this is nessisary in order to get screen display. don't know why-- without it I get a grey screen
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()
    '''
   
    
     


