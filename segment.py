from random import choice, random, randint, sample
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

	def __init__(self, segment_number, mutation_rate, sequence=None):
		"""Initialize a segment with no sequence."""
		super(Segment, self).__init__()
		
		# The sequence of the Segment object is a Sequence object.
		self.seed_sequence = Sequence(sequence=None)
		
		# Each segment has a segment number associated with it. The
		# segment number does not belong to the Sequence object, but
		# to the Segment object.
		self.segment_number = None
		self.set_segment_number(segment_number=segment_number)

		# A dictionary that keeps track of the positions that have been mutated
		self.mutations = dict()

		# This is syntactic sugar, can be taken away if not needed.
		self.length = len(self.compute_sequence())

		# Each segment has a mutation rate associated with it.
		# This is to simulate the different mutation rates associated
		# with each segment e.g. HA mutates faster than NP.
		self.mutation_rate = None
		self.set_mutation_rate(mutation_rate)

	def __repr__(self):
		return 'Segment %s' % self.segment_number

	def set_mutation_rate(self, rate):
		"""This method initializes the mutation rate of the segment."""
		if type(rate) != float:
			raise TypeError('A floating point number must be specified!')
		else:
			self.mutation_rate = rate

	def set_segment_number(self, segment_number):
		"""
		This method initializes the segment number of the segment.
		"""
		if type(segment_number) != int:
			raise TypeError('An integer must be specified!')
		else:
			self.segment_number = segment_number

	def compute_sequence(self):
		"""
		This method computes the segment's sequence by comparing the seed 
		sequence with the mutation dictionary.
		"""
		sequence = ''

		for i, letter in enumerate(self.seed_sequence.get_string()):
			if i in self.mutations.keys():
				sequence += self.mutations[i]
			else:
				sequence += letter

		return sequence

	def get_segment_number(self):
		return self.segment_number

	def get_mutations(self):
		return self.mutations

	def mutate(self):
		"""
		This method uses the length of the segment and the segment's mutation 
		rate to identify the number of positions that will be mutated. It then
		chooses that many positions at random, and records the mutation in the
		segment's mutation dictionary.
		"""
		n = self.length
		p = self.mutation_rate

		num_positions = binomial(n,p)

		def choose_positions(start, end, num_positions):
			"""
			This function chooses n positions at random within
			range(start, end)
			"""
			return sample(range(start, end), num_positions)

		positions = choose_positions(0, len(self.compute_sequence()), \
			num_positions)

		def choose_new_letter(letter):
			"""
			This function chooses a new letter from ATGC that is
			different from the letter passed into the function.
			"""
			possible_letters = set(['A', 'T', 'G', 'C'])
			new_letter = choice(list(
				possible_letters.difference(set(letter))))

			return new_letter

		for position in positions:
			if position in self.mutations.keys():
				letter = self.mutations[position]
			else:
				letter = self.seed_sequence.get_string()[position]

			self.mutations[position] = choose_new_letter(letter)







