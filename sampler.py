from environment import Environment
from random import sample, randint
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from datetime import datetime
import networkx as nx


class Sampler(object):
	"""The Sampler class samples a bunch of viruses from an Environment."""
	def __init__(self):
		super(Sampler, self).__init__() 
		self.sampled_viruses = []

	def SampleVirusesFromEnvironment(self, environment, n):
		"""
		This method takes in an Environment and samples n viruses from 
		it.
		"""
		if n == 'all':
			self.sampled_viruses = environment.GetViruses()

		elif not isinstance(n, int) or n < 0:
			print "ERROR: Please change n to an integer number greater than \
					zero."

		elif not isinstance(environment, Environment):
			print "ERROR: You have not specified an environment to sample \
					viruses from."

		else:
			viruses = environment.GetViruses()

			if n > len(viruses):
				print "ERROR: The number of viruses that you want to sample" + \
				" is greater than the number of viruses present."

			else:
				self.sampled_viruses = sample(viruses, n)

	def GetSampledViruses(self):
		"""This method returns the viruses sampled from the environment."""
		return self.sampled_viruses

	def GetRandomVirus(self):
		"""
		This method returns a randomly selected virus from the pool of viruses that
		have been sampled from the environment.
		"""

		return self.sampled_viruses[randint(0, len(self.sampled_viruses) - 1)]

	def DumpSequences(self):
		"""
		This function takes all of the viruses that have been sampled from the 
		environment, and writes their sequences to FASTA files. 

		Each segment will get its own FASTA file.
		"""

		# Get the number of segments present in a randomly selected virus.
		v = self.GetRandomVirus()
		num_segments = len(v.GetSegments())

		# Initialize a dictionary that will contain the list of segments. Make sure
		# the dictionary contains a key for each element present, and initialize the
		# value to be an empty list.
		segments = dict()
		for i in range(num_segments):
			segments[i] = []
		
		# Iterate through all the viruses present in the sampled set. Append each
		# segment to the appropriate list.
		for virus in self.GetSampledViruses():
			for i in range(num_segments):
				record = SeqRecord(Seq(virus.GetSegment(i).GetSequence().GetString()),\
					id=str(virus.GetID()), description="")
				segments[i].append(record)

		# Write the sequences to file with the current date and time present.
		current_time = datetime.now()
		for i in range(num_segments):
			num_sequences = len(segments[i])
			SeqIO.write(segments[i], "%s Simulation Segment %s %s Sequences.fasta" % \
				(current_time, i, num_sequences), "fasta")

	def GenerateNetworkVisualization(self):
		G = nx.MultiDiGraph()
		for virus in self.GetSampledViruses():
			parent = virus.GetParent()
			child = virus.GetID()
			if parent == None:
				G.add_node(child)
			elif type(parent) == int:
				G.add_edge(parent, child, weight=1)
			elif len(parent) == 2:
				G.add_edge(parent[0], child, weight=0.5)
				G.add_edge(parent[1], child, weight=0.5)
		
		nx.draw_circular(G)