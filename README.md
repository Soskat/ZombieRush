# ZombieRush

A simple PyGame game where player must kill waves of zombies before they kill them.

The essence of this game was to implement a set of different steering behaviours for AI agents. It was an assignment for a course realized in 2016 at faculty of Physics, Astronomy and Applied Computer Science of Jagiellonian University in Cracow.

---
## Assignemnt specification:

### Player:
- can mowe around game world with basic input WSAD
- can shoot a death ray with LMB
	- lenght of a death ray must be the diagonal of game display

### Zombies:
- for each wave spawn a bunch of zombie agens in random positions in game world
- they utilize following steering behaviours:
	- seek (for the Player when in rage)
	- flee (from the Player when in normal mood)
	- wandern (if the Player is far away)
	- avoid obstacles
	- avoid game world borders
	- hide (if the Player is chasing me)
- if X number of zombies gather around at the same time in one spot of specific range - trigger their RAGE
	- raged zombies will hunt the Player and try to kill them

### HUD:
- Player HP
- Player score
- number of current wave
- death ray indicator
- game menu
