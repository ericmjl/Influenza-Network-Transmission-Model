from id_generator import generate_id
from random import sample, choice
from joblib import Parallel, delayed

# def _allow_viral_replication(host):
# 	return host.allow_viral_replication()

# def _allow_immune_removal(host):
# 	return host.allow_immune_removal()

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
		print('Creating environment %s...' % environment.id[0:5])

	def create_host(self, environment, immune_halftime=2):
		"""
		This creates a host inside a specified environment.
		"""
		from host import Host

		host = Host(environment=environment, immune_halftime=immune_halftime)
		print('Creating host %s...' % host.id[0:5])

	def create_hosts(self, environment, num_hosts):
		for i in range(num_hosts):
			self.create_host(environment=environment)

	def create_virus(self, host):
		"""
		This creates a virus inside a specified host.
		"""
		from virus import Virus
		
		virus = Virus(creation_date=self.current_time, host=host)
		virus.host.set_infection_history(time=self.current_time, source_host=None)

		print('Creating virus %s...' % virus.id[0:5])

	def increment_timestep(self, num_generations=10):
		"""
		This set of commands happens when one increments one timestep. 
		"""
		print('Current time is %s. Incrementing time to %s' % (self.current_time, self.current_time + 1))
		
		self.current_time += 1

		for environment in self.environments:
			environment.current_time += 1

			for host in environment.get_infected_hosts():
				host.allow_one_cycle_of_replication()

	def get_host_virus_population(self, environment):
		"""
		This method returns a list of the number of viruses in each host in 
		the environment.
		"""
		virus_populations = []
		for host in environment.hosts:
			virus_populations.append(len(host.viruses))
				
		return virus_populations

	def get_num_of_infected_hosts(self, environment):
		"""
		This method counts the number of alive hosts that are infected with 
		viruses.
		"""

		infected_hosts = [host for host in environment.hosts if host.is_infected() == True and host.is_dead() == False]

		return len(infected_hosts)

	def make_one_infection_happen(self, environment):
		if len(environment.get_infected_hosts()) != 0:
			infected_host = choice(environment.get_infected_hosts())
			niave_host = choice(environment.get_naive_hosts())
			infected_host.infect(niave_host)
		else:
			pass

	def make_many_infections_happen(self, environment, num_infections):
		for i in range(num_infections):
			self.make_one_infection_happen(environment)

