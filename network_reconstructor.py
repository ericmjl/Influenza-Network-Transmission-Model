from Bio import SeqIO
from numpy import median
from random import sample, choice
from copy import deepcopy

import networkx as nx

def compute_edit_distance(string1, string2):
	"""
	This function computes the edit distance between two strings of 
	equal length.
	"""
	distance = 0
	
	if len(string1) != len(string2):
		raise ValueError('The two input strings must be of equal length.')
	else:		
		for n, i in enumerate(string1):
			if string2[n] != i:
				distance += 1
			
	return distance

def get_id(seqrecord):
	"""
	This function returns the ID from the SeqRecord description.
	"""
	sequence_id = seqrecord.description.split(' ')[0]
	return sequence_id

def get_date(seqrecord):
	"""
	This function returns the virus creation date from the SeqRecord description.
	"""
	sequence_date = seqrecord.description.split(' ')[1]
	return sequence_date

def add_nodes_from_records(graph, records):
	"""
	This function takes in a graph and a list of SeqRecord objects. 

	The SeqRecord objects should have at least an ID and a Date (in that order), 
	separated by a " " (space) character. See the "get_id" and "get_date" functions
	above.

	It then adds each SeqRecord as a node in the graph.
	"""
	for record in records:
		date = get_date(record)
		id = get_id(record)
		# print id, date
		graph.add_node(id, date=date)

def add_edges_from_records(graph, records, segment):
	"""
	This function will construct a fully connected graph between all pairs of nodes,
	for a particular segment, and will compute the pair-wise identity (PWI) for each
	edge.

	It takes in a graph, a list of SeqRecord objects, and an integer number.

	Basically, it will create a segment transmission graph.
	"""
	for n1, record1 in enumerate(records):
		for n2, record2 in enumerate(records):
			if n1 != n2:
				edit_distance = compute_edit_distance(record1.seq, record2.seq)
				weight = 1 - float(edit_distance) / len(record1.seq)

				graph.add_edge(get_id(record1), get_id(record2), segment=segment, \
					distance=edit_distance, weight=weight)

def remove_edges_below_threshold(graph, threshold):
	"""
	This function removes edges in a graph that have a weight below a specified
	threshold value.
	"""
	for node in graph.nodes():
		in_edges = graph.in_edges(node, data=True)
		if len(in_edges) > 0:
			for edge in in_edges:
				if edge[2]['weight'] < threshold:
					graph.remove_edge(edge[0], edge[1])

def remove_incorrectly_timed_edges(graph):
	"""
	This function will remove edges that are incorrectly timed. This means that the 
	source node occurred after the sink node.
	"""
	for edge in graph.edges(data=True):
		sinknode = edge[1]
		sourcenode = edge[0]

		sinkdate = int(graph.node[sinknode]['date'])
		sourcedate = int(graph.node[sourcenode]['date'])
		
		if sourcedate > sinkdate:
			graph.remove_edge(sourcenode, sinknode)


def remove_edges_not_max(graph):
	"""
	This function will remove edges that are not the maximum PWI, as computed in the 
	add_edges_from_records function.
	"""
	for node in graph.nodes():
		in_edges = graph.in_edges(node, data=True)
		if len(in_edges) > 0:
			max_weight = max(edge[2]['weight'] for edge in in_edges)
			for edge in in_edges:
				sourcenode = edge[0]
				sinknode = edge[1]
				if edge[2]['weight'] < max_weight:
					graph.remove_edge(sourcenode, sinknode)


def standard_processing(seqrecords, segment):
	"""
	Treat this function as a script that does the standard processing of the data.
	See comments below to make sense of it.
	"""

	# Initialize a graph
	graph = nx.DiGraph()
	# Add in nodes
	add_nodes_from_records(graph, seqrecords)
	# Add in edges between nodes
	add_edges_from_records(graph, seqrecords, segment)
	# Remove incorrectly timed edges
	remove_incorrectly_timed_edges(graph)
	# Remove edges below median PWI. This potentially helps separate two 
	# infections
	matrix_values = nx.adjacency_matrix(graph).flat
	remove_edges_below_threshold(graph, median(matrix_values))
	# Remove edges that are non-maximum.
	remove_edges_not_max(graph)
	return graph

