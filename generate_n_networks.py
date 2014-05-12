from environment import Environment
from sampler import Sampler
from random import randint
import networkx as nx 

for i in range(500):
# We allow ourselves to start with between 1 and 3 viruses
	num_viruses = randint(1,4)

	# We allow ourselves to finish with between 20 and 50 viruses
	max_num_viruses = randint(20, 50)

	e = Environment(num_viruses=num_viruses, virus_type='influenza')

	for j in range(max_num_viruses):
		if len(e.GetViruses()) < max_num_viruses:
			virus = e.GetRandomVirus()
			e.ReplicateVirus(virus, date=j)
			e.MutateVirus()
		else:
			break

	s = Sampler()
	s.SampleVirusesFromEnvironment(e, 'all')
	s.DumpSequences(run_number=i)
	G = s.GenerateNetwork()
	nx.write_gpickle(G, "Simulated Networks/Run %s Transmission Tree.gpickle" % i)