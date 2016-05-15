import os
import time
import threading
import sys

class Alarm:
    
    def __init__(self, imu):
        self.imu = imu
        self.status = "off"
        return
        
    def switch_on(self):
        if self.status == "on":
            return
        self.status = "on"
        self.thread_stop_event = threading.Event()
        thread = threading.Thread(target=self.run, args=(1, self.thread_stop_event))
        thread.daemon = True
        thread.start()
        print("Starting alarm system")
        return
        
    def switch_off(self):
        if self.status == "off":
            return
        self.status = "off"
        self.thread_stop_event.set()
        print("Stopping alarm system")
        return
        
    def run(self, arg1, thread_stop_event):
        while(not thread_stop_event.is_set()):
            time.sleep(1)
            print("Running")
            sys.stdout.flush()
            time.sleep(0.05)
            val = self.imu.get_acceleration_norm()
            if (val > 1.02):
                print('Alarm detected: ' + str(val))
                
                # write to database and send event!
            
            
        return
    
    def get_state(self):
        if self.status == "off":
            return False;
        else:
            return True;
        return;
        