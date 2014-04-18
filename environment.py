from virus import Virus
from random import choice, sample
from collections import defaultdict

class Environment(object):
	"""docstring for Environment

	The Environment contains a bunch of viruses, and in the Environment, one 
	can choose to manipulate the viruses at will.
	"""
	def __init__(self, num_viruses=1):
		"""Initialize the environment with only 1 virus."""
		super(Environment, self).__init__()
		
		# This list keeps track of the number of viruses present
		self.viruses = []
		for i in range(num_viruses):
			virus = Virus(id=i)
			self.viruses.append(virus)

		self.num_viruses = len(self.viruses)

	def GetViruses(self):
		"""This method returns the list of viruses in the environment."""
		return self.viruses

	def GetVirus(self, id):
		"""This method returns a specified virus from the environment."""
		if id < 0 or id > len(self.viruses) - 1:
			print "ERROR: The virus ID should be between"
			" 0 and %s ." % (len(self.viruses))
		else:
			return self.viruses[id]

	def ReplicateAVirus(self, mutate=False):
		"""
		This method picks a virus at random and replicates it.

		One can set the "mutate" parameter to be True or False. This will set
		whether the virus will mutate upon replication.
		"""
		# Select a virus to replicate, generate a new ID number.
		virus = choice(self.viruses)
		new_id = len(self.viruses)

		# Replicate the virus.
		new_virus = virus.Replicate(mutate=mutate, id=new_id)

		# Append the virus to the virus list.
		self.viruses.append(new_virus)

	def RandomlyReassortTwoViruses(self, mutate=False):
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
			print "ERROR: Virus %s and Virus %s do not have the same number \
				of segments!" % (virus1.GetID(), virus2.GetID())

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

			# print segments_pool

			new_id = len(self.viruses)
			new_virus = Virus(id=new_id, num_segments=num_segments)
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

			# print new_parents

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