# -*- coding: utf-8

"""Class to check the style of a whole project."""

class Checker(object):
    """Abstract class to build a checker."""

    def __init__(self, files):
        from pygments.lexer import Lexer

        self.lexer = Lexer
        self.files = files
        self.rules = set()

    def register(self, rule):
        """Add a rule to the rule list.

        @param rule: rule to add to the list

        """
        self.rules.add(rule)

    def run(self):
        """Run all the rules over the files."""
        import fileinput

        if self.lexer in self.files:
            for rule in self.rules:
                files = fileinput.input(files=self.files[self.lexer])
                #pylint: disable=not-callable
                rule.check(files, self.lexer(), line_filter=self.line_filter)

def C_filter(line):
    """Internal filter to change tabulation into 8 whitespaces."""
    return line.replace('\t', ' ' * 8)

class CChecker(Checker):
    """C checker class."""

    def __init__(self, files):
        from pygments.lexers.c_cpp import CLexer

        super().__init__(files)
        self.lexer = CLexer
        self.line_filter = C_filter

        ### Registering rules ###
        from checkstyle.rules import LineWidthRule, SpacesAroundOps
        # 80 columns' rule
        self.register(LineWidthRule(80))
        # Spaces around Operators
        self.register(SpacesAroundOps())
