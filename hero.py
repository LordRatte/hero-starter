def move(game, h):
	return h.weaker_enemy(game) or h.enemy(game)


module.exports = move
