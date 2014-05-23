from id_generator import generate_id

class Controller(object):
	"""
	The controller object is the overall manager for the viral simulation.
	"""
	def __init__(self, environments=None):
		super(Controller, self).__init__()
		
		self.environments = []
		self.current_time = 0

	def create_environment(self, num_hosts=0):
		from environment import Environment
		environment = Environment(num_hosts=num_hosts)

		self.environments.append(environment)

	def create_host(self, environment):
		from host import Host 

		host = Host(environment)

	def create_hosts(self, environment, num_hosts):
		for i in num_hosts:
			self.create_host(environment)

	def seed_viruses_into_hosts(self, environment, num_hosts):
		"""
		This 
		"""