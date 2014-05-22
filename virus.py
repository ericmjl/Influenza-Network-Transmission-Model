from random import random, randint, choice
from segment import Segment
from copy import deepcopy
from host import Host
from datetime import datetime
from joblib import Parallel, delayed

import hashlib

class Virus(object):
	"""
	The Virus class specifies the viruses that exist within the environment.

	A virus has Segments, and starts with a default of 2 segments of
	length 10 nucleotides.

	"""
	def __init__(self, creation_date, host, num_segments=2, parent=None, \
		generate_sequence=True, burst_size_range=(5, 50), \
		generation_time=30):
		"""
		Initiailize the virus with 2 segments, with default segment length.
		"""
		super(Virus, self).__init__()

		# variable that records the id of the Virus in the Environment.
		self.id = None
		self.SetID()

		# variable that references to the parent Virus object.
		self.parent = None
		self.SetParent(parent)

		# Boolean variable that records whether this virus was reassorted from 
		# two parents or not.
		self.reassorted = None
		self.SetReassortedStatus(False) 

		# An integer number describing the time step in which a virus was 
		# generated.
		self.creation_date = None
		self.SetCreationDate(creation_date)

		# List of segments present in the virus. This is changed 
		# in SmallFluVirus.
		self.segments = []
		self.GenerateSegments(num_segments)

		# This is the current host of the virus particle. Each virus particle
		# can only have one host.
		if type(host) != Host:
			raise TypeError('A Host object must be specified!')
		else:
			self.host = host
			host.AddVirus(self)

		# Burst size is a two-tuple that describes the minimum and maximum burst
		# size of the virus per generation/replication cycle. 
		self.burst_size_range = None
		self.SetBurstSizeRange(burst_size_range)

		# Generation time is an integer number that specifies, in minutes, the 
		# time from one generation to the next.
		self.generation_time = None
		self.SetGenerationTime(generation_time)


	def __repr__(self):
		return str(self.GetID())

	def InfectHost(self, host):
		"""
		This method will make the virus infect a specified host.
		"""
		if type(host) != Host:
			raise TypeError('A Host object must be specified!')
		else:
			# Remove virus from the current host.
			self.host.RemoveVirus(self)
			# Set new host for the virus.
			self.host = host
			# Add self to the host.
			host.AddVirus(self)

	def TransmitFromHostToHost(self, host1, host2):
		"""
		DEPRECATE: Move this to Host object.
		This method will make the virus jump from one host to the next.
		"""
		if type(host1) != Host or type(host2) != Host:
			raise TypeError('Two Host objects must be specified!')
		else:
			host2.AddVirus(self)
			host1.RemoveVirus(self)
			self.host = host2

	def Mutate(self, segment=None):
		"""
		This method will mutate all of the viral segments according to their 
		specified substitution rates.
		"""

		for segment in self.GetSegments():
			segment.Mutate()

	def GenerateProgeny(self, date):
		"""
		This method returns a list of progeny virus that have replicated from 
		the current virus.
		"""
		burst_size = randint(self.burst_size_range[0], self.burst_size_range[1])
		# print burst_size
		progeny_viruses = []

		for i in range(burst_size):
			new_virus = self.Replicate(date)
			progeny_viruses.append(new_virus)

		# progeny_viruses = Parallel(n_jobs=10)(delayed(self.Replicate(date))() \
		# 	for i in range(burst_size))

		return progeny_viruses
		
	def Replicate(self, date):
		"""
		This method returns a deep copy of the virus chosen to replicate.

		At the end, return the new virus. 

		Mutate is guaranteed to be called, but not guaranteed to happen. Whether 
		a mutation occurs or not depends on the mutation rate of the virus.
		"""
		new_virus = deepcopy(self)
		new_virus.host = self.host
		new_virus.SetCreationDate(date)
		new_virus.SetID()
		new_virus.SetParent(self)
		new_virus.SetReassortedStatus(False)
		self.host.AddVirus(new_virus)
		new_virus.Mutate()

		return new_virus

	def GenerateSegment(self, segment_number, mutation_rate=0.03, \
		sequence=None, length=100):
		"""
		This method creates a segment with the parameters passed in.

		It is necessary because with some simulations, we do not necessarily
		want a virus generated that has a random sequence. For example, the
		SmallFluVirus has one segment (0) that is completely defined, and 
		another segment (1) that is partially conserved and partially variable. 

		Hence, with the SmallFluVirus, we want to initialize each segment
		differently compared to a regular Virus. 
		-	With a regular Virus, we can initialize the segments to be of 
			equal length and completely random sequence.
		-	With a SmallFluVirus, we need to initialize semgent 0 to have 300
			n.t. mutated 1 n.t. off a fixed seed, and initialize segment 1 to 
			have 200 n.t. mutated 1 n.t. off a fixed seed in addition to 100 
			n.t. with 20 n.t. mutated off a fixed seed.
		"""
		segment = Segment(segment_number=segment_number, \
			mutation_rate=mutation_rate, sequence=sequence, length=length)

		if sequence == None:
			segment.GenerateAndSetSequence()
		
		if sequence != None:
			segment.SetSequence(sequence)

		return segment

	def GenerateSegments(self, num_segments=2, segment_lengths=(10, 10)):
		"""
		This method generates a list of segments with the tuple of segment 
		lengths passed in as a parameter. This method basically automates
		the process of creating segments.
		"""
		if num_segments != len(segment_lengths):
			raise ValueError('The number of segment lengths specified does ' + \
				'not match the number of segments in the virus.')
			pass
		segments = []
		for i, length in enumerate(segment_lengths):
			segments.append(self.GenerateSegment(i, sequence=None, \
				length=length))

		return segments

	def GetCreationDate(self):
		"""
		This method returns the creation date of the virus.
		"""
		return self.creation_date

	def GetGenomeLength(self):
		"""
		This method returns the length of the virus genome, summed over all    
		segments in the viral genome.
		"""
		length = sum(segment.length for segment in self.GetSegments())
		return length

	def GetID(self):
		"""This method returns the ID of the virus."""
		return self.id

	def GetParent(self):
		"""This method returns the ID of the virus' parent."""
		return self.parent

	def GetSegments(self):
		"""This method will return a list of segments."""
		return self.segments

	def GetSegment(self, segment_number):
		"""This method will return the particular segment specified."""
		return self.segments[segment_number]

	def GetSequences(self):
		"""
		This method will return a list of sequences, one for each 
		segment.
		"""
		sequences = []

		for segment in self.segments:
			sequences.append(segment.GetSequence())

		return sequences

	def SetBurstSizeRange(self, burst_size_range):
		"""
		This method will set the burst size range. The burst size range must
		be passed in as a two-element list or tuple, with minimum at the first 
		position, and maximum at the second position.
		"""
		if type(burst_size_range) not in [tuple, list]:
			raise TypeError("A tuple/list of two integers must be specified!")

		if len(burst_size_range) != 2:
			raise ValueError("A two-element tuple/list must be specified!")

		if type(burst_size_range[0]) != int or type(burst_size_range[1]) != int:
			raise TypeError("Integer values of burst sizes must be specified!")

		if burst_size_range[0] > burst_size_range[1]:
			raise ValueError("The burst size range must be specified as (min, max)!")
		else:
			self.burst_size_range = burst_size_range

	def SetCreationDate(self, date):
		"""This method sets the creation date of the virus."""
		self.creation_date = date

	def SetGenerationTime(self, generation_time):
		if type(generation_time) != int:
			raise TypeError('An integer number of minutes must be specified!')
		else:
			self.generation_time = generation_time

	def SetID(self):
		"""
		This method sets the ID of the virus to be a unique string based on
		the string representation of the current time and a randomly chosen
		number.
		"""
		random_number = str(random())
		current_time = str(datetime.now())

		unique_string = random_number + current_time

		unique_id = hashlib.new('sha512')
		unique_id.update(unique_string)
		
		self.id = unique_id.hexdigest()

	def SetParent(self, parent_virus):
		"""This method records the ID of the virus' parent."""
		if parent_virus == None:
			self.parent = None
		elif not isinstance(parent_virus, Virus):
			raise TypeError('A Virus object must be specified!')
		else:
			self.parent = parent_virus

	def SetSegments(self, list_of_segments):
		"""
		This method will override all segments present in the virus. This
		is essentially syntactic sugar for changing a virus wholesale;
		however, use with caution.
		"""
		self.segments = list_of_segments

	def SetReassortedStatus(self, status):
		"""This is a helper method that will set the reassortant status."""
		if status not in [True, False]:
			raise TypeError('A Boolean status must be specified!')
		else:
			self.reassorted = status

	def IsReassorted(self):
		"""This method returns the reassortant status of the virus."""
		return self.reassorted


