import logging
import ctypes
from retry import retry

logger = logging.getLogger(__name__)

class DataPacket(ctypes.Structure):
    _fields_ = [("header", ctypes.c_uint8),
                ("count", ctypes.c_uint8),
                ("adc", ctypes.c_uint16),
                ("ball_detected", ctypes.c_uint8)]

class Colour(ctypes.Structure):
    _fields_ = [("red", ctypes.c_uint8),
                ("green", ctypes.c_uint8),
                ("blue", ctypes.c_uint8)]

    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

class ArgColour(Colour):
    def __init__(self, value):
        self.red = value.red
        self.green = value.green
        self.blue = value.blue
        super(ArgColour, self).__init__()

class Command(object):
    '''A command that can be sent to cup firmware.
    '''
    def __init__(self, code, name, *args):
        self.name = name
        self.args = args
        fields = args

        class CommandStruct(ctypes.Structure):
            _fields_ = [('code', ctypes.c_uint8)] + list(fields)
            _pack_ = 1

            def __init__(self, *args, **kwargs):
                self.kwargs = kwargs
                super(type(self), self).__init__(**kwargs)

            def to_bytes(self):
                data = bytearray(self)
                return data

            def __str__(self):
                argvals = [str(self.kwargs[n]) for n, _ in args]
                return "%s(%s)" % (type(self).__name__, ', '.join(argvals))

        CommandStruct.__name__ = name
        self.pos_ctors = [ctor for name, ctor in args]
        self.kw_ctors = {name: ctor for name, ctor in args}
        self.code = code
        self.stype = CommandStruct

    def __call__(self, script, *args, **kwargs):
        for argval, (argname, argtype) in zip(args, self.args):
            kwargs[argname] = argval

        for k, v in kwargs.items():
            kwargs[k] = self.kw_ctors[k](v)

        cmd = self.stype(*args, **kwargs)
        cmd.code = self.code

        return cmd

    def __str__(self):
        argstrs = ["%s %s" % (argtype.__name__, name) for name, argtype in self.args]
        return "%s(%s)" % (self.name, ", ".join(argstrs))

_commands = [
    Command(0x74, "SET_COLOUR", ("colour", ArgColour)),
    Command(0x01, "SET_COLOUR_MASK", ("mask", ctypes.c_uint8), ("colour", ArgColour)),
]

class Cup(object):
    '''Object for communicating with a cup over the I2C bus.
    '''

    def __init__(self, slave_address):
        self.slave_address = slave_address
        for cmd in _commands:
            self._wrap_command(cmd)
        logger.debug('Created cup at address 0x%2x', slave_address)

    def __hash__(self):
        return self.slave_address

    def __eq__(self, other):
        return self.slave_address == other.slave_address

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return "Cup 0x%2x" % self.slave_address

    def _wrap_command(self, cmd):
        def call_cmd(bus, *args, **kwargs):
            cmdstruct = cmd(self, *args, **kwargs)
            b = cmdstruct.to_bytes()
            logger.debug('Writing %s to address 0x%2x', b, self.slave_address)
            bus.write_i2c_block_data(self.slave_address, 0, b)

        setattr(self, cmd.name, call_cmd)

    @retry(OSError, tries=3, delay=0.5, logger=logger)
    def get_status(self, bus):
        data_packet = bus.read_ctypes_struct(self.slave_address, DataPacket)
        return data_packet