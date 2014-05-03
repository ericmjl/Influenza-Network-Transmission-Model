from virus import Virus
from random import choice

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
	def __init__(self, id, num_segments=2, parent=None, \
		generate_sequence=False):
		Virus.__init__(self, id=id, num_segments=num_segments, \
			parent=parent, generate_sequence=generate_sequence)

		"""
		This function is a replacement function for initializing the virus. 
		Specifically, a SmallFluVirus is initialized from a starting seed sequence, 
		then it is mutated.
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
		# A random mutation anywhere in genome.
		self.Mutate(num_positions=1) 

		# Mutate variable region with default parameters
		self.MutateVariableRegion() 
		
		# Mutate constant region with default parameters
		self.MutateConstantRegion()
		
	def Mutate(self, num_positions, mutate_anywhere=True, \
		mutate_variable_region=True, mutate_constant_region=False):
		"""
		This function is a replacement implementation of the Virus class "Mutate" 
		function. The mutation of a SmallFluVirus is different from a Virus in
		the following ways:

		- SmallFluVirus can mutate specified # of positions anywhere.
		- SmallFluVirus can mutate pre-coded # of times in the variable region.
		- SmallFluVirus can mutate specified # of positions in constant region.
		"""

		if mutate_anywhere == True:
			segment_to_mutate = choice(self.GetSegments())
			segment_to_mutate.Mutate(num_positions)

		if mutate_constant_region == True:
			self.MutateConstantRegion()

		if mutate_variable_region == True:
			self.MutateVariableRegion()

	def ReplicateAndMutate(self, id, date, num_positions, mutate_anywhere, \
		mutate_variable_region, mutate_constant_region ):
		"""
		This function is a replacement implementation of the Virus class
		"ReplicateAndMutate" function. A second implementation is necessary because
		the Mutate function takes a different set of parameters. 
		"""

		new_virus = self.Replicate(id, date)
		new_virus.Mutate(num_positions, mutate_anywhere, mutate_variable_region, \
			mutate_constant_region)

		return new_virus	

	def MutateVariableRegion(self, start=200, end=300, num_positions=20):
		"""
		This function specifically mutates 20 nucleotides in the variable 
		region (200-300) of Segment 0 of the virus.
		"""
		self.segments[1].sequence.Mutate(start=start, end=end, \
			num_positions=num_positions)

	def MutateConstantRegion(self, start=0, end=200, num_positions=1):
		"""
		This function specifically mutates 1 nucleotide in the constant 
		region (0-200) of Segment 0 of the virus.
		"""
		self.segments[1].sequence.Mutate(start=start, end=end, \
			num_positions=num_positions)