# -*- coding: utf-8

"""Class to check the style of a whole project"""

class Checker(object):
    """Abstract class to build a checker"""

    def __init__(self, files):
        self.lexer = None
        self.files = files
        self.rules = set()

    def register(self, rule):
        """Add a rule to the rule list

        @param rule: rule to add to the list

        """
        self.rules.add(rule)

    def run(self):
        """Run all the rules over the files"""
        import fileinput

        if self.lexer in self.files:
            files = fileinput.input(files=self.files[self.lexer])

            for rule in self.rules:
                #pylint: disable=not-callable
                rule.check(files, self.lexer())

class CChecker(Checker):
    """C checker class"""

    def __init__(self, files):
        from pygments.lexers.c_cpp import CLexer

        super().__init__(files)
        self.lexer = CLexer

        ### Registering rules ###

        # 80 columns' rule
        from checkstyle.rules import LineWidthRule
        self.register(LineWidthRule(80))
