# Cup Pong

## Test Script

Run the test script from Python 3:

    python3 i2ctest.py

To run the file with `pipenv`:
    pipenv install
    pipenv run python i2ctest.py

To see which i2c lines have connections:

    i2cdetect -y 1

To read a single byte from address 0x60 of the i2c bus:

    i2cget -y -a 1 0x60

## Notes

The i2c baud rate has a huge impact on the reliability of transmission. To edit the baud rate, open the config file:

    sudo nano /boot/config.txt

The most effective value is 

    dtparam=i2c_arm=on
    dtparam=i2c_arm_baudrate=40000
    dtparam=i2s=on

Then reboot:

    sudo reboot