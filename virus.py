from random import random, randint, choice
from segment import Segment
from copy import deepcopy

class Virus(object):
	"""
	The Virus class specifies the viruses that exist within the environment.

	A virus has Segments, and starts with a default of 2 segments of
	length 10 nucleotides.

	"""
	def __init__(self, id, num_segments=2, parent=None, \
		generate_sequence=True):

		"""
		Initiailize the virus with 2 segments, with default segment length.
		Set the id of the virus to the particular id fed in.
		"""

		super(Virus, self).__init__()
		# variable that records the id of the Virus in the Environment.
		self.id = id 
		# variable that records the id of the parent Virus in the Environment.
		self.parent = parent 
		# Boolean variable that records whether this virus was mutated from the
		# parent virus or not.
		self.mutated = False 
		# Boolean variable that records whether this virus was reassorted from 
		# two parents or not.
		self.reassorted = False 

		# List of segments present in the virus.
		self.segments = []
		for i in range(0, num_segments):
			segment = Segment(segment_number=i)
			if generate_sequence == True:
				segment.GenerateAndSetSequence()
				self.segments.append(segment)
			else:
				self.segments.append(None)

	def __repr__(self):
		return str([self.GetID(), self.GetParent(), self.GetSequences()])

	## ID Getters and Setters ##
	def SetID(self, id):
		"""This method sets the ID of the virus."""
		self.id = id

	def GetID(self):
		"""This method returns the ID of the virus."""
		return self.id

	def SetParent(self, parent_id):
		"""
		This method records the ID of the virus' parent prior to 
		replication.
		"""
		self.parent = parent_id

	def GetParent(self):
		"""This method returns the ID of the virus' parent."""
		return self.parent

	def GetSegments(self):
		"""This method will return a list of segments."""
		return self.segments

	def SetSegments(self, list_of_segments):
		"""
		This method will override all segments present in the virus. This
		is essentially syntactic sugar for changing a virus wholesale;
		however, use with caution.
		"""
		self.segments = list_of_segments

	def GetSequences(self):
		"""
		This method will return a list of sequences, one for each 
		segment.
		"""
		sequences = []

		for segment in self.segments:
			sequences.append(segment.GetSequence())

		return sequences

	def SetMutatedStatus(self, status):
		"""This is a helper method that will set the mutated status."""
		self.mutated = status

	def IsMutated(self):
		"""This method returns the mutated status of the virus."""
		return self.mutated

	def IsReassorted(self):
		"""This method returns the reassortant status of the virus."""
		return self.reassorted

	def SetReassortedStatus(self, status):
		"""This is a helper method that will set the reassortant status."""
		self.reassorted = status

	def Mutate(self, segment=None):
		"""
		This method will randomly select one of the segments, then randomly 
		select one position in the segment, and mutate that position. This 
		is essentially syntactic sugar for mutating a segment at random.
		"""
		segment_to_mutate = choice(self.segments)
		segment_to_mutate.Mutate()
		self.SetMutatedStatus(True)

	def Replicate(self, id, mutate=False):
		"""
		This method returns the virus itself, which can be assigned to 
		another virus variable in the Environment (another class). 

		If mutate is set to "False", then a perfect copy of the virus is 
		returned; if mutate is set to "True", then a mutated version of the 
		virus is returned.
		"""
		new_virus = deepcopy(self)
		new_virus.SetID(id)
		new_virus.SetParent(self.GetID())
		new_virus.SetReassortedStatus(False)
		
		if mutate == True:
			new_virus.Mutate()
			return new_virus
		else:
			new_virus.SetMutatedStatus(False)
			return new_virus




