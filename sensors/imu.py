from smbus import SMBus
from time import sleep
import math
import datetime
    
from LSM9DS0 import *

class IMU:

    def __init__(self):

        # 0 for R-Pi Rev. 1, 1 for Rev. 2
        self.bus = SMBus(1)

        #initialise the accelerometer
        self.writeACC(CTRL_REG1_XM, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
        self.writeACC(CTRL_REG2_XM, 0b00100000) #+/- 16G full scale

    def writeACC(self, register,value):
        self.bus.write_byte_data(ACC_ADDRESS , register, value)
        return -1
        
    def readACCx(self):
        acc_l = self.bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
        acc_h = self.bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
    	acc_combined = (acc_l | acc_h <<8)
    	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


    def readACCy(self):
        acc_l = self.bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
        acc_h = self.bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
    	acc_combined = (acc_l | acc_h <<8)
    	return acc_combined  if acc_combined < 32768 else acc_combined - 65536

    def readACCz(self):
        acc_l = self.bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
        acc_h = self.bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
        acc_combined = (acc_l | acc_h <<8)
    	return acc_combined  if acc_combined < 32768 else acc_combined - 65536
    
    def read_simple_accelerometer(self):
        ACCx = self.readACCx()
        ACCy = self.readACCy()
        ACCz = self.readACCz()
        return (ACCx, ACCy, ACCz)
        
    def get_acceleration_norm(self):
        x = self.readACCx() * 0.732 / 1000
        y = self.readACCy() * 0.732 / 1000
        z = self.readACCz() * 0.732 / 1000
        return math.sqrt(x*x+y*y+z*z);
    