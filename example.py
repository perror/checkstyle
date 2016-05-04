from io import TextIOWrapper

class IterStream(TextIOWrapper):
    """
    File-like streaming iterator.
    """
    def __init__(self, generator):
        self._buffer = ''
        self.generator = generator
        self.iterator = iter(generator)
        self.leftover = ''

    def __iter__(self):
        return self.iterator

    def next(self):
        return self.iterator.next()

    def __next__(self):
        if self._buffer:
            next = self._buffer[0]
            self._buffer = self._buffer[1:]
        else:
            next = self.iterator.__next__()

        return next

    def readline(self):
        line = ''
        while True:
            # Initializing the line and previous_line
            previous_size = len(line)
            line += self.__next__()

            # Check EOF
            if len(line) == previous_size:
                break

            # Check for EOL
            # We are looking for '\n', '\r' or '\r\n' new line characters.
            nlpos = line.find('\n')
            crpos = line.find('\r')

            if nlpos != -1:
                break
            elif crpos < len(line):
                if nlpos == crpos + 1:
                    break
                else:
                    self._buffer += line[crpos+1:]
                    line = line[:crpos]
                    break
        return line

    def readlines(self):
        return self.readline()

    def close(self):
        pass


def streamfilter(filter):
    def stream(iostream):
        return IterStream(filter(iostream))
    return stream

@streamfilter
def tab_filter(stream):
    for line in stream:
        yield line.replace ('\t', ' ' * 8)

def fileinput_hook(filename, mode):
    return tab_filter(open(filename, mode))

if __name__ == "__main__":
    import fileinput
    import sys

    with fileinput.input(files='Makefile', openhook=fileinput_hook) as f:
        for line in f:
            sys.stdout.write(f.filename() + ": " + str(f.filelineno()) + ": " + line)
