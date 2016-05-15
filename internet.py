import sys
import os
import time

class Internet:
    

    def __init__(self):
        self.status = "off"
        return
        

    def switch_on(self):
        if self.status == "on":
            return
        print("Starting Internet connection: USB Modeswitch")
        os.system("sudo usb_modeswitch -I -W -c /etc/usb_modeswitch.d/12d1\:14d1 &")
        time.sleep(3)
        print("Done running USB Modeswitch")
        
        print("Starting Internet connection: WVDial")
        os.system("sudo wvdial &")
        time.sleep(3)
        print("Done running WVDial")
        
        print("Starting Internet connection: NAT")
        os.system("sudo iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE")
        time.sleep(1)
        print("Done setting NAT rule")
        
        sys.stdout.flush()
        
        self.status = "on"
        
        return
        

    def switch_off(self):
        if self.status == "off":
            return
        self.status = "off"
        print("Stopping Internet connection")
        os.system("sudo killall wvdial")
        return
        

    def get_state(self):
        if self.status == "off":
            return False;
        else:
            return True;
        return;


    def get_state_ping_successful(self):
        response = os.system("sudo ping -c 1 -W 1 www.heise.de")
        if response == 0:
            print("Ping to www.heise.de successful")
            return True
        else:
            print("Ping not successful")
            return False
