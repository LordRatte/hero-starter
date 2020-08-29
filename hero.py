def move(game, Map):
	M = Map(game.board, game.activeHero)

	M.print()	
	return 'East'	

try:
	pragma = __pragma__
	pragma = True
except:
	pragma = False

if pragma:
	__pragma__('ecom')
	#?module.exports = move
	__pragma__('noecom')
