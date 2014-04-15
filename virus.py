from random import random, randint

class Virus(object):
	"""docstring for Virus

	Virus contains only 1 segment, and that one segment contains a string that
	represents its sequence."""
	def __init__(self):
		super(Virus, self).__init__()
		self.sequence = ''

	"""If you already have a sequence that you would like to set the virus to be,
	then use this method."""
	def setsequence(sequence):
		self.sequence = sequence

	"""If you would like to generate a sequence of n characters using 0s and 1s, 
	then use this method."""
	def generatesequence(self, n):
		sequence = ''
		for position in range(0, n):
			rnd = random()
			if rnd >= 0.5:
				sequence += '1'
			else:
				sequence += '0'
		self.sequence = sequence
		# print sequence

	"""This method will mutate a position in the virus at random."""
	def mutate(self):
		n = randint(0, len(self.sequence) - 1)
		sequence = self.sequence
		print n
		if sequence[n] == '0':
			sequence[n] == '1'
			self.sequence = sequence
		else:
			sequence[n] == '0'
			self.sequence = sequence
