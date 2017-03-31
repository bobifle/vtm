import re
import os

# that's the environment
env = Environment()

# there's a bug where acronyms building will be triggered when matching glossaries
# make sure acronyms are not triggered
from SCons.Tool import tex
tex.makeacronyms_re=re.compile(r"^[^%\n]*\\DO_NOT_FIND_ME", re.MULTILINE)

packages = [p.name for p in Glob("*.sty")]

texFiles = Glob("*.tex")
t0 = texFiles[-1]
projects = {}
for tfile in texFiles:
	basename = os.path.splitext(tfile.name)[0]
	builder = env.PDF(target=[basename+'.pdf'], source=[tfile])
	# the late builder does no implicitly search for cls dependencies
	# add dependencies to packages and the class file
	Depends(builder, packages)
	classFile = basename+'.cls'
	if os.path.isfile(basename+'.cls'):	Depends(builder, classFile)
	projects[basename] = builder
	env.Alias(basename, tfile) # make xxx.tex available as rule xxx
