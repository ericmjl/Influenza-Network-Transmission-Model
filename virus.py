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

		# An integer number describing the time step in which a virus was generated.
		self.creation_date = None

		# List of segments present in the virus. This is changed 
		# in SmallFluVirus.
		self.segments = self.GenerateSegments(num_segments)

	def __repr__(self):
		return str([self.GetID(), self.GetParent()])

	def Mutate(self, num_positions, randomly_choose_segment=True, \
		segment=None):
		"""
		By default, a random segment will be chosen to be mutated. From that segment's
		sequence, a random position will be chosen to be changed.

		This method will automatically set the mtuated status of the virus to True.
		"""
		if randomly_choose_segment == True:
			segment_to_mutate = choice(self.GetSegments())

		if randomly_choose_segment == False:
			if segment == None:
				raise Error("If you are not opting to randomly mutate a virus, then " + \
					"you must specify the segment to be mutated.")
			else:
				segment_to_mutate = self.GetSegments()[segment]
		segment_to_mutate.Mutate(num_positions)
		self.SetMutatedStatus(True)

	def Replicate(self, id, date):
		"""
		NOTE: THIS FUNCTION LOOKS WELL-CODED ENOUGH. DO NOT MODIFY UNNECESSARILY.

		This method returns a deep copy of the virus chosen to replicate.

		At the end, return the new virus.
		"""
		new_virus = deepcopy(self)
		new_virus.SetCreationDate(date)
		new_virus.SetID(id)
		new_virus.SetParent(self.GetID())
		new_virus.SetReassortedStatus(False)
		
		return new_virus

	def ReplicateAndMutate(self, id, date, num_positions_to_mutate, \
		randomly_choose_segment=True, segment=None):
		"""
		This method will take a specified virus and replicate it using the Replicate()
		function, and then mutate a specified segment with a specified number of 
		mutations. 
		"""
		new_virus = self.Replicate(id, date)
		new_virus.Mutate(num_positions_to_mutate, \
			randomly_choose_segment=randomly_choose_segment,\
			segment=segment)

		return new_virus

	def GenerateSegment(self, segment_number, sequence=None, length=10):
		"""
		This method creates a segment with the parameters passed in.

		It is necessary because with some simulations, we do not necessarily
		want a virus generated that has a random sequence. For example, the
		SmallFluVirus has one segment (0) that is completely defined, and 
		another segment (1) that is partially conserved and partially variable. 

		Hence, with the SmallFluVirus, we want to initialize each segment
		differently compared to a regular Virus. 
		-	With a regular Virus, we can initialize the segments to be of 
			equal length and completely random sequence.
		-	With a SmallFluVirus, we need to initialize semgent 0 to have 300
			n.t. mutated 1 n.t. off a fixed seed, and initialize segment 1 to 
			have 200 n.t. mutated 1 n.t. off a fixed seed in addition to 100 
			n.t. with 20 n.t. mutated off a fixed seed.
		"""
		segment = Segment(segment_number=segment_number, sequence=sequence,\
			length=length)

		if sequence == None:
			segment.GenerateAndSetSequence()
		
		if sequence != None:
			segment.SetSequence(sequence)

		return segment

	def GenerateSegments(self, num_segments=2, segment_lengths=(10, 10)):
		"""
		This method generates a list of segments with the tuple of segment 
		lengths passed in as a parameter. This method basically automates
		the process of creating segments.
		"""
		if num_segments != len(segment_lengths):
			print 'ERROR: The number of segment lengths specified does not\
					match the number of segments in the virus.'
			pass
		segments = []
		for i, length in enumerate(segment_lengths):
			segments.append(self.GenerateSegment(i, sequence=None, \
				length=length))

		return segments

	def GetCreationDate(self):
		"""
		This method returns the creation date of the virus.
		"""
		return self.creation_date

	def GetGenomeLength(self):
		"""
		This method returns the length of the virus genome, summed over all segments 
		in the viral genome.
		"""
		length = sum(segment.length for segment in self.GetSegments())
		return length

	def GetID(self):
		"""This method returns the ID of the virus."""
		return self.id

	def GetParent(self):
		"""This method returns the ID of the virus' parent."""
		return self.parent

	def GetSegments(self):
		"""This method will return a list of segments."""
		return self.segments

	def GetSegment(self, segment_number):
		"""This method will return the particular segment specified."""
		return self.segments[segment_number]

	def GetSequences(self):
		"""
		This method will return a list of sequences, one for each 
		segment.
		"""
		sequences = []

		for segment in self.segments:
			sequences.append(segment.GetSequence())

		return sequences

	def SetCreationDate(self, date):
		"""This method sets the creation date of the virus."""
		self.creation_date = date

	def SetID(self, id):
		"""This method sets the ID of the virus."""
		self.id = id

	def SetMutatedStatus(self, status):
		"""This is a helper method that will set the mutated status."""
		self.mutated = status

	def SetParent(self, parent_id):
		"""
		This method records the ID of the virus' parent prior to 
		replication.
		"""
		self.parent = parent_id

	def SetSegments(self, list_of_segments):
		"""
		This method will override all segments present in the virus. This
		is essentially syntactic sugar for changing a virus wholesale;
		however, use with caution.
		"""
		self.segments = list_of_segments

	def SetReassortedStatus(self, status):
		"""This is a helper method that will set the reassortant status."""
		self.reassorted = status

	def IsMutated(self):
		"""This method returns the mutated status of the virus."""
		return self.mutated

	def IsReassorted(self):
		"""This method returns the reassortant status of the virus."""
		return self.reassorted


