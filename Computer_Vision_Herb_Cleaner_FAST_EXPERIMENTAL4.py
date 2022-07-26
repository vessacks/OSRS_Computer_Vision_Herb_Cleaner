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
import breakRoller


# initialize the WindowCapture class
wincap = WindowCapture('Runelite - Vessacks')


# initialize the Vision class
clean_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\clean_herb.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
dirty_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_herb.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
dirty_bank_herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\dirty_bank_herb.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
in_bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\in_bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_x_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\HerbCleaner\\image library\\bank_x.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)

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


BANK_THRESHOLD = .6
IN_BANK_THRESHOLD = .8
CLEAN_HERB_THRESHOLD = .8
DIRTY_BANK_HERB_THRESHOLD = .8
BANK_X_THRESHOLD = .8
DIRTY_HERB_THRESHOLD = .8

SPEED = np.random.normal(.6, .03)

while True:

    #pause
    time.sleep(np.random.normal(.5,.07))

    #1 open bank
    #take a screenshot
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    # get an updated image of the game and look for object of interest
    all_bank_window, best_bank_window, bank_confidence = bank_vision.find(screenshot, BANK_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    #check it found bank
    if bank_confidence < BANK_THRESHOLD:
        print('best_bank_window confidence = %s | BANK_THRESHOLD = %s | exiting...' %(bank_confidence, BANK_THRESHOLD))
        exit()
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()    

    #once it's found the object, translate to screen coords and click
    bank_screen_point = wincap.get_screen_position(best_bank_window)
    bankClickPoint = bank_action.click(bank_screen_point,speed = SPEED)
    print('num banks found = %s/1 | confidence best bank = %s | screencoords best bank=  %s' % (len(all_bank_window), bank_confidence, best_bank_window))


    #2 wait for it to be in the bank
    in_bank_confidence = [0,0]
    search_start = time.time()
    search_time = 0

    while in_bank_confidence[1] < IN_BANK_THRESHOLD:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        in_bank_confidence = in_bank_vision.find(screenshot, IN_BANK_THRESHOLD, return_mode = 'confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()    
        search_time = time.time() - search_start
        
        if search_time > 25:
            print('search_time %s exceeds threshold 25s. giving up...')
            exit()
        
        if search_time > 3:
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            bank_confidence = bank_vision.find(screenshot, threshold = BANK_THRESHOLD, return_mode= 'confidence')

            bank_screenPoint = wincap.get_screen_position(bank_confidence[0])
            bank_clickPoint = bank_action.click(bank_screenPoint, speed = SPEED)
            sleepytime = 5 + abs(np.random.normal(0,1))
            print('search time %s | threshold = 2 | attempted reclick of bank entrance w. confidence %s | waiting %ss' %(search_time, bank_confidence[1], sleepytime))
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()                 
            time.sleep(5 + abs(np.random.normal(0,1)))
               
                

    #2.1 we only get here once it's in the bank


  
    #3 find clean herbs
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_clean_herb_window, best_clean_herb_window, clean_herb_confidence = clean_herb_vision.find(screenshot, CLEAN_HERB_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if clean_herb_confidence < CLEAN_HERB_THRESHOLD:
        print('clean_herb confidence = %s | CLEAN_HERB_THRESHOLD = %s | exiting...' %(clean_herb_confidence, CLEAN_HERB_THRESHOLD))
        exit()
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit() 

    #dump clean herbs
    clean_herb_screen = wincap.get_screen_position(best_clean_herb_window)
    clean_herb_click_point = clean_herb_action.click(clean_herb_screen, speed = SPEED)
    print('num clean herbs = %s/28 | confidence best herb = %s | screencoords best herb=  %s' % (len(all_clean_herb_window), clean_herb_confidence, clean_herb_click_point))

    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #4 find dirty herbs
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_dirty_bank_herb_window, best_dirty_bank_herb_window, dirty_bank_herb_confidence = dirty_bank_herb_vision.find(screenshot, DIRTY_BANK_HERB_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if dirty_bank_herb_confidence < DIRTY_BANK_HERB_THRESHOLD:
        print('dirty_bank_herb confidence = %s | DIRTY_BANK_HERB_THRESHOLD = %s | exiting...' %(dirty_bank_herb_confidence, DIRTY_BANK_HERB_THRESHOLD))
        exit()
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit() 

    #5 click dirty herb in bank
    dirty_bank_herb_screen = wincap.get_screen_position(best_dirty_bank_herb_window)
    dirty_bank_herb_click_point = dirty_bank_herb_action.click(dirty_bank_herb_screen, speed = SPEED)
    print('num dirty_bank_herbs = %s/1 | confidence best herb = %s | screencoords best herb=  %s' % (len(all_dirty_bank_herb_window), dirty_bank_herb_confidence, dirty_bank_herb_click_point))

    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #6 find bank exit
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_bank_x_window, best_bank_x_window, bank_x_confidence = bank_x_vision.find(screenshot, BANK_X_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if bank_x_confidence < BANK_X_THRESHOLD:
        print('bank_x confidence = %s | BANK_X_THRESHOLD = %s | exiting...' %(bank_x_confidence, BANK_X_THRESHOLD))
        exit()
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit() 


    #7 click bank exit
    bank_x_screen = wincap.get_screen_position(best_bank_x_window)
    bank_x_click_point = bank_x_action.click(bank_x_screen, speed = SPEED)
    print('num bank_x = %s/1 | confidence best bank_x = %s | screencoords best bank_x =  %s' % (len(all_bank_x_window), bank_x_confidence, bank_x_click_point))

    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #8 check you're outside the bank by checking for bank entrance
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_bank_window, best_bank_window, bank_confidence = bank_vision.find(screenshot, BANK_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if bank_confidence < BANK_THRESHOLD:
        print('bankWindow confidence = %s | BANK_THRESHOLD = %s | exiting...' %(bank_confidence, BANK_THRESHOLD))
        exit()
    else:
        print('num bank %s/1 | confidence best bank %s ' % (len(all_bank_window), bank_confidence))
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()    
    

    #pause
    time.sleep(abs(np.random.normal(.6,.07)))

    #9 find dirty herb in inventory
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_dirty_herb_window, best_dirty_herb_window, dirty_herb_confidence = dirty_herb_vision.find(screenshot, DIRTY_HERB_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if dirty_herb_confidence < DIRTY_HERB_THRESHOLD:
        print('dirty_herb_window confidence = %s | DIRTY_HERB_THRESHOLD = %s | exiting...' %(dirty_herb_confidence, DIRTY_HERB_THRESHOLD))
        exit()
    else:
        print('num bank %s/1 | confidence best bank %s ' % (len(all_dirty_herb_window), dirty_herb_confidence))
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()    
   
    #10 click dirty herb in inventory
    for herb in all_dirty_herb_window:
        dirty_herb_screen = wincap.get_screen_position(herb)
        time.sleep(abs(np.random.normal(.1,.06)))
        dirty_herb_click_point = dirty_herb_action.click(dirty_herb_screen,speed = SPEED)


    #10.5 check the herbs are clean now 
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_dirty_herb_window = dirty_herb_vision.find(screenshot, DIRTY_HERB_THRESHOLD,debug_mode= 'rectangles', return_mode = 'allPoints')
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()    
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_clean_herb_window = clean_herb_vision.find(screenshot, CLEAN_HERB_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints')
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()       
    print('num clean herbs = %s/28 | num dirty herbs = %s/0' % (len(all_clean_herb_window), len(all_dirty_herb_window)))
    
    #breakroll
    breakRoller.breakRoller(odds = 80)
    
    #11 debugging data
    loop_time = round(time.time() - loop_time, 2)
    runTime = round(time.time() - startTime, 2)
    numLoops =+ 1
    print('cycle complete. loop_time = %s | runTime = %s | numLoops = %s' % (loop_time, runTime, numLoops))
    loop_time = time.time() #resetting loop time
    
        
    #12 check if runtime elapsed
    if runTime > STOP_AFTER:
        print('completed run. final runtime was %s' % runTime)
        exit()
    


'''
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    #somehow this is nessisary in order to get screen display. don't know why-- without it I get a grey screen
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()
'''
   
    
     