def add_two_graph_overlapping_edges(G0, G1):
	"""
	This function takes in two graphs, and does the following:

	1. Removes edges not present in both graphs.
	2. Sums up the weights for each edge that is present in both graphs.

	Returns: G_all, a graph of the same type as G0.
	"""
	G_all = G0.copy()
	G_all.edges(data=True)
	for edge in G_all.edges():
		if edge not in G1.edges():
			G_all.remove_edge(edge[0], edge[1])

		if edge in G1.edges():
			other_edge_index = G1.edges().index(edge)
			other_edge = G1.edges(data=True)[other_edge_index]

			edge_index = G_all.edges().index(edge)
			edge = G_all.edges(data=True)[edge_index]

			edge[2]['weight'] += other_edge[2]['weight']
			
	return G_all

######## The following functions pertain to measuring accuracy of edge reconstruction ########

def find_transmission_edges(graph, is_ground_truth):
	"""
	This function returns the edges that are "transmissions".
	"""
	if is_ground_truth == True:
		return [(edge[0], edge[1]) for edge in graph.edges(data=True) if edge[2]['weight'] == 1]
	if is_ground_truth == False:
		return [edge for edge in graph.edges()]

def find_transmission_true_positives(ground_truth, reconstruction):
	"""
	This function finds the edges in the transmission reconstruction that are in the ground truth.
	"""
	ground_truth_edges = set(find_transmission_edges(ground_truth, is_ground_truth=True))
	reconstruction_edges = set(find_transmission_edges(reconstruction, is_ground_truth=False))

	transmission_true_positives = ground_truth_edges.intersection(reconstruction_edges)

	return transmission_true_positives

def find_transmission_false_positives(ground_truth, reconstruction):
	"""
	This function finds the edges in the transmission reconstruction that are not in the ground truth.
	"""
	ground_truth_edges = set(find_transmission_edges(ground_truth, is_ground_truth=True))
	reconstruction_edges = set(find_transmission_edges(reconstruction, is_ground_truth=False))

	transmission_false_positives = reconstruction_edges.difference(ground_truth_edges)

	return transmission_false_positives

def find_transmission_false_negatives(ground_truth, reconstruction):
	"""
	This function finds the edges in the ground truth that are not in the transmission reconstruction.
	"""
	ground_truth_edges = set(find_transmission_edges(ground_truth, is_ground_truth=True))
	reconstruction_edges = set(find_transmission_edges(reconstruction, is_ground_truth=False))

	transmission_false_negatives = ground_truth_edges.difference(reconstruction_edges)

	return transmission_false_negatives

def compute_transmission_true_positive_rate(ground_truth, reconstruction):
	"""
	This functions computes the edge true positive rate, defined as:

	TP / TP + FN
	"""
	num_true_positives = len(find_transmission_true_positives(ground_truth, reconstruction))
	num_false_negatives = len(find_transmission_false_negatives(ground_truth, reconstruction))

	transmission_true_positive_rate = float (num_true_positives) / (num_true_positives + num_false_negatives)

	return transmission_true_positive_rate

def compute_transmission_false_positive_fraction(ground_truth, reconstruction):
	"""
	This function computes the fraction of reconstructed edges that are false positives.
	"""
	num_false_positives = len(find_transmission_false_positives(ground_truth, reconstruction))
	num_true_positives = len(find_transmission_true_positives(ground_truth, reconstruction))

	transmission_false_positive_fraction = float(num_false_positives) / (num_false_positives + num_true_positives)

	return transmission_false_positive_fraction


def compute_fraction_of_true_edges_found(ground_truth, reconstruction):
	"""
	This function computes the fraction of ground truth edges found in the reconstruction.
	"""
	ground_truth_edges = find_transmission_edges(ground_truth, is_ground_truth=True)
	true_positives = find_transmission_true_positives(ground_truth, reconstruction)

	fraction_of_true_edges_found = float(len(true_positives)) / float(len(ground_truth_edges))

	return fraction_of_true_edges_found


######## The following functions pertain to generating "null" reconstructed graphs    ########
######## for each simulation run.                                                     ########

