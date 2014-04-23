from random import choice, random, randint
from sequence import Sequence

class Segment(object):
	"""
	Segment class defines what a viral segment is.

	This class specifies the methods for a segment, namely:
	1. Mutating the segment.
	2. Generating a sequence for the segment (if needed).
	"""
	def __init__(self, segment_number, sequence=None, length=10):
		"""Initialize a segment with no sequence."""
		super(Segment, self).__init__()
		
		# The sequence of the Segment object is a Sequence object.
		self.sequence = Sequence(length)
		
		# Each segment has a segment number associated with it. The
		# segment number does not belong to the Sequence object, but
		# to the Segment object.
		self.number = segment_number

		# This is syntactic sugar, can be taken away if not needed.
		self.length = self.sequence.length

	def __repr__(self):
		return '%s %s' % (self.number, self.sequence)
	
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
		"""This method gets a segment's sequence."""
		return self.sequence.GetSequence()

	def GetNumber(self):
		"""This method gets a segment's number."""
		return self.number

	def Mutate(self, start=None, end=None, num_positions=1):
		"""
		This method is syntactic sugar for mutating the segment's sequence.
		See: Sequence.Mutate()
		"""

		self.GetSequence().Mutate(start=start, end=end, num_positions=num_positions)