import logging
from smbuswrapper import SMBusWrapper as SMBus
from retry import retry
import time
import threading
import struct

from cup import Cup, Colour

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SLAVE_ADDRESS = 0x60
I2C_BUS = 1

@retry(OSError, tries=3, delay=1, logger=logger)
def print_i2c_data(cups):
    while (True):
        time.sleep(0.5)
        with SMBus(I2C_BUS) as bus:
            #header = 0
            #while header != 0x12:
            #    header = bus.read_byte(SLAVE_ADDRESS)
            #count, adc, ball_detected = bus._read_bytes(SLAVE_ADDRESS, '<BHB')
            
            for cup in cups:
                cup_status = cup.get_status(bus)

                if cup_status.header != 0x12:
                    print ('ERR')
                    continue

                print ('#%d -> ADC = %d %s' % (cup_status.count, cup_status.adc, 'YES' if cup_status.ball_detected == 1 else cup_status.ball_detected))
            

if __name__ == '__main__':

    cup0 = Cup(SLAVE_ADDRESS)
    cups = [cup0]

    ball_detection_thread = threading.Thread(target=print_i2c_data, args=(cups,), daemon=True)
    ball_detection_thread.start()

    a = input('Press enter to quit...')
