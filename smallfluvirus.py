from virus import Virus
from random import choice, randint
from numpy.random import binomial, normal

class SmallFluVirus(Virus):
	"""
	The Small Flu Virus is a condensed version of the influenza virus.

	The difference between the Virus and a Small Flu Virus is that the 
	Small Flu Virus has a 200 nucleotide constant region, and a 100 
	nucleotide variable region on one segment, and a plain vanilla sequence 
	as the other segment. 

	The 200 n.t region is intentionally hard-coded into the class.

	-	Segment 0 contains the  constant 300 n.t. segment that does not undergo
		much mutation.
	-	Segment 1 contains the hybrid 200-100 segment.

	The variable region mutates with high probability. Also, when it mutates,
	5 positions will mutate at one time, as opposed to 1.

	"""
	def __init__(self, id, creation_date, num_segments=2, parent=None, \
		generate_sequence=False):
		Virus.__init__(self, id=id, creation_date=creation_date, \
			num_segments=num_segments, parent=parent, \
			generate_sequence=generate_sequence)

		"""
		This function is a replacement function for initializing the virus. 
		Specifically, a SmallFluVirus is initialized from a starting seed 
		sequence, then it is mutated.
		"""

		# This is the seed sequence for a SmallFluVirus' Segment 0.
		sequence0 = 'ATTTCCCTTGCATATATATTGCGTTTCTTCGACCTTTTAACCGCTCTCTTAGAA' + \
		'GAGAGACAGATAGCTTCTTACCCGTGCCCCACCGTTGGCAGTACGATCGCACGCCCCACGTGAACG' + \
		'ATTGGTAAACCCTGTGGCCTGTGAGCGACAAAAGCTTTAATGGGAAATACGCGCCCATAACTTGGT' + \
		'GCGAATACGGGTCGTAGCAATGTTCGTCTGAGTATGATCTATATAATACGGGCGGTACGTCTGCTT' + \
		'TGGTCAGCCTCTAATGGCTCGTATGATAGTGCAGCCGCTGGTGATCAC'

		# This is the seed sequence for a SmallFluVirus' Segment 1.
		sequence1 = 'CACCGATCTAGAATCGAATGCAAAGATCACCCAGGTGCAAATCAAAAATTCTAG' + \
		'GTAACTAGAAGATTTGCGACGTTCTAAGTGTTGGACGATATGAATCGCGACCCAGGATGACGTCGC' + \
		'CCTGAAAAAAAGATTTCTGCAACTCTCCTCGTCAGCAGTCTGGTGTATCGAAAGTACAGGACTAGC' + \
		'CTTCCTAGCAACCGCGGGCTGGGAATCTGAGACATGAGTCAAGATATTTGCTCGGTAACGTATGCT' + \
		'CTAGGCATCTAACTATTCCCTGTGTCTTATAGGGGCCTGCGTTATCTG'

		self.segments = []

		# Make segment 0 and append to list of segments
		self.segments.append(self.GenerateSegment(0, sequence=sequence0, \
			length=len(sequence0)))

		# Make segment 1's 200 n.t. constant region and append to list
		# of segments
		self.segments.append(self.GenerateSegment(1, sequence=sequence1, \
			length=len(sequence1)))

		# Initialize the virus with some mutations, so that it is 
		# distinguishable from another virus.

		# Firstly, introduce a random mutation anywhere in genome.
		self.Mutate() 

		# Mutate the variable region with default parameters
		self.MutateVariableRegion() 
		
		# Mutate the constant region with default parameters
		self.MutateConstantRegion()
		
	def Mutate(self, mutate_anywhere=True, \
		mutate_variable_region=False, mutate_constant_region=False):
		"""
		This function is a replacement implementation of the Virus class 
		"Mutate" function. The mutation of a SmallFluVirus is different from a 
		Virus in the following ways:

		- Specify whether to mutate anywhere.
		- Specify whether to mutate in constant region
		- Specify whether to mutate in variable region

		NOTE: KEEP THIS FUNCTION UNTIL THE MUTATION RATES HAVE BEEN PROPERLY
		COMPUTED.
		"""

		if mutate_anywhere == True:
			segment_to_mutate = choice(self.GetSegments())
			segment_to_mutate.Mutate()

		if mutate_constant_region == True:
			self.MutateConstantRegion()

		if mutate_variable_region == True:
			self.MutateVariableRegion()

	def MutateVariableRegion(self, start=200, end=300):
		"""
		This function specifically mutates a random number of nucleotides in 
		the variable region (200-300) of Segment 0 of the virus. The number of 
		mutations made follows a Uniform distribution.

		num_positions ~ U(10,20).
		"""
		num_positions = randint(20,60)

		self.segments[1].sequence.Mutate(start=start, end=end, \
			num_positions=num_positions)

	def MutateConstantRegion(self, start=0, end=200):
		"""
		This function specifically mutates a random number of nucleotides in 
		the constant region (0-200) of Segment 0 of the virus. The number of 
		mutations made follows a Binomial distribution 

		num_positions ~ Bin(length of segment, segment mutation rate)
		
		"""
		n = self.segments[0].length
		p = self.segments[0].mutation_rate
		num_positions = binomial(n, p)

		self.segments[1].sequence.Mutate(start=start, end=end, \
			num_positions=num_positions)