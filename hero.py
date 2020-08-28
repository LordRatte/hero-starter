def dumps(o):
	return JSON.stringify(o, None, 2)

class DangerGrid:
	def __init__(self, board, x, y, my_team):
		self.team = my_team


def move(game, h):
	h.game_data = game
	danger_grid = DangerGrid(game.board, game.activeHero.distanceLeft, game.activeHero.distanceLeft, game.activeHero.team)
	if game.activeHero.health <= 75:
		return h.health_well(game)
	return h.weaker_enemy(game) or h.enemy(game)


module.exports = move
