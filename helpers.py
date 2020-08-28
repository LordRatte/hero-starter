class Helpers:
 
	@classmethod
	def valid_coord(cls, board, distance_from_top, distance_from_left):
		''' Returns false if the given coordinates are out of range
		'''
		return (not (distance_from_top < 0 or distance_from_left < 0 or
		  distance_from_top > board.lengthOfSide - 1 or distance_from_left > board.lengthOfSide - 1))

	@classmethod
	def get_tile_nearby(cls, board, distance_from_top, distance_from_left, direction): 
		''' Returns the tile [direction] (North, South, East, or West) of the given X/Y coordinate
		'''
		# These are the X/Y coordinates
		from_top_new = distance_from_top
		from_left_new = distance_from_left

		# This associates the cardinal directions with an X or Y coordinate
		if direction == 'North':
			from_top_new -= 1
		elif direction == 'East':
			from_left_new += 1
		elif (direction == 'South'): 
			from_top_new += 1
		elif direction == 'West':
			from_left_new -= 1
		else:
			return False		

		# If the coordinates of the tile nearby are valid, return the tile object at those coordinates
		if cls.valid_coord(board, from_top_new, from_left_new):
			return board.tiles[from_top_new][from_left_new]
		else:
			return False

	@classmethod
	def object_direction_and_distance(cls, board, from_tile, tile_callback):
		''' Returns an object with certain properties of the nearest object we are looking for
		'''
		# Storage queue to keep track of places the from_tile has been
		queue = []

		# Keeps track of places the from_tile has been for constant time lookup later
		visited = {}

		# Variable assignments for from_tile's coordinates
		dft = from_tile.distanceFromTop
		dfl = from_tile.distanceFromLeft

		# Stores the coordinates, the direction from_tile is coming from, and it's location
		visit_info = (dft, dfl, 'None', 'START')

		# Just a unique way of storing each location we've visited
		visited[dft + '|' + dfl] = True

		# Push the starting tile on to the queue
		queue.append(visit_info)

		# While the queue has a length
		while len(queue):

			# Shift off first item in queue
			coords = queue.pop(0)

			# Reset the coordinates to the shifted object's coordinates
			dft, dfl = coords[0], coords[1]

			# Loop through cardinal directions
			directions = ('North', 'East', 'South', 'West')
			for i, direction in enumerate(directions):

				# For each of the cardinal directions get the next tile...
				# ...Use the get_tile_nearby helper method to do this
				next_tile = cls.get_tile_nearby(board, dft, dfl, direction)

				# If next_tile is a valid location to move...
				if next_tile:

					# Assign a key variable the next_tile's coordinates to put into our visited object later
					key = next_tile.distanceFromTop + '|' + next_tile.distanceFromLeft

					is_goal_tile = False
					try:
						is_goal_tile = tile_callback(next_tile)
					except Exception as err:
						is_goal_tile = False

					# If we have visited this tile before
					if key in visited:
						# Do nothing--this tile has already been visited
						pass
					# Is this tile the one we want?
					elif is_goal_tile:
						# This variable will eventually hold the first direction we went on this path
						correct_direction = direction

						# This is the distance away from the final destination that will be incremented in a bit
						distance = 1

						# These are the coordinates of our target tile_type
						final_coords = (next_tile.distanceFromTop, next_tile.distanceFromLeft)

						# Loop back through path until we get to the start
						while not (coords[3] == 'START'):
							# Haven't found the start yet, so go to previous location
							correct_direction = coords[2]

							# We also need to increment the distance
							distance += 1

							# And update the coords of our current path
							coords = coords[3]

						# Return object with the following pertinent info
						goal_tile = next_tile
						goal_tile.direction = correct_direction
						goal_tile.distance = distance
						goal_tile.coords = final_coords
						return goal_tile

					# If the tile is unoccupied, then we need to push it into our queue
					elif next_tile.type == 'Unoccupied':
						queue.push((next_tile.distanceFromTop, next_tile.distanceFromLeft, direction, coords))

						# Give the visited object another key with the value we stored earlier
						visited[key] = True
		# If we are blocked and there is no way to get where we want to go, return false
		return False

	@classmethod
	def non_team_diamond_mine(cls):
		''' Returns the direction of the nearest non-team diamond mine or false, if there are no diamond mines
		'''
		hero = cls.game_data.activeHero
		board = cls.game_data.board
		
		def func(mine_tile):
			if mine_tile.type == 'DiamondMine':
				if mine_tile.owner:
					return mine_tile.owner.team != hero.team
				else:
					return True
			else:
				return False

		# Get the path info object
		path_info_object = cls.object_direction_and_distance(board, hero, func, board)

		# Return the direction that needs to be taken to achieve the goal
		return path_info_object.direction

	@classmethod
	def unowned_diamond_mine(cls):
		''' Returns the nearest unowned diamond mine or false, if there are no diamond mines
		'''
		hero = cls.game_data.activeHero
		board = cls.game_data.board
		def func(mine_tile):
			if mine_tile.type == 'DiamondMine':
				if mine_tile.owner:
					return mine_tile.owner.id != hero.id
				else:
					return True
			else:
				return False

		# Get the path info object
		path_info_object = cls.object_direction_and_distance(board, hero, func)

		# Return the direction that needs to be taken to achieve the goal
		return path_info_object.direction

	@classmethod
	def health_well(cls):
		''' Returns the nearest health well or false, if there are no health wells
		'''
		hero = cls.game_data.activeHero
		board = cls.game_data.board

		def func(health_well_tile):
			return health_well_tile.type == 'Health_well'

		# Get the path info object
		path_info_object = cls.object_direction_and_distance(board, hero, func)

		# Return the direction that needs to be taken to achieve the goal
		return path_info_object.direction

	@classmethod
	def weaker_enemy(cls):
		''' Returns the direction of the nearest enemy with lower health
			(or returns false if there are no accessible enemies that fit this description)
		'''
		hero = cls.game_data.activeHero
		board = cls.game_data.board

		def func(enemy_tile):
			return enemy_tile.type == 'Hero' and enemy_tile.team != hero.team and enemy_tile.health < hero.health

		# Get the path info object
		path_info_object = cls.object_direction_and_distance(board, hero, func)
		# Return the direction that needs to be taken to achieve the goal
		# If no weaker enemy exists, will simply return undefined, which will
		# be interpreted as "Stay" by the game object
		return path_info_object.direction

	@classmethod
	def enemy(cls):
		''' Returns the direction of the nearest enemy
			(or returns false if there are no accessible enemies)
		'''
		hero = cls.game_data.activeHero
		board = cls.game_data.board
		def func(enemy_tile):
			return enemy_tile.type == 'Hero' and enemy_tile.team != hero.team

		# Get the path info object
		path_info_object = cls.object_direction_and_distance(board, hero, func)

		# Return the direction that needs to be taken to achieve the goal
		return path_info_object.direction

	# Returns the direction of the nearest friendly champion
	# (or returns false if there are no accessible friendly champions)
	@classmethod
	def team_member(cls):
		hero = cls.game_data.activeHero
		board = cls.game_data.board

		def func(hero_tile):
			return hero_tile.type == 'Hero' and hero_tile.team == hero.team

		# Get the path info object
		path_info_object = cls.object_direction_and_distance(board, hero, func)

		# Return the direction that needs to be taken to achieve the goal
		return path_info_object.direction

__pragma__ ('ecom')
#?module.exports = Helpers
__pragma__ ('noecom')
