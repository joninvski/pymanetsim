from job_list import ALL_JOBS
from simulator import PlaneParameters, ProtocolParameters, NodeParameters, ConfigurationParameters, SimulationParameters
from sim_job import Job


PROFILE_PROGRAM = False

def update_all_parameters(job):
    for abstract_job in job.abstract:
        job.plane_parameters.update(abstract_job.plane_parameters)
        job.node_parameters.update(abstract_job.node_parameters)
        job.config_parameters.update(abstract_job.config_parameters)
        job.protocol_parameters.update(abstract_job.protocol_parameters)

        job.x_variable_field = abstract_job.x_variable_field or job.x_variable_field
        job.x_variable_name = abstract_job.x_variable_name or job.x_variable_name
        job.x_variable_values = abstract_job.x_variable_values or job.x_variable_values

def make_all_parameters_exist(job):
    job.plane_parameters = getattr(job, 'plane_parameters', {})
    job.protocol_parameters = getattr(job, 'protocol_parameters', {})
    job.node_parameters = getattr(job, 'node_parameters', {})
    job.config_parameters = getattr(job, 'config_parameters', {})
    job.abstract = getattr(job, 'abstract', [])

    job.x_variable_field = getattr(job, "x_variable_field", None)
    job.x_variable_name = getattr(job, "x_variable_name", None)
    job.x_variable_values = getattr(job, "x_variable_values", None)

    for abstract_job in job.abstract:
        make_all_parameters_exist(abstract_job)

def run_all_jobs():
    global ALL_JOBS
    run_job_list(ALL_JOBS)

def run_job_list(job_list):
    #This is to put the jobs with hierarchy working
    for job in job_list:
        make_all_parameters_exist(job)
        update_all_parameters(job)

    #Now lets execute the jobs
    for job in job_list:
        print """
        ----->----->----->-------
        Running job: %s"
        """ % (job)

        plane_p = PlaneParameters(job.plane_parameters)
        protocol_p = ProtocolParameters(job.protocol_parameters)
        node_p = NodeParameters(job.node_parameters)
        config_p = ConfigurationParameters(job.config_parameters)

        simulation_parameters = SimulationParameters(plane_parameters=plane_p, protocol_parameters=protocol_p, node_parameters=node_p, config_parameters=config_p)

        print simulation_parameters

        job = Job(job_name=job.job_name, simulation_parameters= simulation_parameters, x_variable_field=job.x_variable_field, \
                  x_variable_name=job.x_variable_name, x_variable_values=job.x_variable_values, y_variables=job.y_variables, debug=True)

        print """
        Finished running job: %s"
        -----<-----<-----<-------
        """ % (job)

if __name__ == '__main__':
    if PROFILE_PROGRAM == True:
        import cProfile
        cProfile.run("run_all_jobs()", filename="test1.cprof", sort=1)
    else:
        run_all_jobs()
