# -*- coding: utf-8

"""Describes the coding style rules and how to check it."""

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
        return "Check if each line of code is below " + str(self.width) + " characters."

    def check(self, files, lexer, line_filter=None):
        """Check line width."""
        for line in files:
            if line_filter is not None:
                line = line_filter(line)
            for column, _, value in lexer.get_tokens_unprocessed(line):
                if value == '\n' and column > self.width:
                    from checkstyle.utils import error
                    error("line too long (>%i columns)" % self.width, files)
