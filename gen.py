#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import logging
import re
from collections import OrderedDict

_LATEX_SUBS = (
	(re.compile(r'\\'), r'\\textbackslash'),
	(re.compile(r'_'), r'\\textunderscore '),
	(re.compile(r'([{}_#%&$])'), r'\\\1'),
	(re.compile(r'~'), r'\~{}'),
	(re.compile(r'\^'), r'\^{}'),
	(re.compile(r'"'), r"''"),
	(re.compile(r'\.\.\.+'), r'\\ldots'),
)
_log = logging.getLogger(__name__)

# return a latex compatible jinja2 syntax
# basically replace { } by ()
def getEnv():
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
	env.block_start_string  = '((*'
	env.block_end_string = '*))'
	env.variable_start_string  = '((('
	env.variable_end_string = ')))'
	env.comment_start_string  = '((='
	env.comment_end_string = '=))'
	env.filters['tex'] = escape_tex
	env.filters['vars'] = vars
	return env

def escape_tex(value):
	"""Escape Tex special character in the given value."""
	if not value: # handles properly '' and None
		return ''
	newval = str(value)
	for pattern, replacement in _LATEX_SUBS:
		newval = pattern.sub(replacement, newval)
	return newval

class Item(object):
	def __init__(self, name, special):
		self.name = name
		self.special = special


class Weapon(Item):
	def __init__(self, name, diff, damage, special):
		Item.__init__(self, name, special)
		self.diff = diff
		self.damage = damage

class Player(object):
	def __init__(self, name, filename):
		self.name = name
		self.fname=filename
		self.story = None

	@property
	def attributes(self): return [attr for attr in self._attributes] # a copy

	@property
	def data(self): return {'player': self}

	def render(self):
		env=getEnv()
		package = env.get_template('rpg.template')
		player = env.get_template('player.template')
		# First render the package
		with open('%s.sty' % self.fname, 'w') as f:
			f.write(package.render(**self.data).encode('utf-8'))
		# then the player tex file
		with open('%s.tex' % self.fname, 'w') as f:
			f.write(player.render(**self.data).encode('utf-8'))

class Vampire(Player):
	_attributes = ['strength', 'dexterity', 'stamina', 'manipulation', 'appearance', 'charisma', 'perception', 'intelligence', 'wits']
	_talents = ['alertness', 'athletics', 'brawl', 'dodge', 'empathy', 'expression', 'intimidate', 'leadership', 'subterfuge', 'tricks']
	_skills = ['acting', 'animal', 'archery', 'craft', 'mounting', 'etiquette', 'melee', 'stealth', 'survival', 'trade']
	_knowledge = ['investigation', 'law', 'linguistics', 'medecine', 'occult', 'politics', 'seneschal', 'scholarship', 'streetwise', 'theology']
	_info = ['clan', 'sire', 'generation', 'nature', 'demeanor', 'concept', 'player', 'chronicle', 'haven']
	_disciplines = sorted(['animalism', 'celerity', 'fortitude', 'protean', 'potence'])
	_backgrounds = sorted(['status', 'generation_', 'servants', 'resources'])
	_merits = ['conscience', 'instinct', 'courage']
	
	def __init__(self, name, filename):
		Player.__init__(self, name, filename)
		self.flaws = {}
		self._weapons = []
		self._armors = []
		self._items = []

	# normalize a list to the given size, filling empty spaces with the given "empty" item
	def norm(self, alist, size, empty):
		ret = [ (item, getattr(self, item, 0)) for item in sorted(alist)]
		#always return size items, appending empty ones ('', 0), suitable for consitent display
		ret += [('', 0)]*(size-len(ret))
		return ret

	@property
	def info(self):
		return [(info, getattr(self, info, '')) for info in self._info]

	@property
	def physical(self): return [(attr, getattr(self, attr, 1)) for attr in self._attributes[:3]]

	@property
	def social(self): return [(attr, getattr(self, attr, 1)) for attr in self._attributes[3:6]]

	@property
	def mental(self): return [(attr, getattr(self, attr, 1)) for attr in self._attributes[6:9]]

	@property
	def attributes(self): return OrderedDict([('Physical', self.physical), ('Social', self.social), ('mental', self.mental)])

	@property
	def talents(self): return self.norm(self._talents, 11, ('', 0))

	@property
	def skills(self): return self.norm(self._skills, 11, ('', 0))

	@property
	def knowledge(self): return self.norm(self._knowledge, 11, ('', 0))

	@property
	def disciplines(self): return self.norm(self._disciplines, 6, ('', 0))

	@property
	def backgrounds(self): return [(i.strip('_'), v ) for i, v in self.norm(self._backgrounds, 6, ('', 0))]

	@property
	def merits(self): return self.norm(self._merits, 6, ('', 0))

	@property
	def abilities(self):
		ret = OrderedDict()
		ret['Talents'] = self.talents
		ret['Skills'] = self.skills
		ret['Knowledge'] = self.knowledge
		return ret

	@property
	def advantages(self):
		return OrderedDict([('Disciplines', self.disciplines), ('Backgrounds', self.backgrounds), ('Merits', self.merits)])

	@property
	def weapons(self): return self._weapons + [Weapon('','','','')]*(len(self._weapons)-5)

	@weapons.setter
	def weapons(self, value): self._weapons = value

	@property
	def armors(self): return self._armors + [Item('','')]*(len(self._armors)-3)

	@armors.setter
	def armors(self, value): self._armors = value


if __name__=='__main__':
	semi = Vampire(u'Semi', 'jmp')
	
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

	# equipment
	semi.weapons = [
		Weapon('P. Boucl.', '4', '4(par)', ''),
		Weapon('Dague', '4', '4(par)', 'un test'),
	]

	semi.armors = [
		Item('Cuir Leger', '3L/2C'),
	]

	# additional story file
	semi.story = 'jmp.story.tex'


	# finally, render the latex code
	semi.render()

