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

class Player(object):
	def __init__(self, name, filename):
		self.name = name
		self.fname=filename

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
			f.write(package.render(**self.data))
		# then the player tex file
		with open('%s.tex' % self.fname, 'w') as f:
			f.write(player.render(**self.data))

class Vampire(Player):
	_attributes = ['strength', 'dexterity', 'stamina', 'manipulation', 'appearance', 'charisma', 'perception', 'intelligence', 'wits']
	_talents = ['alertness', 'athletics', 'brawl', 'dodge', 'empathy', 'expression', 'intimidate', 'leadership', 'subterfuge', 'tricks']
	_skills = ['acting', 'animal', 'archery', 'craft', 'mounting', 'etiquette', 'melee', 'stealth', 'survival', 'trade']
	_knowledge = ['investigation', 'law', 'linguistics', 'medecine', 'occult', 'politics', 'seneschal', 'scholarship', 'streetwise', 'theology']
	_info = ['clan', 'sire', 'generation', 'nature', 'demeanor', 'concept', 'player', 'chronicle', 'haven']
	_disciplines = sorted(['animalism', 'celerity', 'fortitude', 'protean', 'potence'])

	def items(self, alist):
		ret = [ (item, getattr(self, item, 0)) for item in sorted(alist)]
		#always return 11 items, appending empty ones ('', 0), suitable for consitent display
		ret += [('', 0)]*(11-len(ret))
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
	def talents(self): return self.items(self._talents)

	@property
	def skills(self): return self.items(self._skills)

	@property
	def knowledge(self): return self.items(self._knowledge)

	@property
	def disciplines(self): return [(item, getattr(self, item)) for item in self._disciplines if hasattr(self, item)]

	@property
	def abilities(self):
		ret = OrderedDict()
		ret['Talents'] = self.talents
		ret['Skills'] = self.skills
		ret['Knowledge'] = self.knowledge
		return ret

	@property
	def advantages(self):
		return OrderedDict([('Disciplines', self.disciplines)])


if __name__=='__main__':
	semi = Vampire(u'Semi', 'jmp')
	
	# info
	semi.clan = 'Gangrel'
	semi.sire = u'Arinbjorn'
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

	# finally, render the latex code
	semi.render()

