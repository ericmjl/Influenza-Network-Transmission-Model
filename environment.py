from virus import Virus
from smallfluvirus import SmallFluVirus
from random import choice, sample, randint
from collections import defaultdict
import networkx as nx


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
				virus = Virus(id=i)
			if virus_type == 'influenza':
				virus = SmallFluVirus(id=i)
			self.viruses.append(virus)

		self.num_viruses = len(self.viruses)

	def GetViruses(self):
		"""This method returns the list of viruses in the environment."""
		return self.viruses

	def GetVirus(self, id):
		"""This method returns a specified virus from the environment."""
		if id < 0 or id > len(self.viruses) - 1:
			print "ERROR: The virus ID should be between" + \
			" 0 and %s." % (len(self.viruses) - 1)
		else:
			return self.viruses[id]

	def GetRandomVirus(self):
		"""
		This function returns a random virus from the population of viruses
		"""
		return self.viruses[randint(0, len(self.viruses)-1)]

	def ReplicateAVirus(self, mutate=False, mutate_variable_region=False, \
		num_variable_positions=20):
		"""
		This method picks a virus at random and replicates it.

		If the "mutate" parameter is set to True, the virus will mutate in one
		randomly chosen position, including any "variable" regions if present.
		Otherwise, this will not happen.

		If the "mutate_variable_region" parameter is set to True, the virus will
		first be checked to be a "smallfluvirus". If that is also true, then the 
		variable region of the smallfluvirus will undergo 20 point mutations.
		Otherwise, the mutate_variable_region parameter will be ignored.
		"""
		# Select a virus to replicate, generate a new ID number.
		virus = choice(self.viruses)
		new_id = len(self.viruses)

		# If the type of the virus is a SmallFluVirus and mutate_variable_region is 
		# True, then replicate the virus while mutating the variable region.
		if isinstance(virus, SmallFluVirus) and mutate_variable_region == True:
			# Replicate the virus.
			print "The virus is a Small Flu Virus."
			new_virus = virus.Replicate(id=new_id, mutate=mutate, \
				mutate_variable_region=mutate_variable_region)

		# If the virus is not a smallfluvirus yet mutate_variable_region is True, then
		# print an error and ignore the mutate_variable_region request.
		elif not isinstance(virus, SmallFluVirus) and mutate_variable_region == True:
			print "WARNING: You are requesting to mutate the variable region of a " + \
					"virus that contains no variable region. Request ignored."
			new_virus = virus.Replicate(mutate=mutate, id=new_id)

		# Otherwise, simply replicate and ignore the mutate_variable_region parameter.
		else:
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

			# Check that the two parental viruses are of identical type. If they are,
			# then create a new virus of the same type as the parental viruses.
			# Otherwise, print error message.
			new_id = len(self.viruses)
			if isinstance(virus1, Virus) and isinstance(virus2, Virus):
				new_virus = Virus(id=new_id, num_segments=num_segments)
			if isinstance(virus1, SmallFluVirus) and isinstance(virus2, SmallFluVirus):
				new_virus = SmallFluVirus(id=new_id, num_segments=num_segments)
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

