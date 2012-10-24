import pdb
import sys
import optparse

import simulator


def main(argv=None):
    """ XXXXXXXXXXXXXXXXXXXXX """
    settings = process_command_line(argv)

#    run(settings)

    return 0        # success


def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)

    # define options here:
    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')

    # define options here:
    parser.add_option(      # number of nodes to generate;
        '-n', '--numberOfNodes', dest='number_of_nodes',
        help="Word to be translated")

    parser.add_option(      # max number of cycles in the simulation;
        '-m', '--numberOfMaxCycles', dest='number_of_cycles',
        help="Word to be translated")

    parser.add_option(      # simulation plane to load;
        '-l', '--load-scenario', dest='scenario_file',
        help="Scenario to load")

    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments; '
                     '"%s" ignored.' % args)

    return settings

if __name__ == '__main__':
    main(sys.argv[1:])
