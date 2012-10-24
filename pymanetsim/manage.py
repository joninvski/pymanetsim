import pdb
import sys
import os

import pep8

from subprocess import Popen, PIPE

from optparse import OptionParser

from pylint import lint

file_list = [
    'messages.py',
    'events.py',
    'simulator.py',
    'job_manager.py',
    'node.py',
    'plane.py',
    'plane_builders.py',
    'configuration.py',
    'protocols/bfg/bfg.py',
    'protocols/bfg/node.py',
    'protocols/bfg/bloom.py',
    'protocols/bfg/arguments.py',
    'protocols/dsr/dsr.py',
    'protocols/dsr/node.py',
    'protocols/dsr/arguments.py',
]

def run_job_manager():
    import job_manager
    job_manager.run_all_jobs()

def draw_import_graph():
    proc = Popen(['sfood', '.', '--internal', '--internal'], stdout=PIPE)
    sfood = proc.communicate()[0]

    proc = Popen(['grep', '-v', 'unit_test'], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(sfood)
    grep_unit = proc.communicate()[0]

    proc = Popen(['grep', '-v', 'jobs'], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(grep_unit)
    grep_jobs = proc.communicate()[0]

    proc = Popen(['sfood-graph'], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(grep_jobs)
    sfood_graph = proc.communicate()[0]

    proc = Popen(['dot', '-Tps'], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(sfood_graph)
    dot = proc.communicate()[0]

    f = open('import_graph.ps', 'w')
    f.write(dot)

    proc = Popen(['evince', 'import_graph.ps'])

def run_eee_tests():
    proc = Popen(['python', 'analysers/parse_results.py'])
    proc = Popen(['sh', './analysers/plot_eee.sh'])

def run_coverage_tests():
    proc = Popen(['python-coverage', '-x', 'unit_tests/__init__.py'])

def run_coverage_report():
    proc = Popen(['python-coverage', '-rm'] + file_list)

def run_pylint():
    lint.Run(['--rcfile=pylint_standard.rc'] + file_list)

def run_pep8():
    pep8._main(file_list)

def run_unit_tests():
    import unit_tests.__init__ as unit_init
    unit_init.test()

def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.
    """
    usage = "%prog option"

    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', default=0, action='count',
                      help="print status messages, or debug with -vv")
    parser.add_option('-l', '--pylint', default=0, action='count',
                      help="performs a pylint check of the code")
    parser.add_option('-i', '--pep-eight', default=0, action='count',
                      help="Performs a pep8 check of the code")
    parser.add_option('-m', '--make-manual', default=0, action='count',
                      help="makes the pymanetsim manual")
    parser.add_option('-r', '--run', default=0, action='count',
                      help="Starts up the job manager of pymanetsim")
    parser.add_option('-n', '--read-manual', default=0, action='count',
                      help="Launches a browser to read the manual")
    parser.add_option('-e', '--clean-results', default=0, action='count',
                      help="Cleans the result files generated by tests")
    parser.add_option('-y', '--clean-pyc', default=0, action='count',
                      help="Clean those awfull pyc files")
    parser.add_option('-c', '--clean-all', default=0, action='count',
                      help="Cleans all but source of pymanetsim")
    parser.add_option('-u', '--run-unit-tests', default=0, action='count',
                      help="Runs the unit tests")
    parser.add_option('-g', '--draw-import-graph', default=0, action='count',
                      help="Draws the import graphics")
    parser.add_option('-x', '--run-coverage', default=0, action='count',
                      help="Runs the coverage tests")
    parser.add_option('-z', '--report-coverage', default=0, action='count',
                      help="Reports on the coverage tests")
    parser.add_option('-q', '--eee-tests', default=0, action='count',
                      help="Does the eee tests")

    options, args = parser.parse_args(arglist)

    return options, args

def _main():
    """
    Parse options and run checks on Python source.
    """
    options, args = process_options(sys.argv)

    if options.report_coverage:
        run_coverage_report()

    if options.run_coverage:
        run_coverage_tests()

    if options.eee_tests:
        run_eee_tests()

    if options.pylint:
        run_pylint()

    if options.pep_eight:
        run_pep8()

    if options.run_unit_tests:
        run_unit_tests()

    if options.make_manual:
        path = sys.path[0]

        #TODO - Think something better for these two lines
        path_list = os.path.split(path)
        manual_path = [''.join(s) for s in path_list[:-1]][0] + os.sep + 'manual/'

        Popen(['make', 'html'], cwd=manual_path)

    if options.read_manual:
        pass #TODO

    if options.clean_results:
        remove_files_in_dir('../results')

    if options.clean_pyc:
        remove_files_in_dir('.', extension='pyc')

    if options.clean_all:
        remove_files_in_dir('../results')
        remove_files_in_dir('.', extension='pyc')

    if options.draw_import_graph:
        draw_import_graph()

    if options.run:
        run_job_manager()

def remove_files_in_dir(dir, extension=None, recursive=True):
    if dir[-1] == os.sep:
        dir = dir[:-1]

    dir_files = os.listdir(dir)

    for file in dir_files:
        if file == '.' or file == '..':
            continue

        path = dir + os.sep + file
        if os.path.isdir(path):
            if recursive:
                remove_files_in_dir(path, extension=extension)
        else:
            if '.placeholder' in path:
                continue
            if extension:
                file_termination = path[-len(extension)-1:]
                if not file_termination == '.' + extension:
                    continue
            print "Removing: %s" % path
            os.unlink(path)

if __name__ == '__main__':
    _main()