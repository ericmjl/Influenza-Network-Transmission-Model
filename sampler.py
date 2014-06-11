from environment import Environment
from random import sample, randint
from numpy.random import normal, binomial
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from datetime import datetime
import networkx as nx
from sklearn.cluster import AffinityPropagation


class Sampler(object):
	"""
	The Sampler object samples a bunch of viruses from hosts in an  
	Environment.

	Many Sampler objects can exist within a single environment. The role of 
	the Sampler object is to contact a host, and remove a certain number of 
	viruses from it to be sequenced. This is to mimic the real-world behavior 
	and limitations of a sampler.

	The dumping of full sequences of every virus present in the host at every 
	timepoint will not be done by the Sampler object, as that is, by 	
	definition, what the Sampler object does not do. This will be a part of 
	the Controller object.

	However, the Sampler object will have a "dump_sampled_sequences()" method, 
	which will dump the sequences that have been sampled. This will not mimic 
	the realities of sampling, in which we don't necesssarily get all of the 
	viruses present. In other words, we are assuming perfect sequencing of the 
	sampled virus population.
	"""
	def __init__(self, environment):
		super(Sampler, self).__init__() 
		self.sampled_viruses = []
		self.environment = environment

		self.sampled_viruses = []

		self.sampled_hosts = []


	def sample_viruses(self, host, mean=10, stdev=2):
		"""
		This method gets a subsample of viruses from the population of viruses 
		present inside a Host. The number of viruses sampled follows a 
		Normal(10,2) distribution, which (for now) is identical to the 
		"infect" function of a Host. 

		The Host must be infectious in order for viruses to be able to be 
		sampled. This should mimic known biology, in which only when the host 
		is shedding virus is it infectious; .similarly, only when it is 
		shedding virus are we able to detect viruses 

		Therefore, when we sample the Host, 
			- 	if the Host is infectious, then will return a tuple containing 
				the host and a list of the sampled viruses 
			-	if the Host is not infectious, we will return a tuple 
				containing the host and an empty list.
		"""
		# Check that host is a Host type
		from host import Host

		if isinstance(host, Host):
			# Check if the host is infectious
			if host.is_infectious():

				# Guarantee that the number of viruses sampled is fewer than 
				# the number of viruses present in the host.
				num_viruses = len(host.viruses) + 1
				while num_viruses > len(host.viruses):
					num_viruses = int(normal(mean, stdev))

				# Sample viruses from the host, and remove them from the host.
				sampled_viruses = sample(host.viruses, num_viruses)
				host.remove_viruses(sampled_viruses)
				return (host, sampled_viruses)

			if not host.is_infectious():
				return (host, [])

		else:
			raise TypeError("A Host object must be specified")

	# def SampleVirusesFromEnvironment(self, environment, n):
	# 	"""
	# 	This method takes in an Environment and samples n viruses from 
	# 	it.
	# 	"""
	# 	if n == 'all':
	# 		self.sampled_viruses = environment.GetViruses()

	# 	else:
	# 		viruses = environment.GetViruses()

	# 		if n > len(viruses):
	# 			print "ERROR: The number of viruses that you want to sample is greater than the number of viruses present."

	# 		else:
	# 			self.sampled_viruses = sample(viruses, n)

	# def GetSampledViruses(self):
	# 	"""This method returns the viruses sampled from the environment."""
	# 	return self.sampled_viruses

	# def GetRandomVirus(self):
	# 	"""
	# 	This method returns a randomly selected virus from the pool of viruses 
	# 	that have been sampled from the environment.
	# 	"""

	# 	return self.sampled_viruses[randint(0, len(self.sampled_viruses) - 1)]

	# def DumpSequences(self, run_number):
	# 	"""
	# 	This function takes all of the viruses that have been sampled from the 
	# 	environment, and writes their sequences to FASTA files. 

	# 	Each segment will get its own FASTA file.
	# 	"""

	# 	# Get the number of segments present in a randomly selected virus.
	# 	v = self.GetRandomVirus()
	# 	num_segments = len(v.GetSegments())

	# 	# Initialize a dictionary that will contain the list of segments. Make sure
	# 	# the dictionary contains a key for each element present, and initialize the
	# 	# value to be an empty list.
	# 	segments = dict()
	# 	for i in range(num_segments):
	# 		segments[i] = []
		
	# 	# Iterate through all the viruses present in the sampled set. Append each
	# 	# segment to the appropriate list.
	# 	for virus in self.GetSampledViruses():
	# 		for i in range(num_segments):
	# 			virus_id = "%s_%s" % (str(virus.GetID()), str(virus.GetCreationDate()))
	# 			record = SeqRecord(Seq(virus.GetSegment(i).GetSequence().GetString()),\
	# 				id=str(virus.GetID()), description=str(virus.GetCreationDate()))
	# 			segments[i].append(record)

	# 	# Write the sequences to file with the current date and time present.
	# 	# current_time = datetime.now()
	# 	for i in range(num_segments):
	# 		num_sequences = len(segments[i])
	# 		SeqIO.write(segments[i], "%s/Run %s Simulation Segment %s Sequences.fasta" % \
	# 			(self.directory_prefix, run_number, i), "fasta")

	# def GenerateNetwork(self):
	# 	G = nx.MultiDiGraph()
	# 	for virus in self.GetSampledViruses():
	# 		# print virus
	# 		parent = virus.GetParent()
	# 		child = virus.GetID()
	# 		# print parent, child
	# 		if parent == None:
	# 			G.add_node(child)
	# 		elif len(parent) == 2:
	# 			G.add_edge(parent[0], child, weight=0.5)
	# 			G.add_edge(parent[1], child, weight=0.5)
	# 		elif type(parent) != None:
	# 			G.add_edge(parent, child, weight=1)
	# 	return G

	# def GenerateNetworkVisualization(self, G):
	# 	nx.draw_circular(G)