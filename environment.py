from virus import Virus
from random import choice, sample, randint
from collections import defaultdict
from numpy.random import normal, binomial
from host import Host
from id_generator import generate_id
import networkx as nx


class Environment(object):
	"""
	The Environment class is the second highest level object in the viral 
	simulator. Metaphorically, the Environment class can represent a 
	geographic location where Host objects interact with each other, and in 
	the process, pass viruses from one host to the next.

	In the Environment class, Sampler objects can also interact with Host
	objects, to simulate the process of sampling pathogens from the Host.

	Multiple Environment objects can exist in a particular simulation, allowing
	a host to move from Environment to Environment. This allows one to 
	simulate the spread of Viruses from one Environment to another, by means 
	of Hosts moving between them.
	"""

	def __init__(self, num_hosts=0):
		"""Initialize the environment."""
		super(Environment, self).__init__()

		self.current_time = 0

		self.id = generate_id()
		
		self.hosts = []
		for i in range(num_hosts):
			self.create_host()

	def __repr__(self):
		return "Environment %s with %s hosts." % (self.id, len(self.hosts))

	def create_host(self):
		from host import Host

		h = Host(self)

		return h

	def add_host(self, host):
		from host import Host

		if isinstance(host, Host):
			self.hosts.append(host)
		else:
			raise TypeError('A Host object must be specified!')

	def remove_host(self, host):
		from host import Host

		if isinstance(host, Host):
			self.hosts.pop(self.hosts.index(host))
		elif type(host) == int:
			self.hosts.pop(host)
		else:
			raise TypeError('A Host object or an integer must be specified!')

	def get_infected_hosts(self):
		infected_hosts = [host for host in self.hosts if len(host.viruses) > 0]
		return infected_hosts

	def get_uninfected_hosts(self):
		uninfected_hosts = [host for host in self.hosts if len(host.viruses) == 0]
		return uninfected_hosts

	def get_naive_hosts(self):
		naive_hosts = [host for host in self.hosts if host.was_infected() == False]
		return naive_hosts

		

