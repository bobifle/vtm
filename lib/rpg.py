#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import logging
import re
import sys
import os
from collections import OrderedDict, namedtuple

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
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('lib', encoding='utf-8'))
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
		self.exp = ''

	@property
	def attributes(self): return [attr for attr in self._attributes] # a copy

	@property
	def data(self): return {'player': self}

	def render(self):
		env=getEnv()
		package = env.get_template('rpg.template')
		player = env.get_template('player.template')
		outdir = sys.argv[1] if len(sys.argv) > 1 else '.'
		# First render the package
		with open(os.path.join(outdir, '%s.sty' % self.fname), 'w') as f:
			f.write(package.render(**self.data).encode('utf-8'))
		# then the player tex file
		with open(os.path.join(outdir, '%s.tex' % self.fname), 'w') as f:
			f.write(player.render(**self.data).encode('utf-8'))

class Vampire(Player):
	_attributes = ['strength', 'dexterity', 'stamina', 'manipulation', 'appearance', 'charisma', 'perception', 'intelligence', 'wits']
	_talents = ['alertness', 'athletics', 'brawl', 'dodge', 'empathy', 'expression', 'intimidate', 'leadership', 'subterfuge', 'tricks']
	_skills = ['acting', 'animal', 'archery', 'craft', 'mounting', 'etiquette', 'melee', 'stealth', 'survival', 'trade']
	_knowledge = ['investigation', 'law', 'linguistics', 'medecine', 'occult', 'politics', 'seneschal', 'scholarship', 'streetwise', 'theology']
	_info = ['clan', 'sire', 'generation', 'nature', 'demeanor', 'concept', 'player', 'chronicle', 'haven']
	_disciplines = sorted(['animalism', 'celerity', 'fortitude', 'protean', 'potence', 'presence'])
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

	@property
	def powers(self):
		powers = []
		for discipline, _ in self.disciplines: 
			# add the scipline powers to the list
			# if the discpline is not described, add an Empty one
			if discipline: powers.extend(disc.get(discipline, DEmpty(discipline)).powers(self))
		return powers

	@property
	def blood_turn(self):
		"""Blood Point per turn"""
		return {9:2, 8:3, 7:4, 6:6, 5:8, 4:10}.get(self.generation, 1)

	@property
	def blood_pool(self): return {7:20, 6:30, 5:40, 4:50}.get(self.generation,13-self.generation+10)

	# will ease latex code a lot, blood pool is displayed as row of 10 squares
	def bp(self, row): 
		if self.blood_pool >= (row*10): return 10
		if self.blood_pool > (row-1)*10: return self.blood_pool%10
		return 0

# TODO use a class ?
Power = namedtuple('Power', ['name', 'level', 'dices', 'cost', 'diff', 'special'])

class Power(object):
	def __init__(self, name, level, dices, cost, diff, special):
		self.name = name; self.level = level ; self.dices = dices
		self.cost = cost; self.diff = diff ; self.special = special
		self.disc = None

class Discipline(object):
	def __init__(self, name, powers):
		self.name = name
		self._powers = powers
		for p in self._powers: p.disc = self

	def powers(self, player):
		pow =  [p for p in self._powers if p.level <= getattr(player, self.name, 0)]
		if len(pow) == 1:
			# discipline with only one power like potence have actually as many power as the player
			# score in the discipline
			pow[0].level = getattr(player, self.name, 1)
		return pow

class DEmpty(Discipline):
	def __init__(self, name):
		Discipline.__init__(self, name, [Power(name, 1, [], '', '', 'unkown implement me')])

disc = {}
disc['protean'] = Discipline('protean', [
		Power('Eyes of the beast', 1, [], '1 bp', '', 'can see in the dark'),
		Power('Feral Claw', 2, [], '1 bp, 1 turn', '', 'claws do str +1 aggravated damage'),
		Power('Earth Meld', 3, [], '', '', 'Melt into the earth to hide and rest'),
		Power('Shape of the Beast', 4, [], '', '', 'Transform into a specific animal'),
		Power('Mist Form', 5, [], '', '', 'Transform into a Mist'),
	])

disc['animalism'] = Discipline('animalism', [
	])

disc['celerity'] = Discipline('celerity', [
	Power('', 1, [], '1 bp per actions', '', 'Add an action in the turn'),
	])

disc['fortitude'] = Discipline('fortitude', [
	Power('', 1, [], '1 bp for auto succes', '', ''),
	])

disc['potence'] = Discipline('potence', [
	Power('', 1, [], '1 bp for auto succes', '', ''),
	])

