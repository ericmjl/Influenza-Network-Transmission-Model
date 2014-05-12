from network_reconstructor import *
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn
import numpy as np

# Reconstruction Statistics
reconstruction_transmission_true_positive_rates = []
reconstruction_transmission_false_positive_fractions = []
reconstruction_reassortant_true_positive_rates = []
reconstruction_reassortant_false_positive_rates = []

# Null model statistics
null_true_positive_rates = []
null_false_positive_fractions = []
null_reassortant_true_positive_rates = []
null_reassortant_false_positive_rates = []
# Reassortant Statistics

total_runs = 500

for i in range(total_runs):
	handle1 = 'Simulated Reassortant Networks/Run %s Transmission Tree.gpickle' % i
	handle2 = 'Reconstructed Reassortant Networks/Run %s Reconstructed Transmission Tree.gpickle' % i
	handle3 = 'Reconstructed Reassortant Networks/Run %s Reconstructed Null Transmission Tree.gpickle' % i

	ground_truth = nx.read_gpickle(handle1)
	reconstruction = nx.read_gpickle(handle2)
	null = nx.read_gpickle(handle3)
	# Step 1: Compute Edge Statistics
	# Part (a): Compute transmission true positive rate
	reconstruction_transmission_true_positive_rates.append(compute_transmission_true_positive_rate(ground_truth, reconstruction))
	null_true_positive_rates.append(compute_transmission_true_positive_rate(ground_truth, null))
	# Part (b): Compute fraction of edges that are false positives
	reconstruction_transmission_false_positive_fractions.append(compute_transmission_false_positive_fraction(ground_truth, reconstruction))
	null_false_positive_fractions.append(compute_transmission_false_positive_fraction(ground_truth, null))
	
	# Step 2: Compute Reassortant Statistics
	# Part (a): Compute reassortant true positive rate
	reconstruction_reassortant_true_positive_rates.append(compute_reassortant_true_positive_rate(ground_truth, reconstruction))
	null_reassortant_true_positive_rates.append(compute_reassortant_true_positive_rate(ground_truth, null))
	# Part (b): Compute reassortant false positive rate
	reconstruction_reassortant_false_positive_rates.append(compute_reassortant_false_positive_rate(ground_truth, reconstruction))
	null_reassortant_false_positive_rates.append(compute_reassortant_false_positive_rate(ground_truth, null))
# Plot transmission true positive rate histogram

plt.figure(0)
bins = np.histogram(np.hstack((reconstruction_transmission_true_positive_rates, null_true_positive_rates)), bins=50)[1] #get the bin edges
plt.hist(reconstruction_transmission_true_positive_rates, bins=bins, alpha=0.75, label='Reconstruction')
plt.hist(null_true_positive_rates, bins=bins, alpha=0.75, label='Null Model')
plt.legend()
plt.xlabel('Transmission True Positive Rate')
plt.ylabel('Count')
plt.title('Transmission True Positive Rate Histogram')
plt.xlim(0, 1)
plt.savefig('Reassortant - Transmission True Positive Rate Histogram.pdf')

# Plot transmission false positive fraction
plt.figure(1)
bins = np.histogram(np.hstack((reconstruction_transmission_false_positive_fractions, null_false_positive_fractions)), bins=50)[1] #get the bin edges
plt.hist(reconstruction_transmission_false_positive_fractions, bins=bins, alpha=0.75, label='Reconstruction')
plt.hist(null_false_positive_fractions, bins=bins, alpha=0.75, label='Null Model')
plt.legend()
plt.xlabel('Transmission False Positive Fraction')
plt.ylabel('Count')
plt.title('Transmission False Positive Fraction Histogram')
plt.xlim(0, 1)
plt.savefig('Reassortant - Transmission False Positive Fraction Histogram.pdf')

# Plot histogram of true positive rate vs false positive fraction
plt.figure(2)
plt.scatter(reconstruction_transmission_false_positive_fractions, reconstruction_transmission_true_positive_rates, \
	color='blue', alpha=0.5, label='Reconstruction')
plt.scatter(null_false_positive_fractions, null_true_positive_rates, \
	color='green', alpha=0.5, label='Null Model')
plt.legend()
plt.xlabel('False Positive Fraction')
plt.ylabel('True Positive Rate')
plt.title('True Positive Rate vs. False Positive Fraction')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
plt.savefig('Reassortants - Transmission TPR vs FPF Scatter Plot.pdf')
# Plot reassortant finder ROC scatterplot
plt.figure(3)
plt.scatter(reconstruction_reassortant_false_positive_rates, reconstruction_reassortant_true_positive_rates, \
	color='blue', alpha=0.5, label='Reconstruction')
plt.scatter(null_reassortant_false_positive_rates, null_reassortant_true_positive_rates, \
	color='green', alpha=0.5, label='Null Model')
plt.legend()
plt.xlabel('Reassortant False Pos_itive Rate')
plt.ylabel('Reassortant True Positive Rate')
plt.title('Reassortant Identification Accuracy')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
plt.savefig('Reassortant - Identification Accuracy.pdf')

