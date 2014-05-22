from random import choice, random, randint
from sequence import Sequence
from numpy.random import binomial

class Segment(object):
	"""
	Segment class defines what a viral segment is.

	This class specifies the methods for a segment, namely:
	1. Mutating the segment.
	2. Generating a sequence for the segment (if needed).
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

		# This is syntactic sugar, can be taken away if not needed.
		self.length = self.sequence.length

		# Each segment has a mutation rate associated with it.
		# This is to simulate the different mutation rates associated
		# with each segment e.g. HA mutates faster than NP.
		self.mutation_rate = None
		self.SetMutationRate(mutation_rate)

	def __repr__(self):
		return '%s %s' % (self.number, self.sequence)

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
	
	def GenerateSequence(self):
		"""
		This is syntactic sugar to generate a sequence of specified length.
		"""
		self.sequence.GenerateSequence(self.length)

	def SetSequence(self, sequence):
		"""Setter method for a segment's sequence."""
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
		"""This method gets a segment's sequence as a string."""
		return self.sequence

	def GetNumber(self):
		"""This method gets a segment's number."""
		return self.number

	def Mutate(self):
		"""
		This method uses the length of the segment and the segment's mutation rate to
		identify the number of positions that will be mutated. 
		"""
		n = self.length
		p = self.mutation_rate

		num_positions = binomial(n,p)

		self.GetSequence().Mutate(num_positions=num_positions)




		