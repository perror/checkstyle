# -*- coding: utf-8

"""Describes the coding style rules and how to check it."""

from checkstyle.utils import error

from pygments.token import *

class Rule(object):
    """Abstract class to check a precise coding style rule."""

    def __init__(self):
        pass

    def name(self):
        """Return the name of the rule."""
        pass

    def description(self):
        """Return the full description of the rule."""
        pass

    def check(self, files, lexer, line_filter=None):
        """Check the files against the rule and output errors on stdout.

        @param files: list of all the files of the same kind
        @param lexer: the tokenizer for the files
        @param filter: filter function to apply before tokenizer
        """
        pass

class LineWidthRule(Rule):
    """Check each line width to be within correct boundaries."""

    def __init__(self, width=80):
        super().__init__()
        self.width = width

    def name(self):
        return "Maximum Line Width Rule"

    def description(self):
        return "Check if each line of code is below %i characters." % self.width

    def check(self, files, lexer, line_filter=None):
        """Check line width."""
        for line in files:
            if line_filter is not None:
                line = line_filter(line)
            for column, _, value in lexer.get_tokens_unprocessed(line):
                if value == '\n' and column > self.width:
                    error("line too long (>%i columns)" % self.width, files)

class SpacesAroundOps(Rule):
    """Check if some operators are between spaces."""

    def name(self):
        return "Spaces Around Operators Rule"

    def description(self):
        return "Check if there are spaces around some operators."

    def check(self, files, lexer, line_filter=None):
        """Check if there are spaces around operators."""
        for line in files:
            if line_filter is not None:
                line = line_filter(line)
            ignore_next = 0
            for pos, token_type, value in lexer.get_tokens_unprocessed(line):
                if ignore_next > 0:
                    ignore_next -= 1
                    continue

                if token_type is Token.Operator:
                    # Filtering special cases '++', '--', '==', '&&', '||'
                    if value in frozenset(['+', '-', '=', '&', '|']):
                        # Check right character
                        if (pos < len(line) - 1) and (line[pos + 1] == value):
                            ignore_next = 1
                            continue

                    # Filtering special cases '+=', '-=', '*=', ...
                    if value in frozenset(['+', '-', '*', '/', '^', '|', '&', '!']):
                        # Check if right char is '='
                        if (pos < len(line) - 1) and (line[pos + 1] == '='):
                            ignore_next = 1
                            continue

                    # Filtering out special operators
                    if value in frozenset([':', '!']):
                        continue

                    # Filtering special cases '&<name>'
                    if value == '&':
                        if (pos < len(line) - 1) and line[pos + 1].isalpha():
                            ignore_next = 1
                            continue

                    # Checking whitespaces around
                    result = True
                    # Check if left char is a space
                    if (pos > 0):
                        if not (line[pos - 1].isspace()):
                            result = False
                    # Check if right char is space
                    if (pos < len(line) - 1):
                        if not (line[pos - 1].isspace()):
                            result = False
                    if not result:
                        error("Missing spaces around '%s'" % value, files)
        
