#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rpg import Vampire, Weapon, Item

if __name__=='__main__':
	semi = Vampire(u'Semi', 'semi')
	
	# info
	semi.clan = 'Gangrel'
	semi.sire = u'Arinbjörn'
	semi.generation = 9
	semi.nature = 'Survivant'
	semi.demeanor = 'Bon vivant'
	semi.concept = 'Mercenaire'
	semi.player = 'Sulay'
	semi.chronicle = 'Orbe Noctis'
	semi.haven = 'Orbe Noctis'

	# attributes
	semi.strength = 4
	semi.dexterity = 5
	semi.stamina = 3
	semi.manipulation = 2
	semi.appearance = 2
	semi.charisma = 2
	semi.perception= 1
	semi.intelligence = 2
	semi.wits = 4

	# talents
	semi.alertness = 3
	semi.athletics = 3
	semi.brawl=3
	semi.subterfuge=3
	semi.dodge=1

	# skills
	semi.acting=1
	semi.etiquette=1
	semi.melee=1
	semi.stealth=3
	semi.survival=2
	semi.trade=1

	# knowledge
	semi.investigation=2
	semi.linguistics=1
	semi.medecine=1
	semi.scholarship=1

	# discipline
	semi.protean = 2
	semi.fortitude = 5
	semi.potence = 4

	# backgrounds
	semi.status = 2
	semi.generation_ = 2 # different from the actual Vampire generation (see info)
	semi.servants = 2
	semi.resources = 2

	# merits
	semi.conscience = 3
	semi.instinct = 3
	semi.courage = 4

	# flaws
	semi.flaws['Lucky'] = 2
	semi.flaws['Former Ghoul'] = 3
	semi.flaws['Sans reflet'] = -1
	semi.flaws['Weak Aura'] = -2
	semi.flaws[u"Allergie a l'ail"] = -1

	semi.roadName = 'Community'
	semi.roadValue = 5
	semi.willpower = 9

	# experience
	semi.exp = '4 (1 mat)'

	# equipment
	semi.weapons = [
		Weapon('P. Boucl.', '4', '4(par)', ''),
		Weapon('Dague', '4', '4(par)', 'un test'),
	]

	semi.armors = [
		Item('Cuir Leger', '3L/2C'),
	]

	# additional story file
	semi.story = 'semi.story.tex'

	# finally, render the latex code
	semi.render()

