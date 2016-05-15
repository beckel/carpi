from smbus import SMBus
from time import sleep
from ctypes import c_short

class TemperaturePressure:

    address = 0x77
    oversampling = 3 # 0..3
    
    def __init__(self):

        # 0 for R-Pi Rev. 1, 1 for Rev. 2
        self.bus = SMBus(1)
        
        # Read whole calibration EEPROM data
        cal = self.bus.read_i2c_block_data(self.address, 0xAA, 22)
        
        # Convert byte data to word values
        self.ac1 = get_short(cal, 0)
        self.ac2 = get_short(cal, 2)
        self.ac3 = get_short(cal, 4)
        self.ac4 = get_ushort(cal, 6)
        self.ac5 = get_ushort(cal, 8)
        self.ac6 = get_ushort(cal, 10)
        self.b1 = get_short(cal, 12)
        self.b2 = get_short(cal, 14)
        self.mb = get_short(cal, 16)
        self.mc = get_short(cal, 18)
        self.md = get_short(cal, 20)
        
        return

    def read(self):
        
        # temperature conversion
        self.bus.write_byte_data(self.address, 0xF4, 0x2E)
        sleep(0.005)
        (msb, lsb) = self.bus.read_i2c_block_data(self.address, 0xF6, 2)
        ut = (msb << 8) + lsb
        
        # pressure conversion
        self.bus.write_byte_data(self.address, 0xF4, 0x34 + (self.oversampling << 6))
        sleep(0.04)
        (msb, lsb, xsb) = self.bus.read_i2c_block_data(self.address, 0xF6, 3)
        up = ((msb << 16) + (lsb << 8) + xsb) >> (8 - self.oversampling)
        
        # calculate temperature
        x1 = ((ut - self.ac6) * self.ac5) >> 15
        x2 = (self.mc << 11) / (x1 + self.md)
        b5 = x1 + x2 
        t = (b5 + 8) >> 4
        
        # calculate pressure
        b6 = b5 - 4000
        b62 = b6 * b6 >> 12
        x1 = (self.b2 * b62) >> 11
        x2 = self.ac2 * b6 >> 11
        x3 = x1 + x2
        b3 = (((self.ac1 * 4 + x3) << self.oversampling) + 2) >> 2
        x1 = self.ac3 * b6 >> 13
        x2 = (self.b1 * b62) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self.ac4 * (x3 + 32768)) >> 15
        b7 = (up - b3) * (50000 >> self.oversampling)
        p = (b7 * 2) / b4
        x1 = (p >> 8) * (p >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        p = p + ((x1 + x2 + 3791) >> 4)
        
        return (t/10.0, p / 100)

        

# return two bytes from data as a signed 16-bit value
def get_short(data, index):
    return c_short((data[index] << 8) + data[index + 1]).value

# return two bytes from data as an unsigned 16-bit value
def get_ushort(data, index):
    return (data[index] << 8) + data[index + 1]
