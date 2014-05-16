class FluVirus(Virus):
	"""docstring for FluVirus"""
	def __init__(self, id, creation_date, num_segments=2, parent=None, \
		generate_sequence=False):

		Virus.__init__(self, id=id, creation_date=creation_date, \
			num_segments=num_segments, parent=parent, \
			generate_sequence=generate_sequence)