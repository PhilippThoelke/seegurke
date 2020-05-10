class Qwirkle:
	def __init__(self, title, cell_size=60):
		self.blocks = {}
		self.title = title
		self.cell_size = cell_size

	def rows(self):
		if len(self.blocks) == 0:
			return 6
		return max(key[0] for key in self.blocks.keys()) + 10

	def cols(self):
		if len(self.blocks) == 0:
			return 6
		return max(key[1] for key in self.blocks.keys()) + 10

	def test(self, arg):
		print(arg)

	def __getitem__(self, idx):
		if idx in self.blocks:
			return True
		return False

	def __repr__(self):
		return f'Qwirkle(title={self.title}, num_blocks={len(self.blocks)})'
