from virus import Virus
from smallfluvirus import SmallFluVirus
from random import choice, sample, randint
from collections import defaultdict
import networkx as nx
from numpy.random import normal, binomial


class Environment(object):
	"""docstring for Environment

	The Environment contains a bunch of viruses, and in the Environment, one 
	can choose to manipulate the viruses at will.
	"""

	def __init__(self, num_viruses=1, virus_type='default'):
		"""Initialize the environment with only 1 default virus."""
		super(Environment, self).__init__()
		
		# This list keeps track of the number of viruses present
		self.viruses = []
		for i in range(num_viruses):
			if virus_type == 'default':
				virus = Virus(id=i, creation_date=0)
			if virus_type == 'influenza':
				virus = SmallFluVirus(id=i, creation_date=0)
			self.viruses.append(virus)

		# This variable keeps track of the number of viruses present
		self.num_viruses = len(self.viruses)

		# The number of times that the environment simulation will run.
		self.timesteps = 100

		# The current timestep of the environment.
		self.current_timestep = 0

	def GetViruses(self):
		"""This method returns the list of viruses in the environment."""
		return self.viruses

	def GetVirus(self, id):
		"""This method returns a specified virus from the environment."""
		virus = [v for v in self.GetViruses() if v.id == id]
		return virus[0]

	def GetRandomVirus(self):
		"""
		This function returns a random virus from the population of viruses
		"""
		return sample(self.viruses, 1)[0]

	def GetLastVirus(self):
		"""
		This function returns the last virus to be generated.
		"""
		return self.viruses[-1]

	def ReplicateVirus(self, virus=None, date=None):
		"""
		This method replicates a specified virus. The number of progeny that come out 
		follows a normal distribution, rounded off to the nearest integer.

		num_of_progeny ~ N(1.2, 0.5)
		"""

		# Check to make sure that the virus is a valid virus object.
		if type(virus) not in [Virus, SmallFluVirus]:
			raise ValueError('You must specify a virus to replicate.')
			pass

		# Check to make sure that the timestamp of the virus is specified.
		if date == None:
			raise ValueError('You must specify a time stamp for the virus.')
			pass

		else:
			num_of_progeny = self.SampleNumberOfDescendants(1.2, 0.5)

			counter = 0
			while counter < num_of_progeny:
				# Generate new virus with new ID.
				new_id = len(self.GetViruses())
				new_virus = virus.Replicate(id=new_id, date=date)
				new_virus.Mutate()

				# Append the virus to the virus list.
				self.viruses.append(new_virus)
				counter += 1

	def MutateVirus(self, virus=None):
		"""
		This method takes a specified virus and mutates it.

		If the virus is not a Virus or SmallFluVirus, an error message will be raised.

		If no virus is specified, then the last virus will be mutated.

		Otherwise, the specified virus will be mutated.
		"""

		# Check to make sure that the virus has the correct type.
		if virus == None:
			virus = self.GetLastVirus()

		virus.Mutate()
		
	def RandomlyReassortTwoViruses(self, date, mutate=False):
		"""
		Here, two viruses will be selected at random from the list of viruses, 
		and a new virus containing a combination of segments, drawn at random 
		per pair of segments, will be returned.

		This is to simulate the process of reassortment in real life.

		If mutate is True, then mutate the chld virus.
		"""
		# Randomly pick two viruses
		virus1, virus2 = sample(self.viruses, 2)
		if len(virus1.GetSegments()) != len(virus2.GetSegments()):
			raise TypeError("ERROR: Virus %s and Virus %s do not have the same number \
				of segments!" % (virus1.GetID(), virus2.GetID())) 

		else:
			# Create the dictionary that will hold the pool of viruses
			segments_pool = dict()

			# Identify how many segments there are
			num_segments = len(virus1.GetSegments())

			# Initialize each segment in the pool to be a list
			for i in range(num_segments):
				segments_pool[i] = []

			# Append each segment in each virus to the appropriate segment 
			# pool
			for i, segment in enumerate(virus1.GetSegments()):
				segments_pool[i].append(segment)

			for i, segment in enumerate(virus2.GetSegments()):
				segments_pool[i].append(segment)

			# Check that the two parental viruses are of identical type. If they are,
			# then create a new virus of the same type as the parental viruses.
			# Otherwise, print error message.
			new_id = "Virus%s" % len(self.viruses)
			if isinstance(virus1, Virus) and isinstance(virus2, Virus):
				new_virus = Virus(creation_date=date, \
					id=new_id, num_segments=num_segments)
			if isinstance(virus1, SmallFluVirus) and isinstance(virus2, SmallFluVirus):
				new_virus = SmallFluVirus(creation_date=date, \
					id=new_id, num_segments=num_segments)
			else:
				print "ERROR: The two viruses must be of the same type."
			new_parents = set()

			# For each pool of segments in the segment pool, randomly choose 
			# one segment to be added to the virus. Append it to the list of 
			# segments to be set as the new virus' segments.
			new_segments = []
			for k,v in segments_pool.iteritems():
				luckysegment = choice(v)
				new_segments.append(luckysegment)
				if v.index(luckysegment) == 0:
					new_parents.add(virus1.GetID())
				else:
					new_parents.add(virus2.GetID())

			# Batch set the new virus' segments to the list of segments. See
			# Virus class documentation on the use of this method.
			new_virus.SetSegments(new_segments)
			new_virus.SetReassortedStatus(True)			
			if len(new_parents) == 1:
				new_virus.SetParent(tuple(new_parents)[0])
				new_virus.SetReassortedStatus(False)
			else:
				new_virus.SetParent(tuple(new_parents))
				new_virus.SetReassortedStatus(True)

			# Add the virus to the list of viruses.
			self.viruses.append(new_virus)

	def SampleNumberOfDescendants(self, mean, stdev):
		"""
		This method returns a rounded number of descendents drawn from a 
		normal distribution. Mean and standard deviation have to be specified.
		"""
		return int(round(normal(mean, stdev)))

	def SampleNumberOfMutations(self, mutation_rate, virus):
		"""
		This method returns a rounded number of mutations to make, drawn from a 
		binomial distribution. Number of positions to choose from is the length 
		of the virus genome, and the mutation rate is specified.
		"""

		length = virus.GetGenomeLength()

		return round(binomial(length, mutation_rate))





