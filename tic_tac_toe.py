import random
from time import sleep

class GameOverError(Exception):
	""" raised when Game Over """
	def __init__(self, message):
		super(GameOverError, self).__init__(message)

	def __str__(self):
		return self.message

class InvalidInputError(Exception):
	""" raised when Game Over """
	def __init__(self, message):
		super(InvalidInputError, self).__init__(message)
		

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

		if len( self[row, col] ) > 0:
			raise InvalidInputError("This spot has already been played.")

		if not isinstance(value, str):
			raise InvalidInputError("You must enter a string as input.")

		if len(value) != 1:
			raise InvalidInputError("Your string must be of length 1.")

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


	def valid_guesses(self):
		v_g = []
		for (row, col), element in self.positions():
			if len(element) == 0:
				v_g.append( (row, col) )
		return v_g

	def board_full(self):
		return len(self.valid_guesses()) == 0


	def check(self):
		''' check for victory
			return True if the game is over (someone won, or board full)
		'''
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
			print "stalemate"
			self.game_over = True
			return

		self.game_over = False


class RandomUser(object):
	"""make random legal moves"""
	def __init__(self, name):
		self.name = name

	def move(self, board):
		x, y = random.choice( board.valid_guesses() )
		board[x,y] = self.name


class HumanUser(object):
	""" prompt the human for input """
	def __init__(self, name):
		self.name = name

	def move(self, board):
		print(board)
		print('\n')
		print("It's {}'s turn!".format(self.name))
		x,y=None, None
		while (x,y) not in board.valid_guesses():
			x, y = self.parse_move()
		board[x,y] = self.name

	def parse_move(self):
		s = raw_input("Enter a valid move: ")
		a,b = s.split(',')
		return int(a), int(b)
		
		

def Play(player1, player2):
	''' play two users against one another '''
	b= Board()
	players = [player1, player2]
	random.shuffle(players)
	try:
		while not b.game_over:
			for player in players:
				player.move(b)

	except GameOverError as e:
		print(e)
		print(b)


Play(RandomUser('x'), HumanUser('o'))


