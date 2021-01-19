# v20210119
import time

# MB? = mouse.click_relative_self(x, y, button number). Can use at keyboard key position
MB1 = [0, 0, 1]
MB2 = [0, 0, 2]

# number type (integer/float) -- time to delay between keys
# string type keys shoult be press
# example MACRO_KEYS = [2.7, "1", "2", 1, "z", ""]
# set delay between keys 2.7 seconds, push key 1, delay, push key 2, delay, set delay between keys 1 second, push key z, delay, empty key(no key press) delay, restart cycle

MACRO_KEYS = [2.7, "1", "2", "1", "3", "3", "6", "1", "z", "1", ""]

# configure
STOP_KEY = '<escape>'           # key to break macros
MAX_CYCLE_COUNT = 10000         # max cycles limit count
MAX_WORK_TIME = 12 * 60 * 60    # maximum work time limit in seconds
DELAY_BEFORE_SCRIPT_RUN = 0.5   # delay before script run in seconds

############################################################################################
break_flag = False
def main_process():
    delay = 0.1     # default delay between keys
    i = 0           # limit cycles counter 
    while i < MAX_CYCLE_COUNT:
        for key in MACRO_KEYS:
            if type(key) == int or type(key) == float:
                delay = key
                continue

            elif key == MB1 or key == MB2:
                mouse.click_relative_self(key[0], key[1], key[2]);
            
            elif type(key) == str:
                if key != "":
                    keyboard.send_keys(key)
                    
            time.sleep(delay)
            
            if break_flag:
                break         
            
        i = i + 1

        if break_flag:
            break
   
time.sleep(DELAY_BEFORE_SCRIPT_RUN)   
thr = threading.Thread(target = main_process, args = ())
thr.start()

keyboard.wait_for_keypress(STOP_KEY, [], MAX_WORK_TIME)
break_flag = True
thr.join()
