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
	def attributes(self):
		return [attr for attr in self._attributes] # a copy

	@property
	def data(self):
		d = {}
		d['attributes'] = [(attr[:3], attr.capitalize()) for attr in self.attributes]
		d['player'] = self
		return d

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


def attribute(attr):
	def decorator(cls):
		cls._attributes.append(attr)
		return cls
	return decorator

@attribute('strength')
@attribute('dexterity')
@attribute('stamina')
@attribute('manipulation')
@attribute('appearance')
@attribute('charisma')
@attribute('perception')
@attribute('intelligence')
@attribute('wits')
class Vampire(Player):
	_attributes = []
	_talents = ['alertness', 'athletics', 'brawl', 'dodge', 'empathy', 'expression', 'intimidate', 'leadership', 'subterfuge', 'tricks']
	_skills = ['acting', 'animal', 'archery']
	_knowledge = ['investigation', 'law']

	@property
	def talents(self): 
		# build the list of talents and their value, default to 0 
		ret = [ (talent, getattr(self, talent, 0)) for talent in sorted(self._talents)]
		#always return 12 talents, appending empty ones ('', 0), suitable for consitent display
		ret += [('', 0)]*(12-len(ret))
		return ret

	@property
	def skills(self):
		ret = [ (skill, getattr(self, skill, 0)) for skill in sorted(self._skills)]
		ret += [('', 0)]*(12-len(ret))
		return ret

	@property
	def knowledge(self):
		ret = [ (knowledge, getattr(self, knowledge, 0)) for knowledge in sorted(self._knowledge)]
		ret += [('', 0)]*(12-len(ret))
		return ret

	@property
	def abilities(self):
		ret = OrderedDict()
		ret['Talents'] = self.talents
		ret['Skills'] = self.skills
		ret['Knowledge'] = self.knowledge
		return ret


if __name__=='__main__':
	semi = Vampire(u'Semi', 'jmp')
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

	# knowledge
	semi.investigation=2

	# finally, render the latex code
	semi.render()

