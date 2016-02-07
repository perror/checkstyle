from io import TextIOWrapper

class IterStream(TextIOWrapper):
    """
    File-like streaming iterator.
    """
    def __init__(self, generator):
        self.generator = generator
        self.iterator = iter(generator)
        self.leftover = ''

    def __iter__(self):
        return self.iterator

    def next(self):
        return self.iterator.next()

    def __next__(self):
        return self.iterator.__next__()

    def read(self, size):
        data = self.leftover
        count = len(self.leftover)
        try:
            while count < size:
                chunk = self.__next__()
                data += chunk
                count += len(chunk)
        except StopIteration:
            self.leftover = ''
            return data

        return data[:size]

    def readline(self, size):
        line = self.read(size)
        return line

    def readlines(self, size):
        return self.readline(size)

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
            line = ''
            for letter in f:
                if letter == '\n':
                    line += '\n'
                    break
                line += letter
            
            sys.stdout.write(f.filename() + ": " + str(f.filelineno()) + ": " + line)
