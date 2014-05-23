from random import random, randint, choice, sample
from datetime import datetime
from joblib import Parallel, delayed
from numpy.random import normal, binomial
from id_generator import generate_id

import hashlib


class Host(object):
	"""
	The Host object is the second highest level object in the simulator. The
	Metaphorically, the Host object is the host for a pathogen. At each 
	discrete viral generation time, the Host can allow Virus(es) to generate  
	progeny inside of itself. Additionally, at each time step, the host can
	remove a proportion of viruses from itself. The dynamics of viral removal 
	can be configured by subclassing the Host object. The dynamics of viral 
	progeny generation can be configured by subclassing the Virus object.

	Host objects have to exist within an environment. This is compulsory to 
	be able to track where a virus was sampled. 

	For the purposes of knowing the ground truth of infection, Host objects
	are capable of keeping track of who they were infected by and when. 
	Currently, this is kept track of as two individual variables. In the 
	future, in order to generalize this to multiple infections, this will be 
	kept track of as a single dictionary, where the keys are the time of 
	infection, and the values are the Host objects that were the source of 
	infection.

	Sampler objects can interact with Host objects. Sampler objects can either 
	sample everything from the host, or it can sample a subset of viruses. The 
	number of viruses that are sampled at each sampling event can be
	configured by subclassing the Sampler class.
	"""

	def __init__(self, environment, immune_halftime=2):
		super(Host, self).__init__()

		self.id = generate_id()

		self.environment = None
		self.set_environment(environment)

		self.infection_history = dict()

		self.immune_halftime = immune_halftime

		self.max_viruses = 5000

		self.viruses = []

	def __repr__(self):
		return "Host %s infected with %s viruses" % (self.id, \
			len(self.viruses))

	def is_infectious(self):
		"""
		The host is infectious if it is currently carrying more than 0.1 of 
		its viral carrying capacity.
		"""
		if len(self.viruses) < self.max_viruses * 0.1:
			return True
		else:
			return False

	def is_dead(self):
		if len(self.viruses) > self.max_viruses:
			return True
		else:
			return False

	def allow_viral_replication(self):
		"""
		This method is the "host" acting on the "viruses" present inside it.

		What it does is the following:
		- Randomly sample a number of progeny to replicate.
		- Generates the progeny by calling on the virus 
		  generate_viral_progeny() function
		"""

		rand_number = randint(0, len(self.viruses))
		viruses_to_replicate = sample(self.viruses, rand_number)

		for virus in viruses_to_replicate:
			virus.generate_progeny()

	def allow_immune_removal(self):
		"""
		This method allows the removal of a certain number of viruses to be 
		removed from the host due to immune system pressure.
		"""

		current_time = self.environment.current_time
		last_infection_time = max(self.infection_history.keys())
		time_difference = current_time - last_infection_time

		p = float(time_difference) / (self.immune_halftime + time_difference)
		n = len(self.viruses)
		num_viruses_to_remove = binomial(n, p)

		viruses_to_remove = sample(self.viruses, num_viruses_to_remove)
		for virus in viruses_to_remove:
			self.remove_virus(virus)


	def set_environment(self, environment):
		"""
		This method sets the environment that the host is currently in.
		This method exists because we want the host to be capable of 
		moving between different environments.
		"""
		from environment import Environment

		if isinstance(environment, Environment):
			self.environment = environment
			environment.add_host(self)

		else:
			raise TypeError('An environment object must be specified!')

	def infect(self, other_host, bottleneck_mean=10, bottleneck_variance=2):
		"""
		This method will sample a random number of viruses to give to another 
		host. It will also update the infection history of the other host.
		"""
		infection_time = self.environment.current_time
		other_host.set_infection_history(infection_time, self)

		num_viruses = len(self.viruses) + 1
		while num_viruses > len(self.viruses):
			num_viruses = normal(bottleneck_mean, bottleneck_variance)

		viruses_to_transmit = sample(self.viruses, int(num_viruses))

		other_host.add_viruses(viruses_to_transmit)

		for virus in viruses_to_transmit:
			self.remove_virus(virus)

	def move_to_environment(self, environment):
		"""
		This method moves the Host from one environment to another.
		"""
		self.environment.remove_host(self)
		environment.add_host(self)

	def set_infection_history(self, time, source_host):
		self.infection_history[time] = source_host

	def is_infected(self):
		"""
		This method checks the length of the viruses list to see if the host
		was infected with virus or not.
		"""
		if len(self.viruses) == 0:
			return False
		else:
			return True

	def add_virus(self, virus):
		# The following line has to be placed inside here, in order to make 
		# the code work. Do not remove virus or 
		from virus import Virus
		"""
		This method adds a virus to the list of viruses present in the host.
		"""
		if not isinstance(virus, Virus):
			raise TypeError('A Virus object must be specified!')
		else:
			self.viruses.append(virus)

	def add_viruses(self, viruses):
		"""
		This method takes in a list of viruses and appends it to the 
		current list of viruses.
		"""
		self.viruses.extend(viruses)

	def viruses(self):
		"""
		This method gets the list of viruses present in the host.
		"""
		return self.viruses

	def remove_virus(self, virus):
		"""
		This method exists for the purpose of removing a virus from a host
		during a transmission event. The particular viral particle goes
		away, though the particle's descendents or ancestors may still
		remain inside the host.

		Either the particular virus object must be specified, or an integer 
		describing the position in the current list of viruses must be 
		specified.
		"""
		from virus import Virus

		if isinstance(virus, Virus):
			self.viruses.pop(self.viruses.index(virus))
		elif type(virus) == int:
			self.viruses.pop(virus)
		else:
			raise TypeError('A Virus object or an integer must be specified!')

