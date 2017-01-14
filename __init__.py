import sys

__all__ = []

if sys.platform == 'win32':
    from winemu import StreamWrapper
    
    sys.stdout = StreamWrapper (sys.stdout)

