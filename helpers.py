from math import sqrt

def dumps(o):
	return JSON.stringify(o, None, 2)

def loads(s):
	return JSON.parse(s)


class Map:
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
				grid[(o.distanceFromLeft, o.distanceFromTop)] = o
				grid[(o.distanceFromLeft, o.distanceFromTop)].rel_danger = rel_danger 
		self.grid = grid

	@staticmethod
	def distance(x1, y1, x2, y2):
		return sqrt(((x1-x2)**2)+((y1-y2)**2))

	def print(self):
		mmax = max(o.rel_danger for o in self.grid.values())
		mmin = abs(min(o.rel_danger for o in self.grid.values()))
		for x in reversed(range(5)):
			line = ''
			for y in range(5):
				if self.grid[(x, y)]['type'] == 'Unoccupied':
					d = self.grid[(x, y)].rel_danger + mmin
					line +=  str(int(9*d/(mmax + mmin)))
				else:
					line += '#'
			print(line)

	def route(self, source, target):
		pass


try:
	pragma = __pragma__
	pragma = True
except:
	pragma = False

if pragma:
	__pragma__ ('ecom')
	#?module.exports = Map
	__pragma__ ('noecom')
