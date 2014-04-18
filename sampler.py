from environment import Environment
from random import sample

class Sampler(object):
	"""docstring for Sampler"""
	def __init__(self):
		super(Sampler, self).__init__() 
		self.sampled_viruses = []

	def SampleVirusesFromEnvironment(self, environment, n):
		"""
		This method takes in an Environment and samples n viruses from 
		it.
		"""
		if not isinstance(n, int) or n < 0:
			print "ERROR: Please change n to an integer number greater than \
					zero."

		if not isinstance(environment, Environment):
			print "ERROR: You have not specified an environment to sample \
					viruses from."

		else:
			viruses = environment.GetViruses()

			if n >= len(viruses):
				print "ERROR: The number of viruses that you want to sample \
						is greater than the number of viruses present."

			else:
				self.sampled_viruses.extend(sample(viruses, n))

	def GetSampledViruses(self):
		"""This method returns the viruses sampled from the environment."""
		return self.sampled_viruses