import pdb
from simulator import Simulation
from configuration import DATA_RAW_PATH, DRAW_MAPS

class Job(object):
    """
    This class represents a simulation job to be run
    """

    def __init__(self, job_name, simulation_parameters, x_variable_field, x_variable_name, x_variable_values, y_variables, debug=False):
        """
        Constructor for the parameters present in a job
        """
        counter = 0
        for x_var in x_variable_values:
            counter += 1
            _set_attribute_recursively(simulation_parameters, x_variable_field, x_var)

            if debug:
                import time

                print "\n\n%s -- Running %d of %d with variable %s with value %s" % (time.strftime("%H:%M:%S"), counter, len(x_variable_values), x_variable_name, str(x_var))

            self.sim = Simulation(simulation_parameters)
            self.sim.run()
            self.sim.end_simulation()

            if DRAW_MAPS:
                import plot_plane
                plot_plane.plot_plane(self.sim.plane, self.sim.all_nodes, str(job_name) + str(counter))

            for y_var_name in y_variables:
                y_value = y_variables[y_var_name](self.sim.protocol_manager)
                _save_to_file_statistics(job_name, x_variable_name, y_var_name, x_var, y_value)

def _set_attribute_recursively(simulation_parameters, x_variable_field, value):
    """Sets the attributes of the simulation parameters the the passed field

    Suports attributes inside attributes"""
    field_levels = x_variable_field.split('.')

    lower = simulation_parameters
    for level in field_levels[:-1]:
        lower = getattr(simulation_parameters, level)

    lower_field = field_levels[-1]
    #Now let's check the case if it is an dictionary
    if '[' in lower_field:
        dictionary_string, key = lower_field.split('[')
        key = key.replace('[', '')
        key = key.replace(']', '')
        key = key.replace('\'', '')
        key = key.replace('\"', '')

        dictionary = getattr(lower, dictionary_string)
        dictionary[key] = value

        setattr(lower, dictionary_string, dictionary)

    else: #It is a normal atribute
        setattr(lower, field_levels[-1], value)

def _save_to_file_statistics(strategy, x_parameter_name, y_parameter_name, x_parameter_value, y_parameter_value):
    """Save the values to a data raw file"""
    file_obj = open("%s%s_%s_%s.txt" % (DATA_RAW_PATH, strategy, x_parameter_name, y_parameter_name), "a")
    file_obj.write("%f %d\n" % (x_parameter_value, y_parameter_value))
    file_obj.close()
