from random import random, randint, choice, sample
from datetime import datetime
from joblib import Parallel, delayed

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
	Currently, this is kept track of as two individual variables. In the future,
	in order to generalize this to multiple infections, this will be kept
	track of as a single dictionary, where the keys are the time of infection,
	and the values are the Host objects that were the source of infection.
	TODO: CHANGE INFECTED_BY AND INFECTED_ON TO INFECTION_HISTORY.

	Sampler objects can interact with Host objects. Sampler objects can either 
	sample everything from the host, or it can sample a subset of viruses. The 
	number of viruses that are sampled at each sampling event can be configured 
	by subclassing the Sampler class.
	"""
	
	def __init__(self, environment, infected_by=None, infected_on=None):
		super(Host, self).__init__()
		# Set the Host ID
		self.id = None
		self.set_id()

		# Set the current environment of the host.
		self.environment = None
		self.set_environment(environment)

		# Infection history
		self.infection_history = dict()

		# A list of viruses present in the host.
		self.viruses = []


	def __repr__(self):
		return "Host %s infected with %s viruses." % (self.id, \
			len(self.viruses))


	def generate_viral_progeny(self, date):
		"""
		This method is the "host" acting on the "viruses" present inside it.
		What it does is the following:
		- Randomly sample a number of progeny to replicate.
		- Generates the progeny by calling on the virus generate_viral_progeny() 
		  function
		- Append the viral progeny to the host's list of viruses
		"""
		
		rand_number = randint(0, len(self.get_viruses()))
		viruses_to_replicate = sample(self.get_viruses(), rand_number)

		for virus in viruses_to_replicate:
			self.add_viruses(virus.generate_viral_progeny(date))

	def set_environment(self, environment):
		"""
		This method sets the environment that the host is currently in.
		This method exists because we want the host to be capable of 
		moving between different environments.
		"""
		from environment import Environment

		if isinstance(environment, Environment):
			self.environment = environment

		else:
			raise TypeError('An environment object must be specified!')

	def set_id(self):
		"""
		This method sets the ID of the virus to be a unique string based on
		the string representation of the current time and a randomly chosen
		number.
		"""
		random_number = str(random())
		current_time = str(datetime.now())

		unique_string = random_number + current_time

		unique_id = hashlib.new('sha512')
		unique_id.update(unique_string)
		
		self.id = unique_id.hexdigest()

	def set_infection_history(self, time, other_host):
		self.infection_history[time] = other_host
	
	def set_infected_by(self, other_host):
		"""
		This method will set the "infected_by" variable to the source of the 
		virus for the host.
		"""
		if other_host == None:
			self.infected_by = None
		elif type(other_host) != Host:
			raise TypeError('A Host object must be specified!')
		else:
			self.infected_by = other_host

	def SetInfectedOn(self, date):
		"""
		This method will set the "infected_on" variable with the date of 
		infection of the host.

		For now, restrict "date" to be an integer.
		"""
		if date == None:
			self.infected_on = None
		elif type(date) != int:
			raise TypeError('An integer must be specified!')
		else:
			self.infected_on = date

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
		# the code work.
		from virus import Virus
		"""
		This method adds a virus to the list of viruses present in the host.
		"""
		if isinstance(virus, Virus):
			self.viruses.append(virus)
		else:
			raise TypeError('A Virus object must be specified!')

	def add_viruses(self, viruses):
		"""
		This method takes in a list of viruses and appends it to the 
		current list of viruses.
		"""
		self.viruses.extend(viruses)

	def get_viruses(self):
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

