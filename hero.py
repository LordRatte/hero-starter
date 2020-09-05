from math import sqrt
from time import time
from misc import dumps


def perform(func):
	def wrap(*args, **kwargs):
		tt = time()
		if not kwargs:
			kwargs = {}
		res = func(*args, **kwargs)
		print(time() - tt)
		return res
	return wrap


def do_self_heal(M, well, soul):
	health_source = None
	health_source = health_source if health_source is not None and well.rel_danger < health_source['dist'] else well
	health_source = health_source if health_source is not None and soul.rel_danger < health_source['dist'] else soul
	if health_source is not None:
		M.goto(health_source)

def do_battle(M, enemy):
	ally_weak = M.find('allies', lambda o: o.health < 100)

	if enemy['dist'] is None or (ally_weak['dist'] is not None and ally_weak['dist'] > enemy['dist']):
		return M.goto(ally_dist)
	elif ally_weak['dist'] is None or (enemy['dist'] is not None and ally_weak['dist'] < enemy['dist']):
		return M.goto(enemy)



@perform
def move(game, Map):
	M = Map(game.board, game.activeHero)
	M.quiet = False
	M.quiet and M.print()

	enemy = M.find('enemies', lambda o: not o['dead'])
	well = M.find('wells')
	ally = M.find('allies', lambda o: not o['dead'])
	mine = M.find('mines')
	soul = M.find(['allies', 'enemies'], lambda o: o['dead'])

	if M.myhealth < 60:
		return do_self_heal(M, well, soul)
	
	if enemy['dist'] is not None and enemy['dist'] > (M.size / 3):
		contingency = False
		if mine['dist'] is not None:
			return M.goto(mine)

		if M.myhealth < 100:
			shealth = do_self_heal(M, well, soul)
			if shealth is not None:
				return shealth

	bat = do_battle(M, enemy)
	if bat is not None:
		return bat
		
	return M.goto(mine) or M.goto(well)
		
try:
	pragma = __pragma__
	pragma = True
except:
	pragma = False

if pragma:
	__pragma__('ecom')
	#?module.exports = move
	__pragma__('noecom')
