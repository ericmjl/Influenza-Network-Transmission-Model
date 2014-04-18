from random import choice, random, randint

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
		self.sequence = sequence
		self.number = segment_number
		self.length = length

	def __repr__(self):
		return '%s %s' % (self.number, self.sequence)
	
	def GenerateSequence(self):
		"""
		This method will generate a sequence for the segment, using the 
		length attribute of the segment.
		"""
		sequence = ''
		for i in range(self.length):
			letter = choice(['A', 'T', 'G', 'C'])
			sequence += letter
		return sequence

	def GenerateAndSetSequence(self):
		"""
		Syntactic sugar for generating and setting the sequence
		of a virus.
		"""
		sequence = self.GenerateSequence()
		self.SetSequence(sequence)

	def SetSequence(self, sequence):
		"""Setter method for a segment's sequence."""
		self.sequence = sequence

	def GetSequence(self):
		"""Getter method for a segment's sequence."""
		return self.sequence

	def GetNumber(self):
		"""Getter method for a segment's number."""
		return self.number

	def Mutate(self):
		"""
		This method will randomly pick a letter in the segment's sequence,
		and proceed to mutate that letter.
		"""

		# Randomly pick a position to mutate.
		n = randint(0, len(self.sequence) - 1)
		sequence = self.sequence

		# Because we are using the nucleotide code, and we are mutating the 
		# segment, we therefore have to mutate away from the current letter.
		possible_letters = set(['A', 'T', 'G', 'C'])
		current_letter = set(sequence[n])
		new_letter = choice(list(
			possible_letters.difference(set(current_letter))))

		# Because Python strings are immutable, we will construct a new
		# string from the old one, except that the position specified will
		# be mutated.
		new_sequence = ''
		for i, letter in enumerate(sequence):
			if i == n:
				new_sequence += new_letter
			else:
				new_sequence += letter
		
		# Set the sequence of the segment 
		self.SetSequence(new_sequence)