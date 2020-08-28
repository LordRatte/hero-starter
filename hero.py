from math import sqrt

def dumps(o):
	return JSON.stringify(o, None, 2)

def loads(s):
	return JSON.parse(s)


class DangerGrid:
	def __init__(self, board, active_hero):
		self.team = active_hero.team
		self.myid = active_hero.id
		base_grid  = {}
		for r in board.tiles:
			for o in r:
				if o['type'] == 'HealthWell':
					d = -20
				elif o['type'] == 'DiamondMine':
					d = 0
				elif o['type'] == 'Hero':
					if o['team'] == self.team:
						if self.myid != o['id']:
							d = -15
						else:
							d = 0
					else:
						d = 20
				else: #Unoccupied etc.
					d = 0
				if len(o.heroesKilled):
					d += len(o.heroesKilled) * (d/abs(d)) * 3
				base_grid[(o.distanceFromLeft, o.distanceFromTop)] = d
		
		grid = {}
		
		for r in board.tiles:
			for o in r:
				rel_danger = 0
				for k, v in base_grid.items():
					ox, oy = k.split(',')
					distance = self.distance(ox, oy, o.distanceFromLeft, o.distanceFromTop)
					if distance > 0:
						rel_danger += float(v) / (float(distance) )
					else:
						rel_danger += float(v)
				grid[(o.distanceFromLeft, o.distanceFromTop)] = rel_danger
		self.grid = grid

	@staticmethod
	def distance(x1, y1, x2, y2):
		return sqrt(((x1-x2)**2)+((y1-y2)**2))

	def print(self):
		mmax = max(self.grid.values())
		mmin = abs(min(self.grid.values()))
		for x in range(5):
			line = ''
			for y in range(5):
				d = self.grid[(x, y)] + mmin
				line +=  str(int(9*d/(mmax + mmin)))
			print(line)


def move(game, h):
	h.game_data = game
	danger_grid = DangerGrid(game.board, game.activeHero)

	danger_grid.print()	
	
	if game.activeHero.health <= 75:
		print(h.health_well())
		return h.health_well()
	return h.weaker_enemy() or h.enemy()

try:
	pragma = __pragma__
	pragma = True
except:
	pragma = False

if pragma:
	__pragma__('ecom')
	#?module.exports = move
	__pragma__('noecom')
