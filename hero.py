from math import sqrt
from time import time


def perform(func):
	def wrap(*args, **kwargs):
		tt = time()
		if not kwargs:
			kwargs = {}
		res = func(*args, **kwargs)
		print(time() - tt)
		return res
	return wrap

@perform
def move(game, Map):
	M = Map(game.board, game.activeHero)
	M.quiet = False
#	x = M.route((0, 0), (4, 4))
#	M.print_route(x)
#	M.print()
	
	x = M.goto('enemies')
	if x is not None:
		return x
	else:
		print(x)

try:
	pragma = __pragma__
	pragma = True
except:
	pragma = False

if pragma:
	__pragma__('ecom')
	#?module.exports = move
	__pragma__('noecom')
