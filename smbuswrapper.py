from smbus2 import SMBus
import struct
import ctypes

class SMBusWrapper(SMBus):
    def __init__(self, bus=None, force=False):
        super().__init__(bus, force)

    def read_ctypes_struct(self, i2c_addr, klass):
        '''Reads enough bytes to deserialize a ctypes structure
        and then deserializes the data.
        '''
        length = ctypes.sizeof(klass)
        b = self.read_i2c_block_data(i2c_addr, 0x00, length)
        obj = klass.from_buffer_copy(bytearray(b))
        return obj

    def read_struct(self, i2c_addr, fmt, force=None):
        length = struct.calcsize(fmt)

        # read the number of bytes specified by length
        bytes_read = self.read_i2c_block_data(i2c_addr, 0x00, length)

        #bytes_read = bytearray([self.read_byte(i2c_addr, force) for _ in range(length)])
        #print (', '.join('0x{:02x}'.format(x) for x in bytes_read), end=" = ")
        s = struct.unpack(fmt, bytearray(bytes_read))
        return s


    def read_uint16(self, i2c_addr, force=None):
        return self.read_struct(i2c_addr, '<H', force=force)[0]

    def read_uint32(self, i2c_addr, force=None):
        return self.read_struct(i2c_addr, '<I', force=force)[0]
