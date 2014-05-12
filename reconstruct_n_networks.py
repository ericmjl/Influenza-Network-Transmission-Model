from Bio import SeqIO
from network_reconstructor import *

for i in range(500):
	print "Currently reconstructing run %s" % i
	handle0 = 'Simulated Sequences/Run %s Simulation Segment 0 Sequences.fasta' % i
	handle1 = 'Simulated Sequences/Run %s Simulation Segment 1 Sequences.fasta' % i

	segment0s = []
	for sequence in [record for record in SeqIO.parse(handle0, 'fasta')]:
		segment0s.append(sequence)

	segment1s = []
	for sequence in [record for record in SeqIO.parse(handle1, 'fasta')]:
		segment1s.append(sequence)

	G0 = standard_processing(segment0s, segment=0)
	G1 = standard_processing(segment1s, segment=1)

	G_all = add_two_graph_overlapping_edges(G0, G1)
	# remove_edges_not_max(G_all)

	nx.write_gpickle(G_all, 'Reconstructed Networks/Run %s Reconstructed Transmission Tree.gpickle' % i)

	# Create "null" networks.
	G_null = permute_edges(G_all)

	nx.write_gpickle(G_null, 'Reconstructed Networks/Run %s Reconstructed Null Transmission Tree.gpickle' % i)