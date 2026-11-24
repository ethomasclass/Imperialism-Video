# Run before every scene script (run_all.py passes it first): text files open as UTF-8 by default, as on Mac and Linux.
# Windows Python otherwise reads text in the old ANSI code page, and the scripts contain characters like the ʻokina.
import builtins

_open = builtins.open


def _utf8_open(file, mode='r', buffering=-1, encoding=None, *args, **kw):
    if 'b' not in mode and encoding is None:
        encoding = 'utf-8'
    return _open(file, mode, buffering, encoding, *args, **kw)


builtins.open = _utf8_open
