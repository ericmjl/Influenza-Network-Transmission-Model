from random import choice, random, randint

class Segment(object):
	"""Segment class defines what a viral segment is.

	This class specifies the methods for a segment, namely:
	1. Mutating the segment.
	2. Generating a sequence for the segment (if needed)."""
	def __init__(self, n, sequence=None):
		"""Initialize a segment with no sequence."""
		super(Segment, self).__init__()
		self.sequence = sequence
		self.number = n
		# self.name = name

	def __repr__(self):
		return '%s %s' % (self.number, self.sequence)
	
	## Methods that pertain to the sequence of the virus ##
	def GenerateSequence(self, length=10):
		sequence = ''
		for i in range(length):
			letter = choice(['A', 'T', 'G', 'C'])
			sequence += letter
		return sequence

	## Syntactic sugar for generating and setting the sequence ##
	def GenerateAndSetSequence(self, length=10):
		sequence = self.GenerateSequence(10)
		self.SetSequence(sequence)

	# Setter method for a segment's sequence
	def SetSequence(self, sequence):
		self.sequence = sequence

	# Getter method for a segment's sequence
	def GetSequence(self):
		return self.sequence

	# Getter method for a segment's number
	def GetNumber(self):
		return self.number

	# Pick a random letter in the segment's sequence and mutate that letter.
	def Mutate(self):
		n = randint(0, len(self.sequence) - 1)
		sequence = self.sequence

		possible_letters = set(['A', 'T', 'G', 'C'])
		current_letter = set(sequence[n])

		new_letter = choice(list(possible_letters.difference(set(current_letter))))

		new_sequence = ''
		for i, letter in enumerate(sequence):
			if i == n:
				new_sequence += new_letter
			else:
				new_sequence += letter
		
		self.SetSequence(new_sequence)