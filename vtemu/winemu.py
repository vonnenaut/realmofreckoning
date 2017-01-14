import ctypes
import re
import sys


# ctypes things
STD_INPUT_HANDLE            = ctypes.c_uint32 (-10)
STD_OUTPUT_HANDLE           = ctypes.c_uint32 (-11)
STD_ERROR_HANDLE            = ctypes.c_uint32 (-12)

INVALID_HANDLE_VALUE        = ctypes.c_ulong (-1)

FOREGROUND_BLUE             = 0x0001
FOREGROUND_GREEN            = 0x0002
FOREGROUND_RED              = 0x0004
FOREGROUND_INTENSITY        = 0x0008

BACKGROUND_BLUE             = 0x0010
BACKGROUND_GREEN            = 0x0020
BACKGROUND_RED              = 0x0040
BACKGROUND_INTENSITY        = 0x0080

COMMON_LVB_LEADING_BYTE     = 0x0100
COMMON_LVB_TRAILING_BYTE    = 0x0200
COMMON_LVB_GRID_HORIZONTAL  = 0x0400
COMMON_LVB_GRID_LVERTICAL   = 0x0800
COMMON_LVB_GRID_RVERTICAL   = 0x1000
COMMON_LVB_REVERSE_VIDEO    = 0x4000
COMMON_LVB_UNDERSCORE       = 0x8000

class COORD (ctypes.Structure):
    _fields_ = [('X', ctypes.c_int16),
                ('Y', ctypes.c_int16)]

class SMALL_RECT (ctypes.Structure):
    _fields_ = [('Left', ctypes.c_int16),
                ('Top', ctypes.c_int16),
                ('Right', ctypes.c_int16),
                ('Bottom', ctypes.c_int16)]

class CONSOLE_SCREEN_BUFFER_INFO (ctypes.Structure):
    _fields_ = [('dwSize', COORD),
                ('dwCursorPosition', COORD),
                ('wAttributes', ctypes.c_short),
                ('srWindow', SMALL_RECT),
                ('dwMaximumWindowSize', COORD)]
    _pack_ = 2

GetStdHandle = ctypes.windll.kernel32.GetStdHandle
GetStdHandle.restype  = ctypes.c_ulong
GetStdHandle.argtypes = [ctypes.c_uint32]

SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
SetConsoleTextAttribute.restype  = ctypes.c_int32
SetConsoleTextAttribute.argtypes = [ctypes.c_ulong, ctypes.c_ushort]

GetConsoleScreenBufferInfo = ctypes.windll.kernel32.GetConsoleScreenBufferInfo
GetConsoleScreenBufferInfo.restype  = ctypes.c_int32
GetConsoleScreenBufferInfo.argtypes = [ctypes.c_ulong,
        ctypes.POINTER (CONSOLE_SCREEN_BUFFER_INFO)]


class StreamWrapper (object):
    _vt100_clr = re.compile (r'(\x1b\[[^m]+m)')
    
    _fg_colours = [0,
        FOREGROUND_RED,
        FOREGROUND_GREEN,
        FOREGROUND_RED | FOREGROUND_GREEN,
        FOREGROUND_BLUE,
        FOREGROUND_BLUE | FOREGROUND_RED,
        FOREGROUND_BLUE | FOREGROUND_GREEN,
        FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
    ]
    
    _bg_colours = [0,
        BACKGROUND_RED,
        BACKGROUND_GREEN,
        BACKGROUND_RED | BACKGROUND_GREEN,
        BACKGROUND_BLUE,
        BACKGROUND_BLUE | BACKGROUND_RED,
        BACKGROUND_BLUE | BACKGROUND_GREEN,
        BACKGROUND_BLUE | BACKGROUND_GREEN | BACKGROUND_RED
    ]

    def __init__ (self, stream):
        self._stream = stream
        
        # get the console handle from the OS
        self._stdout = GetStdHandle (STD_OUTPUT_HANDLE)
        if self._stdout == INVALID_HANDLE_VALUE:
            sys.stderr.write ("Failed to obtain STDOUT handle!\n");
            sys.exit (1)
        
        # now store the default text attributes
        csbi = CONSOLE_SCREEN_BUFFER_INFO ()
        if GetConsoleScreenBufferInfo (self._stdout, ctypes.byref (csbi)) == 0:
            sys.stderr.write ("Failed to obtain console screen buffer info!\n")
            sys.exit (1)
        self._def_text_attr = csbi.wAttributes
        
        self._attrs = self._def_text_attr
    
    def __del__ (self):
        if self._stdout != INVALID_HANDLE_VALUE:
            SetConsoleTextAttribute (self._stdout, self._def_text_attr)
    
    def write (self, line):
        parts = StreamWrapper._vt100_clr.split (line)
        
        for part in parts:
            if part.startswith ('\x1b['):
                self._handle_escape (part)
            else:
                self._stream.write (part)
    
    def _handle_escape (self, sequence):
        if sequence[-1] != 'm':
            sys.stderr.write ('unsupported')
        
        attributes = sequence[2:-1].split (';')
        
        new_attrs = self._attrs
        
        bright = False
        
        # calculate the new attributes
        for attr in attributes:
            attr = int (attr)
            
            if attr == 0:
                # Reset
                new_attrs = self._def_text_attr
            elif attr == 1:
                # Bright
                bright = True
            elif attr == 2:
                # Dim
                bright = False
            elif 30 <= attr <= 37:
                # Foregroud colour
                new_attrs &= 0xfff0
                new_attrs |= StreamWrapper._fg_colours[attr % 30]
                
                if bright:
                    new_attrs |= FOREGROUND_INTENSITY
            elif 40 <= attr <= 47:
                # Background colours
                new_attrs &= 0xff0f
                new_attrs |= StreamWrapper._bg_colours[attr % 40]
                
                if bright:
                    new_attrs |= BACKGROUND_INTENSITY
        
        # update the console
        if SetConsoleTextAttribute (self._stdout, new_attrs) != 0:
            self._attrs = new_attrs

