from environment import Environment
from sampler import Sampler
from random import randint, random
from numpy.random import normal
import networkx as nx 

for i in range(500):
# We allow ourselves to start with between 1 and 3 viruses
	num_viruses = randint(1,4)

	# We allow ourselves to finish with between 20 and 50 viruses
	max_num_viruses = randint(20, 50)

	e = Environment(num_viruses=num_viruses, virus_type='influenza')

	for j in range(max_num_viruses):
		if len(e.GetViruses()) < max_num_viruses:
			
			cointoss = random()

			if cointoss < 0.7:
				virus = e.GetRandomVirus()
				e.ReplicateVirus(virus, date=j)
				e.MutateVirus()

			elif cointoss > 0.3 and len(e.GetViruses()) > 2:
				e.RandomlyReassortTwoViruses(mutate=True, date=i)

		else:
			break

	s = Sampler(directory_prefix='Simulated Reassortant Sequences')
	s.SampleVirusesFromEnvironment(e, 'all')
	s.DumpSequences(run_number=i)
	G = s.GenerateNetwork()
	nx.write_gpickle(G, "Simulated Reassortant Networks/Run %s Transmission Tree.gpickle" % i)
	# s.GenerateNetworkVisualization(G)