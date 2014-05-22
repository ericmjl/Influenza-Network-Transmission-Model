from random import choice, random, randint, sample

class Sequence(object):
	"""
	The Sequence object is the lowest level object in the viral simulator. 
	It provides a container for storing seed sequences for the viruses present
	in the environment. 

	This can be subclassed to store seed sequences for other viruses, rather 
	than using a generated sequence. 
	"""
	def __init__(self, length=10, sequence=None):
		"""
		Initialize the sequence with a random sequence of length 10 if 
		sequence is not specified.

		Otherwise, initialize sequence with a sequence that is specified. 
		"""
		super(Sequence, self).__init__()
		if sequence == None:
			self.sequence = self.GenerateSequence(length)
		else:
			self.sequence = sequence

		# self.length = len(self.sequence)

	def __repr__(self):
		return self.sequence
		
	def generate_sequence(self, length):
		"""
		This method will generate a sequence, and set the Sequence object's 
		sequence to that sequence.
		"""
		sequence = ''
		for i in range(length):
			letter = choice(['A', 'T', 'G', 'C'])
			sequence += letter
		return sequence

	# def SetSequence(self, sequence):
	# 	"""Setter method for a segment's sequence."""
	# 	self.sequence = sequence

	# def GenerateAndSetSequence(self, length):
	# 	"""
	# 	Syntactic sugar for generating and setting the sequence
	# 	of a virus.
	# 	"""
	# 	sequence = self.GenerateSequence(length)
	# 	self.SetSequence(sequence)

	# def Append(self, sequence):
	# 	"""
	# 	Appends a sequence to the 3' end of the segment's sequence.
	# 	The 3' end is the right hand side of the sequence.
	# 	"""
	# 	self.sequence += sequence

	def get_string(self):
		"""
		This method returns a string representation of the sequence. This is
		syntactic sugar for the __repr__ method, to help make code in other
		places look cleaner.
		"""
		return str(self.sequence)

	# def Mutate(self, start=None, end=None, num_positions=None):
	# 	"""
	# 	This method will randomly pick a letter in the segment's sequence,
	# 	and proceed to mutate that letter.

	# 	If you wish to mutate a specific region, then specify the "start" and
	# 	"end" positions.

	# 	If you wish to mutate more than 1 position in the specified region, 
	# 	then specify the num_positions that you wish to mutate.

	# 	NOTE: THIS FUNCTION IS WELL-INSULATED. DO NOT CHANGE OR MODIFY.

	# 	UPDATE: THIS FUNCTION WILL BE DEPRECATED, AS THE WAY THAT MUTAITONS 
	# 	ARE BEING MADE IS THROUGH A DICTIONARY.
	# 	"""

	# 	def ChooseNewLetter(letter):
	# 		"""
	# 		This function chooses a new letter from ATGC that is
	# 		different from the letter passed into the function.
	# 		"""
	# 		possible_letters = set(['A', 'T', 'G', 'C'])
	# 		new_letter = choice(list(
	# 			possible_letters.difference(set(letter))))

	# 		return new_letter

	# 	def ChoosePositions(start, end, num_positions):
	# 		"""
	# 		This function chooses n positions at random within
	# 		range(start, end)
	# 		"""
	# 		return sample(range(start, end), num_positions)

	# 	# If it is not specified where to start or end, or if one is specified
	# 	# and the other isn't, then set the start to 0, and end to the length
	# 	# of the sequence.
	# 	if start == None or end == None:
	# 		start = 0
	# 		end = len(self.sequence)

	# 	if num_positions == None:
	# 		raise ValueError("Specify the number of positions to mutate.")

	# 	positions = ChoosePositions(start, end, num_positions)

	# 	new_sequence = ''

	# 	for i, letter in enumerate(self.sequence):
	# 		if i in positions:
	# 			new_sequence += ChooseNewLetter(letter)
	# 		else:
	# 			new_sequence += letter

	# 	self.SetSequence(new_sequence)