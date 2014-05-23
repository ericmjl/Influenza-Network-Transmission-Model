from id_generator import generate_id
from random import sample, choice

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

	def increment_timestep(self):
		self.current_time += 1

		for environment in self.environments:
			environment.current_time += 1

	def increment_one_generation_time(self, environment):
		"""
		This method causes the viruses present in the host to replicate. 
		"""
		hosts = environment.hosts

		for host in hosts:
			host.allow_viral_replication()

	def make_one_infection_happen(self, environment):
		infected_host = choice(environment.get_infected_hosts())
		uninfected_host = choice(environment.get_uninfected_hosts())
		infected_host.infect(uninfected_host)