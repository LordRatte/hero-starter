def move(game, h):
	if game.activeHero.health <= 75:
		return h.health_well()
	return h.weaker_enemy(game) or h.enemy(game)


module.exports = move
