import logging
import ctypes

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Colour(ctypes.Structure):
    _fields_ = [("red", ctypes.c_ubyte),
                ("green", ctypes.c_ubyte),
                ("blue", ctypes.c_ubyte)]

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
    Command(0x00, "SET_COLOUR", ("colour", ArgColour)),
]

class Cup(object):
    '''Object for communicating with a cup over the I2C bus.
    '''

    def __init__(self, slave_address):
        self.slave_address = slave_address
        for cmd in _commands:
            self._wrap_command(cmd)
        logger.debug('Created cup at address 0x%2x', slave_address)

    def _wrap_command(self, cmd):
        def call_cmd(bus, *args, **kwargs):
            cmdstruct = cmd(self, *args, **kwargs)
            b = cmdstruct.to_bytes()
            bus.write_i2c_block_data(self.slave_address, 0, b)

        setattr(self, cmd.name, call_cmd)

    def check_ball_detected(self, bus):
        b = bus.read_byte_data(self.slave_address, 0)
        print (b)
        if b != 0:
            logger.debug('Ball detected on cup at address 0x%2x', self.slave_address)
            return True
        return False
