# v20210223
import time


_MCRD = 2.7
frenzy_skill = ["2", [5.4]]
break_armor_skill = ["3", [2.6], [1.35]]

MACRO_KEYS = ["1", _MCRD, "z", 0, break_armor_skill, "1", _MCRD, frenzy_skill, "1", break_armor_skill, 0, "z" "1", _MCRD, "1", "", "1", "", "1", "", "1", "", "1", ""]


######################################################################################################

# number type (integer/float) -- delay and set delay time delay between next keys
# string type keys should be press
# array  type: ['key_to_press_(only one key)', array_of_commands_while_key_pressed, array_of_commands_after_key_release]
# typle  type: mouse click, use relative position (mouse_button_number, x, y). x and y are not required and x = y = 0 by default
#
# example: MACRO_KEYS = [2.7, "1", "2", 1, "z", ""]
# set delay between keys 2.7 seconds and wait 2.7 seconds, push key 1, delay, push key 2, delay, set delay between keys 1 second and delay, push key z, delay, empty key(no key press) but wait 1 second. Restart cycle
#
# complex example:
# _MCRD = 2.7 #magic cast recovery delay
# frenzy_skill = ["2", [5.4]]
# break_armor_skill = ["3", [2.6], [1.35]]
# MACRO_KEYS = ["1", _MCRD, "z", 0, break_armor_skill, "1", _MCRD, frenzy_skill, "1", break_armor_skill, 0, "z" "1", _MCRD, "1", "", "1", "", "1", "", "1", "", "1", ""]
# result: [send_keys:100] 1 [send_keys:2753] z [push_key:2703] 33333333333333333333333333333333333333333333333333333333333333333333333 [release_key:2602] 3 [send_keys:1352] 1 [push_key:2702] 222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222 [release_key:5402]  [send_keys:2700] 1 [push_key:2701] 33333333333333333333333333333333333333333333333333333333333333333333333 [release_key:2602]  [send_keys:4054] z1 [send_keys:2701] 1 [send_keys:2703]  [send_keys:2701] 1 [send_keys:2703]  [send_keys:2700] 1 [send_keys:2702]  [send_keys:2701] 1 [send_keys:2703]  [send_keys:2702] 1 [send_keys:2703]

######################################################################################################

class Clicker:
    stop_key = '<escape>'           # key to break macros '<escape>'
    stop_key_modifiers = []         # modifier key array to break macros ['<ctrl>','<shift>']
    max_work_time = 12 * 60 * 60    # maximum work time limit in seconds
    delay_before_script_run = 0.1   # delay before script run in seconds
    
    max_cycle_count = 1000          # max cycles limit count

    debug_mode = False
    
    ############################################################################################
    break_flag = False
    debug_mode_time = time.time()
    def main_process(self, keys, max_cycle_count):
        
        delay = 0.05     # default delay between keys
        i = 0            # limit cycles counter 

        def write_debug_time(msg = ''):
            if self.debug_mode:
                t = round((time.time() - self.debug_mode_time) * 1000)
                keyboard.send_keys(' [' + msg + ':' + str(t) + '] ')
                self.debug_mode_time = time.time()        
        
        def press_keys(key):
            write_debug_time('send_keys')
            if key != "":
                keyboard.send_keys(key)
                    
        while i < max_cycle_count:
            for key in keys:
                
                if type(key) == int or type(key) == float:
                    delay = key

                if self.break_flag:
                    break
                
                elif type(key) == str:
                    press_keys(key)

                elif type(key) is tuple and len(key) == 3:
                    if len(key) == 1:
                        mouse.click_relative_self(0, 0, key[0])
                    elif len(key) == 1:
                        mouse.click_relative_self(key[1], 0, key[0])
                    elif len(key) == 1:
                        mouse.click_relative_self(key[1], key[2], key[0])

                elif type(key) is list:
                    if len(key) >= 1:
                        if (len(key[0]) == 1):
                            write_debug_time('push_key')
                            keyboard.press_key(key[0])
                            keyboard.send_keys(key[0])

                        if len(key) >= 2 and type(key[1]) is list:
                            self.main_process(key[1], 1)
                        
                        write_debug_time('release_key')
                        keyboard.release_key(key[0])
                        
                    if len(key) >= 3 and type(key[2]) is list:
                        self.main_process(key[2], 1)
                
                time.sleep(delay)

            i = i + 1

            if self.break_flag:
                break
            
    def run(self, macro_commands):
        time.sleep(self.delay_before_script_run)   
        thr = threading.Thread(target = self.main_process, args = [macro_commands, self.max_cycle_count])
        thr.start()
        
        keyboard.wait_for_keypress(self.stop_key, self.stop_key_modifiers, self.max_work_time)
        self.break_flag = True
        thr.join()
        
clicker = Clicker()
clicker.run(MACRO_KEYS)
