import random

class GameOverError(Exception):
	""" raised when Game Over """
	def __init__(self, message):
		super(GameOverError, self).__init__(message)

	def __str__(self):
		return self.message

class InvalidInput(Exception):
	""" raised when Game Over """
	def __init__(self, message):
		super(InvalidInput, self).__init__(message)
		

class Board(list):
	"""docstring for Board"""
	def __init__(self):
		for _ in range(3):
			self.append( ["","",""] )
		self.won = None
		self.game_over = False


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


	def __setitem__(self, key, value):
		row, col = key
		print "Setting {},{} to {}".format(row, col, value)
		super(type(self), self).__getitem__(row)[col] = value

		self.check()
		if self.game_over:
			if self.won is not None:
				message = "{} won, congrats!".format(self.won)
			else:
				message = "It was a stalemate. Y'all suck."
			raise GameOverError("Game Over: " + message)


	def __getitem__(self, key):
		row, col = key
		return super(type(self), self).__getitem__(row)[col]


	@classmethod
	def all_same(cls, array):
		''' return true if all elements of the array are the same '''
		for e in array:
			if e != array[0]: return False
		return len(e) > 0


	def positions(self):
		''' generator to iterate over (index, value) tuples '''
		for row_i in range(3):
			for col_i in range(3):
				yield (row_i, col_i), self[row_i,col_i]


	def board_full(self):
		for (_, _), element in self.positions():
				if len(element) > 0: return False
		return True


	def valid_guesses(self):
		v_g = []
		for (row, col), element in self.positions():
			if len(element) == 0:
				v_g.append( (row, col) )
		return v_g


	def check(self):
		''' check for victory
			return True if the game is over (someone won, or board full)
		'''
		print "checking"
		# check rows
		for row in self:
			if self.all_same(row):
				self.won = row[0]
				self.game_over = True
				return

		# check cols
		for col_i in range(3):
			col = (self[0,col_i], self[1,col_i], self[2,col_i],)
			if self.all_same(col):
				self.won = col[0]
				self.game_over = True
				return

		# check diags
		diag1 = (self[0,0], self[1,1], self[2,2])
		if self.all_same(diag1):
			self.won = diag1[0]
			self.game_over = True
			return

		diag2 = (self[0,2], self[1,1], self[2,0])
		if self.all_same(diag2):
			self.won = diag2[0]
			self.game_over = True
			return
		
		if self.board_full():
			# stalemate
			self.game_over = True
			return

		self.game_over = False


	def make_random_move(self, user):
		''' given a user, have them move to a random spot on the board '''
		x, y = random.choice( self.valid_guesses() )
		self[x,y] = user



b = Board()
for i in range(3):
	b[0,i] = 'a'
	print b
	print "\n"
