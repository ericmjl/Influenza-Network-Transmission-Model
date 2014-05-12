from Bio import SeqIO
from network_reconstructor import *




for i in range(500):

	print "Currently on run %s" % i

	handle0 = 'Simulated Reassortant Sequences/Run %s Simulation Segment 0 Sequences.fasta' % i
	handle1 = 'Simulated Reassortant Sequences/Run %s Simulation Segment 1 Sequences.fasta' % i

	segment0s = [record for record in SeqIO.parse(handle0, 'fasta')]
	segment1s = [record for record in SeqIO.parse(handle1, 'fasta')]

	G0 = standard_processing(segment0s, segment=0)
	G1 = standard_processing(segment1s, segment=1)

	G_all = add_two_graph_overlapping_edges(G0, G1)

	nx.write_gpickle(G_all, 'Reconstructed Reassortant Networks/Run %s Reconstructed Transmission Tree.gpickle' % i)

	# Create "null" networks.
	G_null = permute_edges(G_all)

	nx.write_gpickle(G_null, 'Reconstructed Reassortant Networks/Run %s Reconstructed Null Transmission Tree.gpickle' % i)