def permute_edges(G):
    """
    This function takes in a graph, and permutes the edges between the nodes.
    
    Permuting the edges means guaranteeing the same number of edges, with the same
    edge attributes being present but reassigned to other pairs of nodes.
    
    This preserves the edge composition and number, but mixes up the placement of
    edges.
    """
    
    # Grab nodes and edges data from passed in graph.
    edges = G.edges(data=True)
    nodes = G.nodes()
    num_of_edges = len(edges)

    
    # Initialize new graph by keeping nodes but removing all edges
    new_graph = deepcopy(G)
    new_graph.remove_edges_from(edges)
    
    
    while len(new_graph.edges()) < len(G.edges()):
        # Randomly choose an edge and its attributes
        edge = choice(edges)
        attributes = edge[2]
        # Get index of that edge in the list of edges
        index = edges.index(edge)
        
        # Sample two different nodes from the list of nodes
        node1, node2 = sample(nodes, 2)
        
        # If the edge is not already present in the new graph,
        # add it to the graph with the chosen edge's attributes.
        if (node1, node2) not in new_graph.edges():
            new_graph.add_edge(node1, node2, attributes)
            edges.pop(index)
    
    return new_graph

######## The following functions pertain to measuring accuracy of reassortant finding ########

def find_reassortants(graph, is_ground_truth):
	if is_ground_truth == True:
		return [node for node in graph.nodes() if len(graph.in_edges(node)) == 2]

	if is_ground_truth == False:
		return [node for node in graph.nodes() if len(graph.in_edges(node)) == 0]

def find_non_reassortants(graph):
	return [node for node in graph.nodes() if len(graph.in_edges(node)) == 1]


def find_reassortant_true_positives(ground_truth, reconstruction):
	ground_truth_reassortants = find_reassortants(ground_truth, is_ground_truth=True)
	reconstruction_reassortants = find_reassortants(reconstruction, is_ground_truth=False)

	true_positives = set(ground_truth_reassortants).intersection(set(reconstruction_reassortants))

	return true_positives

def find_reassortant_false_positives(ground_truth, reconstruction):
	ground_truth_non_reassortants = find_non_reassortants(ground_truth)
	reconstruction_reassortants = find_reassortants(reconstruction, is_ground_truth=False)

	false_positives = set(reconstruction_reassortants).intersection(set(ground_truth_non_reassortants))

	return false_positives

def find_reassortant_true_negatives(ground_truth, reconstruction):
	ground_truth_non_reassortants = find_non_reassortants(ground_truth)
	reconstruction_non_reassortants = find_non_reassortants(reconstruction)

	true_negatives = set(ground_truth_non_reassortants).intersection(set(reconstruction_non_reassortants))

	return true_negatives

def find_reassortant_false_negatives(ground_truth, reconstruction):
	ground_truth_reassortants = find_reassortants(ground_truth, is_ground_truth=True)
	reconstruction_non_reassortants = find_non_reassortants(reconstruction)

	false_negatives = set(ground_truth_reassortants).intersection(set(reconstruction_non_reassortants))

	return false_negatives


def compute_reassortant_true_positive_rate(ground_truth, reconstruction):
	"""
	This function computes the True Positive Rate, given by:
	TP = TP / (TP + FN)
	"""
	num_true_positives = len(find_reassortant_true_positives(ground_truth, reconstruction))
	num_false_negatives = len(find_reassortant_false_negatives(ground_truth, reconstruction))

	if num_true_positives + num_false_negatives == 0:
		return 1
	else:
		return float(num_true_positives)/(num_true_positives + num_false_negatives)

def compute_reassortant_false_positive_rate(ground_truth, reconstruction):
	"""
	This function computes the false positive rate, given by:
	FPR = FP / (FP + TN)
	"""
	num_false_positives = len(find_reassortant_false_positives(ground_truth, reconstruction))
	num_true_negatives = len(find_reassortant_true_negatives(ground_truth, reconstruction))

	if num_false_positives + num_true_negatives == 0:
		return 1
	else:
		return float(num_false_positives) / (num_false_positives + num_true_negatives)




