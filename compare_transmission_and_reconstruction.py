from network_reconstructor import *
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn
import numpy as np

# Reconstruction Statistics
transmission_true_positive_rates = []
transmission_false_positive_fractions = []

# Null model statistics
null_true_positive_rates = []
null_false_positive_fractions = []

total_runs = 500

for i in range(total_runs):
	handle1 = 'Simulated Networks/Run %s Transmission Tree.gpickle' % i
	handle2 = 'Reconstructed Networks/Run %s Reconstructed Transmission Tree.gpickle' % i
	handle3 = 'Reconstructed Networks/Run %s Reconstructed Null Transmission Tree.gpickle' % i

	ground_truth = nx.read_gpickle(handle1)
	reconstruction = nx.read_gpickle(handle2)
	null = nx.read_gpickle(handle3)

	# Step 1: Compute Edge Statistics
	# Part (a): Compute transmission true positive rate
	transmission_true_positive_rates.append(compute_transmission_true_positive_rate(ground_truth, reconstruction))
	null_true_positive_rates.append(compute_transmission_true_positive_rate(ground_truth, null))

	# Part (b): Compute fraction of edges that are false positives
	transmission_false_positive_fractions.append(compute_transmission_false_positive_fraction(ground_truth, reconstruction))
	null_false_positive_fractions.append(compute_transmission_false_positive_fraction(ground_truth, null))
# Plot transmission true positive rate histogram
plt.figure(0)
bins = np.histogram(np.hstack((transmission_true_positive_rates, null_true_positive_rates)), bins=50)[1] #get the bin edges
plt.hist(transmission_true_positive_rates, bins=bins, alpha=0.75, label='Reconstruction')
plt.hist(null_true_positive_rates, bins=bins, alpha=0.75, label='Null Model')
plt.legend(loc='best')
plt.xlabel('Transmission True Positive Rate')
plt.ylabel('Count')
plt.title('Transmission True Positive Rate Histogram')
plt.xlim(0, 1)
plt.savefig('No Reassortants - Transmission True Positive Rate Histogram.pdf')

# Plot transmission false positive fraction
plt.figure(1)
bins = np.histogram(np.hstack((transmission_false_positive_fractions, null_false_positive_fractions)), bins=50)[1] #get the bin edges
plt.hist(transmission_false_positive_fractions, bins=bins, alpha=0.75, label='Reconstruction')
plt.hist(null_false_positive_fractions, bins=bins, alpha=0.75, label='Null Model')
plt.legend(loc='best')
plt.xlabel('Transmission False Positive Fraction')
plt.ylabel('Count')
plt.title('Transmission False Positive Fraction Histogram')
plt.xlim(0, 1)
plt.savefig('No Reassortants - Transmission False Positive Fraction Histogram.pdf')

# Plot histogram of true positive rate vs false positive fraction
plt.figure(2)
plt.scatter(transmission_false_positive_fractions, transmission_true_positive_rates, color='blue', alpha=0.5, \
	label='Reconstruction')
plt.scatter(null_false_positive_fractions, null_true_positive_rates, color='green', alpha=0.5,\
	label='Null Model')
plt.legend()
plt.xlabel('False Positive Fraction')
plt.ylabel('True Positive Rate')
plt.title('True Positive Rate vs. False Positive Fraction')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
plt.savefig('No Reassortants - Transmission TPR vs FPF Scatter Plot.pdf')