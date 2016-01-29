# -*- coding: utf-8

"""Utility functions for this module"""

def error(msg, files):
    """Handling error messages for each broken rule"""
    import sys
    prefix = "checkstyle: error: "
    text = prefix + "%s: %i: %s\n" % (files.filename(), files.filelineno(), msg)
    sys.stderr.write(text)
