# -*- coding: utf-8

"""Class to check the style of a whole project."""

class Checker(object):
    """Abstract class to build a checker."""

    def __init__(self, files):
        from pygments.lexer import Lexer

        self.lexer = Lexer
        self.files = files
        self.rules = set()
        self.line_filter = None

    def register(self, rule):
        """Add a rule to the rule list.

        @param rule: rule to add to the list

        """
        self.rules.add(rule)

    def run(self):
        """Run all the rules over the files."""
        import fileinput

        if self.lexer in self.files:
            files = fileinput.input(files=self.files[self.lexer])
            for rule in self.rules:
                if self.line_filter is None:
                    #pylint: disable=not-callable
                    rule.check(files, self.lexer())
                else:
                    #pylint: disable=not-callable
                    rule.check(files, self.lexer(), line_filter=self.line_filter)

def tab_filter(line):
    """Internal filter to change tabulation into 8 whitespaces."""
    return line.replace('\t', ' ' * 8)

class CChecker(Checker):
    """C checker class."""

    def __init__(self, files):
        from pygments.lexers.c_cpp import CLexer

        super().__init__(files)
        self.lexer = CLexer
        self.line_filter = tab_filter

        ### Registering rules ###
        # 80 columns' rule
        from checkstyle.rules import LineWidthRule
        self.register(LineWidthRule(80))
