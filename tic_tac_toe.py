

class Board(list):
	"""docstring for Board"""
	def __init__(self):
		for _ in range(3):
			self.append( ["","",""] )
		self.won = None

	@staticmethod
	def hbar():
		return "+-----------+"

	@staticmethod
	def divider():
		return "|---+---+---|"

	@staticmethod
	def row():
		return "| {:^1} | {:^1} | {:^1} |"

	def __str__(self):
		rows = map(lambda x: self.row().format(*x), self)
		pretty_board = (self.hbar(), rows[0], self.divider(), rows[1], self.divider(), rows[2], self.hbar())
		return "\n".join(pretty_board)

	@classmethod
	def all_same(cls, array):
		''' return true if all elements of the array are the same '''
		for e in array:
			if e != array[0]: return False
		return True

	def check(self):
		''' check for victory '''
		# check rows
		for row in self:
			if self.all_same(row):
				self.won = row[0]
				print("{} won".format(self.won))

		# check cols
		for col_i in range(3):
			col = (self[0][col_i], self[1][col_i], self[2][col_i],)
			if self.all_same(col):
				self.won = col[0]
				print("{} won".format(self.won))

		# check diags
		diag1 = (self[0][0], self[1][1], self[2][2])
		if self.all_same(diag1):
			self.won = diag1[0]
			print("{} won".format(self.won))

		diag2 = (self[0][2], self[1][1], self[2][0])
		if self.all_same(diag2):
			self.won = diag2[0]
			print("{} won".format(self.won))

	def __setitem__(self, key, value):
		super(type(self), self).__setitem__(key, value)
		self.check()



b = Board()
for i in range(3):
	b[0][i] = 'a'
print b
b.check()
print b.won
