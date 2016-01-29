# -*- coding: utf-8

# raw_filters: Apply filters directly to the stream before lexing it.
# First prototype: filter_tabs

import sys

from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.c_cpp import CLexer
from pygments.lexers.make import MakefileLexer
from pygments.lexers.markup import TexLexer
from pygments.lexers.shell import BashLexer

#from pygments.filters import Filter, VisibleWhitespaceFilter

def filter_tabs(stream, tabsize=8):
    for line in stream:
        yield line.replace('\t', ' ' * tabsize)

def process_file(filename):
    lexer = guess_lexer_for_filename(filename, None)

    if type(lexer) is BashLexer:
        print('This is a bash file')
    elif type(lexer) is CLexer:
        print('This is a C/C++ file')
    elif type(lexer) is MakefileLexer:
        print('This is a Makefile')
    elif type(lexer) is TexLexer:
        print('This is a LaTeX file')

    lineno = 1
    with open(filename, 'r') as f:
        for line in filter_tabs(f):
            for i, t, v in lexer.get_tokens_unprocessed(line):
                print(lineno, i, t, "'" + v + "'")
            lineno = lineno + 1

def main(args):
    import argparse, os

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='file to tokenize with pygments')

    args = parser.parse_args()

    for file in args.file:
        if os.path.isfile(file):
            print('Processing ' + file)
            process_file(file)
            print('')
        else:
            sys.stderr.write("tokenize: error: cannot read '" + file + "'\n")
                          
if __name__ == "__main__":
    sys.exit(main(sys.argv))

