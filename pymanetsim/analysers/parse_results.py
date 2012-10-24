import pdb
import glob, os
import numpy

def parse_single_file(file):
    """
    Opens a single file. Calculates the mean of each value in the first collumn.
    The values of this are in the second collumn.
    """

    f = open(file, 'r')

    results = {} # This is the dictionary where x values have a list of their y, values

    for line in f:
        x_value, y_value = map(float, line.split()) #Transforms both columns in floasts
        x_value = round(x_value, 2) #Rounds to two decimal cases

        if not x_value in results:
            results[x_value] = {'raw':[]} #Puts an empty list in that x_value

        results[x_value]['raw'].append(y_value) #Inserts the y value

    f.close() #The data raw file is no longer needed

    # Calculates the mean of each x_value list
    for x_value in results:
        results[x_value]['mean'] = numpy.mean(results[x_value]['raw'])
        results[x_value]['std'] =  numpy.std(results[x_value]['raw'])

    # Let's put the x_values ordered
    sorted_keys = sorted(results, key=lambda k: k)

    sorted_results = []
    for key in sorted_keys:
        sorted_results.append((key, results[key],))

    return sorted_results

def parse_test(file_name):
    path_processed = "../results/data_processed/"
    path_raw = "../results/data_raw/"

    for infile in glob.glob( os.path.join(path_raw, file_name + '_*.txt') ):
        print "current file is: " + infile
        sorted_results_list = parse_single_file(infile)

        f = open(os.path.join(path_processed, os.path.basename(infile)), 'w')
        for pair in sorted_results_list:
            f.write('%f %d %d\n' % (pair[0], pair[1]['mean'], pair[1]['std']))

        f.close()

if __name__ == '__main__':
    parse_test('*')
