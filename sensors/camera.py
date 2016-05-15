import os
import time

class Camera:
    
    def __init__(self):
        # self.user = user
        # self.key = key
        
        self.status = "off"
        return
        
    def switch_on(self):
        if self.status == "on":
            return
        os.system("sudo /etc/init.d/mjpgstreamer start")
        self.status = "on"
        return
        
        
    def switch_off(self):
        if self.status == "off":
            return
        os.system("sudo /etc/init.d/mjpgstreamer stop")    
        self.status = "off"
        return
        
    def get_state(self):
        if self.status == "off":
            return False;
        else:
            return True;
        return;
        
        
    