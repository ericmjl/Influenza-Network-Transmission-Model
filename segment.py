from random import choice, random, randint
from sequence import Sequence
from numpy.random import binomial

class Segment(object):
	"""
	The Segment class is one level below the Virus class, as it houses the 
	genomic sequence of the Virus. This class has the following attributes and
	methods:

	----------

	ATTRIBUTES 

	- SEQUENCE OBJECT: sequence
		the seed sequence of the segment. 

	- DICTIONARY: mutations
		a dictionary of the mutations that have been made to the virus.

	- FLOAT: mutation_rate
		a floating point number that describes the mutation rate of the virus.
		The units of this number are: substitutions per site per generation time. 
		This can be calculated by dividing the known substitution rate (in 
		substitutions per site per year) by the generation time (in years).

	----------

	MAIN METHODS 

	- Mutate: 
		a method that mutates the segment according to its mutation rate.
		This method is called upon by the Virus object each time it 
		replicates.

	The other methods written in this class are helper methods or syntactic 
	sugar for reducing the number of lines of code, to help with readability.
	"""

	def __init__(self, segment_number, mutation_rate, sequence=None, length=10):
		"""Initialize a segment with no sequence."""
		super(Segment, self).__init__()
		
		# The sequence of the Segment object is a Sequence object.
		self.sequence = Sequence(length)
		
		# Each segment has a segment number associated with it. The
		# segment number does not belong to the Sequence object, but
		# to the Segment object.
		self.number = None
		self.SetSegmentNumber(segment_number)

		# A dictionary that keeps track of the positions that have been mutated
		self.mutations = dict()

		# This is syntactic sugar, can be taken away if not needed.
		self.length = len(self.GetSequence())

		# Each segment has a mutation rate associated with it.
		# This is to simulate the different mutation rates associated
		# with each segment e.g. HA mutates faster than NP.
		self.mutation_rate = None
		self.SetMutationRate(mutation_rate)

	def __repr__(self):
		return 'Segment %s' % self.number

	def SetMutationRate(self, mutation_rate):
		"""This method initializes the mutation rate of the segment."""
		if type(mutation_rate) != float:
			raise TypeError('A floating point number must be specified!')
		else:
			self.mutation_rate = mutation_rate

	def SetSegmentNumber(self, segment_number):
		"""
		This method initializes the segment number of the segment.
		"""
		if type(segment_number) != int:
			raise TypeError('An integer must be specified!')
		else:
			self.segment_number = segment_number

	def SetSequence(self, sequence):
		"""
		Setter method for a segment's sequence.

		NOTE: TO BE DEPRECATED. NOT NEEDED.
		"""
		self.sequence.SetSequence(sequence)

	def GenerateAndSetSequence(self):
		"""
		This method is syntactic sugar for generating and setting the sequence
		of a virus.
		"""
		sequence = self.sequence.GenerateSequence(self.length)
		self.sequence.SetSequence(sequence)

	def Append(self, sequence):
		"""
		This method is syntactic sugar for appending a sequence to the virus.
		"""
		self.sequence.Append(sequence)

	def GetSequence(self):
		"""
		This method computes the segment's sequence by comparing the seed 
		sequence with the mutation dictionary.
		"""
		sequence = ''

		for i, letter in enumerate(self.sequence):
			if i in self.mutations.keys():
				sequence.append(self.mutations[i])
			else:
				sequence.append(letter)

		return sequence

	def GetNumber(self):
		"""This method gets a segment's number."""
		return self.number

	def Mutate(self):
		"""
		This method uses the length of the segment and the segment's mutation 
		rate to identify the number of positions that will be mutated. 

		TODO: REWRITE SUCH THAT THIS UPDATES A DICTIONARY OF MUTATIONS INSTEAD 
		OF MUTATING AN ACTUAL SEQUENCE.
		"""
		n = self.length
		p = self.mutation_rate

		num_positions = binomial(n,p)

		def ChoosePositions(start, end, num_positions):
			"""
			This function chooses n positions at random within
			range(start, end)
			"""
			return sample(range(start, end), num_positions)

		positions = ChoosePositions(0, len(self.GetSequence()), num_positions)

		def ChooseNewLetter():
			"""
			This function randomly chooses one letter from ATGC. The letter
			that is chosen may not necessarily be different from the original
			letter at that position in the sequence.
			"""
			return choice(['A', 'T', 'G', 'C'])

		for position in positions:
			self.mutations[position] = ChooseNewLetter()

		# self.GetSequence().Mutate(num_positions=num_positions)




		