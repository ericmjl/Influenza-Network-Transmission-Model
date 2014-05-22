from random import random, randint, choice, sample
from datetime import datetime
from joblib import Parallel, delayed

import hashlib

class Host(object):
	"""
	The Host exists within the environment.

	The host exists to allow viruses to replicate within it.

	One host can have many viruses, replicating and mutating within it.

	When a Sampler samples something, it will sample the host and grab one 
	of the many viral particles present inside the host. That virus is then
	sequenced, and used for reconstruction.
	"""
	def __init__(self, environment, infected_by=None, infected_on=None):
		super(Host, self).__init__()
		# Set the Host ID
		self.id = None
		self.SetID()

		# Set the current environment of the host.
		self.environment = None
		self.SetEnvironment(environment)

		# Set who infected the host.
		self.infected_by = None
		self.SetInfectedBy(infected_by)

		# Set when the host was infected.
		self.infected_on = None
		self.SetInfectedOn(infected_on)

		# A list of viruses present in the host.
		self.viruses = []


	def __repr__(self):
		return "Host %s infected with %s viruses." % (self.id, \
			len(self.viruses))


	def GenerateViralProgeny(self, date):
		"""
		This method is the "host" acting on the "viruses" present inside it.
		What it does is the following:
		- Randomly sample a number of progeny to replicate.
		- Generates the progeny by calling on the virus GenerateProgeny() 
		  function
		- Append the viral progeny to the host's list of viruses
		"""
		
		rand_number = randint(0, len(self.GetViruses()))
		viruses_to_replicate = sample(self.GetViruses(), rand_number)

		for virus in viruses_to_replicate:
			self.AddViruses(virus.GenerateProgeny(date))

	def SetEnvironment(self, environment):
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

	def SetID(self):
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
	
	def SetInfectedBy(self, other_host):
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

	def IsInfected(self):
		"""
		This method checks the length of the viruses list to see if the host
		was infected with virus or not.
		"""
		if len(self.viruses) == 0:
			return False
		else:
			return True

	def AddVirus(self, virus):
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

	def AddViruses(self, viruses):
		"""
		This method takes in a list of viruses and appends it to the 
		current list of viruses.
		"""
		self.viruses.extend(viruses)

	def GetViruses(self):
		"""
		This method gets the list of viruses present in the host.
		"""
		return self.viruses

	def RemoveVirus(self, virus):
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

