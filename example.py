from io import TextIOWrapper

import fileinput
import sys

class IterStream(TextIOWrapper):
    """
    File-like streaming iterator.
    """
    def __init__(self, generator):
        self._buffer = ''
        self.generator = generator
        self.iterator = iter(generator)
        self._next = self.iterator.__next__

    def __iter__(self):
        return self.iterator

    def __next__(self):
        if self._buffer:
            _next_char = self._buffer[0]
            self._buffer = self._buffer[1:]
        else:
            _next_char = self.iterator.__next__()
        return _next_char

    def read(self, size=None):
        if size is None:
            size = -1
        # Read and store in result.
        result = ''
        if size < 0:
            # Read everything.
            while True:
                previous = len(result)
                result += self._next()
                if previous == len(result):
                    break
        else:
            for _ in range(size):
                previous = len(result)
                result += self._next()
                if previous == len(result):
                    break
        return result

    def readline(self):
        _line = ''
        while True:
            # Initializing the line and previous_line
            _previous = len(_line)
            _line += self._next()

            # Check EOF
            if len(_line) == _previous:
                break

            # Check for EOL
            # We are looking for '\n', '\r' or '\r\n' new line characters.
            _nlpos = _line.find('\n')
            _crpos = _line.find('\r')

            if _nlpos != -1:
                break
            elif _crpos < len(_line):
                if _nlpos == _crpos + 1:
                    break
                else:
                    self._buffer += _line[_crpos+1:]
                    _line = _line[:_crpos]
                    break
        return _line

    def readlines(self):
        return self.readline()

    def close(self):
        pass

def streamfilter(filterfunc):
    def stream(iostream):
        return IterStream(filterfunc(iostream))
    return stream

@streamfilter
def tab_filter(stream):
    for _line in stream:
        yield _line.replace('\t', ' ' * 8)

def fileinput_hook(filename, mode):
    return tab_filter(open(filename, mode))

if __name__ == "__main__":
    with fileinput.input(files=('Makefile', 'README', 'requirements.txt'), openhook=fileinput_hook) as f:
        while not f.isfirstline():
            for line in f:
                sys.stdout.write(f.filename() + ": " + str(f.filelineno()) + ": " + line)
            f.nextfile()
