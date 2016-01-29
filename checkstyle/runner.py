# -*- coding: utf-8

"""Discover the projects files and run the registered checkers on it"""

class Runner(object):
    """Class to run the checkers on the project files"""

    def __init__(self, path):
        self.files = dict()
        self.checkers = None
        self.discover(path)

    def discover(self, path):
        """Discover all files of the project and group them by categories

        @param path: Path to the project or to the file to check.

        """
        import fnmatch
        import os

        from pygments.lexers import guess_lexer_for_filename
        from pygments.util import ClassNotFound

        files = set()
        if os.path.isfile(path):
            files.add(path)
        else:
            for root, _, filenames in os.walk(path):
                files |= set([os.path.join(root, file) for file in filenames])

        for file in files:
            try:
                lexer = guess_lexer_for_filename(file, None)
                #pylint: disable=unidiomatic-typecheck
                self.files.setdefault(type(lexer), set()).add(file)
            except ClassNotFound:
                pass

    def register(self, checker):
        """Add a checker to the runner list

        @param checker: Checker to add to the runner.

        """
        if self.checkers is None:
            self.checkers = [checker(self.files)]
        else:
            self.checkers.append(checker(self.files))

    def run(self):
        """Start all the checkers on the files of the project"""
        from checkstyle.checker import Checker

        for checker in self.checkers:
            checker.run()

