from random import random, randint, choice, sample
from datetime import datetime
from joblib import Parallel, delayed
from numpy.random import normal, binomial
from id_generator import generate_id
from time import time
import ctypes

import hashlib

def _generate_progeny(virus):
	return virus.generate_progeny()

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

	def immune_removal_probability(self):
		time_difference = self.timespan_of_infection()
		p = float(time_difference) / (self.immune_halftime + time_difference)

		return p

	def timespan_of_infection(self):
		current_time = self.environment.current_time
		last_infection_time = max(self.infection_history.keys())
		time_difference = current_time - last_infection_time

		return time_difference

	def num_progeny_made(self):
		"""
		This method precomputes the number of progeny to be made.
		"""
		rand_number = randint(0, len(self.viruses))
		parents = sample(self.viruses, rand_number) # the viruses to replicate

		made = sum(virus.burst_size() for virus in parents)

		return made

	def num_progeny_removed(self, num_progeny_made):
		"""
		This method precomputes the number of progeny to be removed from the 
		host.
		"""
		
		time_difference = self.timespan_of_infection()

		p = self.immune_removal_probability()
		n = num_progeny_made

		removed = binomial(n, p)

		return removed

	def num_progeny_leftover(self):
		made = self.num_progeny_made()
		removed = self.num_progeny_removed(made)

		leftover = made - removed

		return leftover

	def generate_viral_progeny(self, num_viruses):
		"""
		This method randomly samples from the current pool of viruses, and  
		generates n progeny from them. The number of progeny that actually 
		comes out may be slightly bigger than the n specified. This is ok.
		"""
		progeny = []
		while len(progeny) < num_viruses:
			parent = choice(self.viruses)
			progeny.extend(parent.generate_progeny())

		# progeny = []
		# returned = Parallel(n_jobs=4)(delayed(_generate_progeny)(parent) for parent in sample(self.viruses, len(self.viruses)) if len(progeny) < num_viruses)

		# print progeny
		return progeny

	def num_parental_removed(self):
		p = self.immune_removal_probability()
		n = len(self.viruses)

		removed = binomial(n, p)

		return removed

	def allow_one_cycle_of_replication(self):
		"""
		This method allows one cycle of replication, where we precompute the 
		net number of progeny present rather than cyclically creating all of 
		them and then removing them (which is slower).
		"""
		if self.is_dead() == False:
			n_leftover = self.num_progeny_leftover()
			# print("Generating %s progeny in host %s..." % \
				# (n_leftover, self.id[0:5]))
			# t1 = time()
			progeny = self.generate_viral_progeny(num_viruses=n_leftover)
			# t2 = time()
			
			# td = t2 - t1

			# print("%s progeny generated in host %s." % (len(progeny), self.id[0:5]))
			parents_to_remove = sample(self.viruses, \
				self.num_parental_removed())
			for virus in parents_to_remove:
				self.remove_virus(virus)

			self.add_viruses(progeny)

		else:
			pass

		return self


	def allow_viral_replication_slow(self):
		"""
		This method is the "host" acting on the "viruses" present inside it.

		What it does is the following:
		- Randomly sample a number of progeny to replicate.
		- Generates the progeny by calling on the virus 
		  generate_viral_progeny() function

		Note: this function might be deprecated in favor of precomputing the 
		number of progeny.
		"""
		if self.is_dead() == False:

			# # print('Host %s currently has %s viruses.' % (id(self), len(self.viruses)))
			
			rand_number = randint(0, len(self.viruses))
			# # print('Replicating %s viruses.' % rand_number)
			
			viruses_to_replicate = sample(self.viruses, rand_number)

			viruses_generated = []
			for virus in viruses_to_replicate:
				viruses_generated.exted(virus.generate_progeny())

			self.add_viruses(viruses_generated)

			# # print('Total of %s viruses generated in host %s. ' % (total_viruses_generated, id(self)))
			# # print('Host %s now has %s viruses.' % (id(self), len(self.viruses)))

			return self

		elif self.is_dead() == True:
			return self
			pass


	def allow_immune_removal_slow(self):
		"""
		This method allows the removal of a certain number of viruses to be 
		removed from the host due to immune system pressure.

		Note: this method may be deprecated in favor of precomputing the 
		number of progeny.
		"""

		current_time = self.environment.current_time
		last_infection_time = max(self.infection_history.keys())
		time_difference = current_time - last_infection_time

		p = float(time_difference) / (self.immune_halftime + time_difference)
		n = len(self.viruses)

		# # print("Time Difference: %s, Probability: %s" % (time_difference, p))
		num_viruses_to_remove = binomial(n, p)
		# num_viruses_to_remove = int(0.6 * len(self.viruses))
		# # print('Removing %s viruses out of %s viruses from host %s.' % (num_viruses_to_remove, len(self.viruses), id(self)))

		viruses_to_remove = sample(self.viruses, num_viruses_to_remove)
		for virus in viruses_to_remove:
			self.remove_virus(virus)

		# # print('Host %s is left with %s viruses.' % (id(self), len(self.viruses)))

		return self


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
			num_viruses = int(normal(bottleneck_mean, bottleneck_variance))

		# # print('Transmission %s viruses out of %s viruses from host %s to host %s.' % (num_viruses, len(self.viruses), id(self), id(other_host)))
		viruses_to_transmit = sample(self.viruses, num_viruses)

		for virus in viruses_to_transmit:
			virus.host = other_host
			self.remove_virus(virus)

		other_host.add_viruses(viruses_to_transmit)

	def move_to_environment(self, environment):
		"""
		This method moves the Host from one environment to another.
		"""
		self.environment.remove_host(self)
		environment.add_host(self)
		self.set_environment(environment)

	def set_infection_history(self, time, source_host):
		self.infection_history[time] = source_host\

	def was_infected(self):
		if len(self.infection_history.keys()) > 0:
			return True

		else:
			return False

	def is_infectious(self):
		if len(self.viruses) < self.max_viruses / 10:
			return False
		else:
			return True

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
		# The following line has to be placed inside here, in order to make the code work. Do not remove.
		from virus import Virus
		"""
		This method adds a virus to the list of viruses present in the host.
		"""
		if not isinstance(virus, Virus):
			raise TypeError('A Virus object must be specified!')
		elif virus not in self.viruses:
			self.viruses.append(virus)

	def add_viruses(self, viruses):
		"""
		This method takes in a list of viruses and appends it to the 
		current list of viruses.
		"""
		for virus in viruses:
			self.add_virus(virus)

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
