# -*- coding: utf-8

"""Check coding style enforcement in students' code.

A collection of functions and classes designed to check automatically
that the coding style is observed in a student programming project.

"""
from checkstyle.checker import Checker
from checkstyle.rules import Rule
from checkstyle.runner import Runner

__version__ = '0.0.1'
__author__ = ("Emmanuel Fleury <emmanuel.fleury@u-bordeaux.fr>")

__all__ = ['Checker', 'Rule', 'Runner']
