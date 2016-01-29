# -*- coding: utf-8

"""Main program when called as a command line software"""

import sys

def main(args):
    """Main function of the checkstyle module"""

    # Parsing the arguments of the command line interface
    import argparse
    import os

    from checkstyle.checker import CChecker
    from checkstyle.runner import Runner

    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+',
                        help='path to the project files or directories')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')

    args = parser.parse_args()

    if args.verbosity > 0:
        print("Running checkstyle...")

    for path in args.input:
        if os.path.isfile(path) or os.path.isdir(path):
            runner = Runner(path)
            runner.register(CChecker)
            runner.run()
        else:
            sys.stderr.write("checkstyle: error: '" + path + "' does not exist!\n")
            sys.exit(1)


# Main function
if __name__ == '__main__':
    sys.exit(main(sys.argv))
