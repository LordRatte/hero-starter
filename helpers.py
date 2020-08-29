from math import sqrt
from misc import Node


def dumps(o):
	return JSON.stringify(o, None, 2)

def loads(s):
	return JSON.parse(s)


class Map:
	def __init__(self, board, active_hero):
		self.team = active_hero.team
		self.myid = active_hero.id
		self.myx = active_hero.distanceFromLeft
		self.myy = active_hero.distanceFromTop
		base_grid  = {}
		self.min =  0
		self.max =  0
		self.wells = []
		self.mines = []
		self.enemies = []
		self.allies = []
		
		for r in board.tiles:
			for o in r:
				d = 0
				dist = self.distance(self.myx, self.myy, o.distanceFromLeft, o.distanceFromLeft)
				o.dist = dist
				if o['type'] == 'HealthWell':
					d = -20
					self.wells.append(o)
				elif o['type'] == 'DiamondMine':
					if not ['team'] == self.team:
						self.mines.append(o)
				elif o['type'] == 'Hero':
					if o['team'] == self.team:
						if self.myid != o['id']:
							self.allies.append(o)
							d = -15
						else:
							d = 0
					else:
						self.enemies.append(o)
						d = 20
				if len(o.heroesKilled):
					d += len(o.heroesKilled) * (d/abs(d)) 
				base_grid[(o.distanceFromLeft, o.distanceFromTop)] = d
				if d < self.min:
					self.min = d
				if d > self.max:
					self.max = d
		self.min = abs(self.min)	
		self.wells.sort(lambda o: o.dist)
		self.mines.sort(lambda o: o.dist)
		self.enemies.sort(lambda o: o.dist)
		self.allies.sort(lambda o: o.dist)
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
				if o['type'] in ['Unoccupied']:
					o.wall = False
				else:
					o.wall = True
				grid[(o.distanceFromLeft, o.distanceFromTop)] = o
				grid[(o.distanceFromLeft, o.distanceFromTop)].rel_danger = rel_danger 
		self.grid = grid

	@staticmethod
	def distance(x1, y1, x2, y2):
		return sqrt(((x1-x2)**2)+((y1-y2)**2))

	@staticmethod
	def get_segment_dir(route, seg=0):
		x1, y1 = route[seg]
		x2, y2 = route[seg+1]
		dx = x2 - x1
		dy = y2 - y1
		if dx == 0 and dy == -1:
			return 'North'
		elif dx == 1 and dy == 0:
			return 'East'
		elif dx == 0 and dy == 1:
			return 'South'
		elif dx == -1 and dy == 0:
			return 'West'
		else:
			print(roue[seg], route[seg+1])
			return 'Stay'

	def print_route(self, route):
		size = sqrt(len(self.grid))
		for x in reversed(range(size)):
			line = ''
			for y in range(size):
				if any([x==xx and y==yy for xx,yy in route]):
					line += 'x'
				else:
					line += ' '	
			print(line)

	def print(self):
		mmax = self.max
		mmin = self.min
		size = sqrt(len(self.grid))
		for x in reversed(range(size)):
			line = ''
			for y in range(size):
				if self.grid[(x, y)]['type'] == 'Unoccupied':
					d = self.grid[(x, y)].rel_danger + mmin
					line +=  str(int(9*d/(mmax + mmin)))
				else:
					line += '#'
			print(line)
		print('wells: ' + len(self.wells))
		print('unowned mines: ' + len(self.mines))
		print('enemies: ' + len(self.enemies))
		print('allies: ' + len(self.allies))


	def route(self, start, end):
		''' A* (star) Pathfinding
		'''
		def return_path(current_node):
			path = []
			current = current_node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return reversed(path)
		
		start_node = Node(None, tuple(start))
		start_node.g = start_node.h = start_node.f = 0
		end_node = Node(None, tuple(end))
		end_node.g = end_node.h = end_node.f = 0

		# Initialize both open and closed list
		open_list = []
		closed_list = []

		open_list.append(start_node)

		# Adding a stop condition
		outer_iterations = 0
		max_iterations = len(self.grid) 

		# what squares do we search
		adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
		# Loop until you find the end
		while len(open_list) > 0:
			outer_iterations += 1

			if outer_iterations > max_iterations:
				return None
				# if we hit this point return the path such as it is
				# it will not contain the destination
				#return return_path(current_node)       
			
			# Get the current node
			open_list.sort(lambda a: a.f)
			current_node = open_list.pop(0)
			closed_list.append(current_node)

			# Found the goal
			if current_node.__eq__(end_node):
				return return_path(current_node)

			# Generate children
			children = []
			
			for new_position in adjacent_squares: # Adjacent squares

				# Get node position
				node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

				# Make sure within range
				if node_position not in self.grid:
					continue


				# Make sure walkable terrain
				if self.grid[node_position].wall and not (node_position[0] == end[0] and node_position[1] == end[1] ): 
					continue

				# Create new node
				new_node = Node(current_node, node_position)

				# Append
				children.append(new_node)

			# Loop through children
			for child in children:
				# Child is on the closed list
				if len([closed_child for closed_child in closed_list if closed_child.__eq__(child)]) > 0:
					continue

				cost = (self.grid[child.position].rel_danger + self.min)/self.max
				# Create the f, g, and h values
				child.g = current_node.g + cost
				child.h = self.distance(child.position[0], child.position[1], end_node.position[0], end_node.position[1])
				child.f = child.g + child.h

				# Child is already in the open list
				if len([open_node for open_node in open_list if child.__eq__(open_node) and child.g > open_node.g]) > 0:
					continue

				# Add the child to the open list
				open_list.append(child)

		return None	

	def goto(self, thing, filt=lambda o: True):
		valid = ['mines', 'wells', 'enemies', 'allies']
		if thing in valid:
			for othing in self[thing]:
				if filt(othing):
					break
			else:
				return None
			dest = (othing.distanceFromLeft, othing.distanceFromTop)
			route = self.route((self.myx, self.myy), dest)
			if route is not None:
				if not self.quiet:
					self.print_route(route)
				return self.get_segment_dir(route)
		else:
			print('Thing must be one of ' + valid)
try:
	pragma = __pragma__
	pragma = True
except:
	pragma = False

if pragma:
	__pragma__ ('ecom')
	#?module.exports = Map
	__pragma__ ('noecom')
