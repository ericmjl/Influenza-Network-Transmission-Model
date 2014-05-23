from id_generator import generate_id
from random import sample, choice
from joblib import Parallel, delayed

def _allow_viral_replication(host):
	return host.allow_viral_replication()

def _allow_immune_removal(host):
	return host.allow_immune_removal()

class Controller(object):
	"""
	The controller object is the overall manager for the viral simulation.
	"""
	def __init__(self, environments=None):
		super(Controller, self).__init__()
		
		self.environments = []
		self.current_time = 0

	def create_environment(self, num_hosts=0):
		from environment import Environment
		environment = Environment(num_hosts=num_hosts)

		self.environments.append(environment)

	def create_host(self, environment):
		from host import Host 

		host = Host(environment)

	def create_hosts(self, environment, num_hosts):
		for i in range(num_hosts):
			self.create_host(environment)

	def create_virus(self, host):
		from virus import Virus
		
		virus = Virus(creation_date=self.current_time, host=host)
		virus.host.set_infection_history(self.current_time, None)

	def increment_timestep(self, num_generations=10):
		self.current_time += 1

		for environment in self.environments:
			environment.current_time += 1

			for host in environment.get_infected_hosts():
				if host.is_dead():
					environment.remove_host(host)
					print("Removing host %s" % host)
				if not host.is_dead():
					host.allow_viral_replication()
					host.allow_immune_removal()
				


	# def increment_one_generation_time(self, environment):
	# 	"""
	# 	This method causes the viruses present in the host to replicate. 
	# 	"""
	# 	hosts = environment.hosts

	# 	for host in hosts:
	# 		host.allow_viral_replication()

	def make_one_infection_happen(self, environment):
		infected_host = choice(environment.get_infected_hosts())
		uninfected_host = choice(environment.get_uninfected_hosts())
		infected_host.infect(uninfected_host)

	def make_many_infections_happen(self, environment, num_infections):
		for i in range(num_infections):
			self.make_one_infection_happen(environment)

