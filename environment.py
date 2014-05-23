from virus import Virus
from random import choice, sample, randint
from collections import defaultdict
from numpy.random import normal, binomial
from host import Host
from id_generator import generate_id
import networkx as nx


class Environment(object):
	"""
	The Environment class is the second highest level object in the viral 
	simulator. Metaphorically, the Environment class can represent a 
	geographic location where Host objects interact with each other, and in 
	the process, pass viruses from one host to the next.

	In the Environment class, Sampler objects can also interact with Host
	objects, to simulate the process of sampling pathogens from the Host.

	Multiple Environment objects can exist in a particular simulation, allowing
	a host to move from Environment to Environment. This allows one to 
	simulate the spread of Viruses from one Environment to another, by means 
	of Hosts moving between them.
	"""

	def __init__(self, num_hosts=0):
		"""Initialize the environment."""
		super(Environment, self).__init__()

		self.current_time = 0

		self.id = generate_id()
		
		self.hosts = []

	def __repr__(self):
		return "Environment %s with %s hosts." % (self.id, len(self.hosts))

	def add_host(self, host):
		from host import Host

		if isinstance(host, Host):
			self.hosts.append(host)
		else:
			raise TypeError('A Host object must be specified!')

	def remove_host(self, host):
		from host import Host

		if isinstance(host, Host):
			self.hosts.pop(self.hosts.index(host))
		elif type(host) == int:
			self.hosts.pop(host)
		else:
			raise TypeError('A Host object or an integer must be specified!')

	# def generate_hosts(self, num_hosts):
	# 	"""
	# 	This method generates hosts that are placed inside the environment.
	# 	"""
	# 	for i in range(num_hosts):
	# 		host = Host(self)
	# 		self.hosts.append(host)

	# """To be coded up"""
	# def RunSimulation(self):
	# 	for i in self.timesteps():
			
			
	# def get_viruses(self):
	# 	"""
	# 	This method returns the list of viruses in the environment.

	# 	NOTE: TO BE DEPRECATED
	# 	"""
	# 	return self.viruses

	# def get_virus(self, id):
	# 	"""
	# 	This method returns a specified virus from the environment.

	# 	NOTE: TO BE DEPRECATED
	# 	"""
	# 	virus = [v for v in self.get_viruses() if v.id == id]
	# 	return virus[0]

	# def get_random_virus(self):
	# 	"""
	# 	This function returns a random virus from the population of viruses.

	# 	NOTE: TO BE DPRECATED
	# 	"""
	# 	return sample(self.viruses, 1)[0]

	# def get_last_virus(self):
	# 	"""
	# 	This function returns the last virus to be generated.

	# 	NOTE: TO BE DEPRECATED
	# 	"""
	# 	return self.viruses[-1]

	# def replicate_virus(self, virus=None, date=None):
	# 	"""
	# 	This method replicates a specified virus. The number of progeny that 
	# 	come out follows a normal distribution, rounded off to the nearest 
	# 	integer.

	# 	num_of_progeny ~ N(1.2, 0.5)

	# 	NOTE: TO BE DEPRECATED
	# 	"""

	# 	# Check to make sure that the virus is a valid virus object.
	# 	if type(virus) not in [Virus, SmallFluVirus]:
	# 		raise ValueError('You must specify a virus to replicate.')
	# 		pass

	# 	# Check to make sure that the timestamp of the virus is specified.
	# 	if date == None:
	# 		raise ValueError('You must specify a time stamp for the virus.')
	# 		pass

	# 	else:
	# 		num_of_progeny = self.sample_number_of_descendents(1.2, 0.5)

	# 		counter = 0
	# 		while counter < num_of_progeny:
	# 			# Generate new virus with new ID.
	# 			new_id = len(self.get_viruses())
	# 			new_virus = virus.replicate(id=new_id, date=date)
	# 			new_virus.mutate()

	# 			# Append the virus to the virus list.
	# 			self.viruses.append(new_virus)
	# 			counter += 1

	# def mutate_virus(self, virus=None):
	# 	"""
	# 	This method takes a specified virus and mutates it.

	# 	If the virus is not a Virus or SmallFluVirus, an error message will be 
	# 	raised.

	# 	If no virus is specified, then the last virus will be mutated.

	# 	Otherwise, the specified virus will be mutated.
	# 	"""

	# 	# Check to make sure that the virus has the correct type.
	# 	if virus == None:
	# 		virus = self.get_last_virus()

	# 	virus.mutate()
		
	# def randomly_reassort_two_viruses(self, date, mutate=False):
	# 	"""
	# 	Here, two viruses will be selected at random from the list of viruses, 
	# 	and a new virus containing a combination of segments, drawn at random 
	# 	per pair of segments, will be returned.

	# 	This is to simulate the process of reassortment in real life.

	# 	If mutate is True, then mutate the chld virus.
	# 	"""
	# 	# Randomly pick two viruses
	# 	virus1, virus2 = sample(self.viruses, 2)
	# 	if len(virus1.get_segments()) != len(virus2.get_segments()):
	# 		raise TypeError("ERROR: Virus %s and Virus %s do not have the same number \
	# 			of segments!" % (virus1.get_id(), virus2.get_id())) 

	# 	else:
	# 		# Create the dictionary that will hold the pool of viruses
	# 		segments_pool = dict()

	# 		# Identify how many segments there are
	# 		num_segments = len(virus1.get_segments())

	# 		# Initialize each segment in the pool to be a list
	# 		for i in range(num_segments):
	# 			segments_pool[i] = []

	# 		# Append each segment in each virus to the appropriate segment 
	# 		# pool
	# 		for i, segment in enumerate(virus1.get_segments()):
	# 			segments_pool[i].append(segment)

	# 		for i, segment in enumerate(virus2.get_segments()):
	# 			segments_pool[i].append(segment)

	# 		# Check that the two parental viruses are of identical type. If they are,
	# 		# then create a new virus of the same type as the parental viruses.
	# 		# Otherwise, print error message.
	# 		new_id = "Virus%s" % len(self.viruses)
	# 		if isinstance(virus1, Virus) and isinstance(virus2, Virus):
	# 			new_virus = Virus(creation_date=date, \
	# 				id=new_id, num_segments=num_segments)
	# 		if isinstance(virus1, SmallFluVirus) and isinstance(virus2, SmallFluVirus):
	# 			new_virus = SmallFluVirus(creation_date=date, \
	# 				id=new_id, num_segments=num_segments)
	# 		else:
	# 			print "ERROR: The two viruses must be of the same type."
	# 		new_parents = set()

	# 		# For each pool of segments in the segment pool, randomly choose 
	# 		# one segment to be added to the virus. Append it to the list of 
	# 		# segments to be set as the new virus' segments.
	# 		new_segments = []
	# 		for k,v in segments_pool.iteritems():
	# 			luckysegment = choice(v)
	# 			new_segments.append(luckysegment)
	# 			if v.index(luckysegment) == 0:
	# 				new_parents.add(virus1.get_id())
	# 			else:
	# 				new_parents.add(virus2.get_id())

	# 		# Batch set the new virus' segments to the list of segments. See
	# 		# Virus class documentation on the use of this method.
	# 		new_virus.set_segments(new_segments)
	# 		new_virus.set_reassorted_status(True)			
	# 		if len(new_parents) == 1:
	# 			new_virus.set_parent(tuple(new_parents)[0])
	# 			new_virus.set_reassorted_status(False)
	# 		else:
	# 			new_virus.set_parent(tuple(new_parents))
	# 			new_virus.set_reassorted_status(True)

	# 		# Add the virus to the list of viruses.
	# 		self.viruses.append(new_virus)

	# def sample_number_of_descendents(self, mean, stdev):
	# 	"""
	# 	This method returns a rounded number of descendents drawn from a 
	# 	normal distribution. Mean and standard deviation have to be specified.

	# 	TODO: DEPRECATE. THIS IS A PROPERTY OF THE VIRUS, NOT OF THE HOST OR 
	# 	ENVIRONMENT
	# 	"""
	# 	return int(round(normal(mean, stdev)))

	# def sample_number_of_mutations(self, mutation_rate, virus):
	# 	"""
	# 	This method returns a rounded number of mutations to make, drawn from a 
	# 	binomial distribution. Number of positions to choose from is the length 
	# 	of the virus genome, and the mutation rate is specified.

	# 	TODO: DEPRECATE. THIS IS A PROPERTY OF THE VIRUS' SEGMENT, NOT OF THE 
	# 	ENVIRONMENT OR HOST.
	# 	"""

	# 	length = virus.GetGenomeLength()

	# 	return round(binomial(length, mutation_rate))





