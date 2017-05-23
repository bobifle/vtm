import os
import logging
# that's the environment
env = Environment()
env['PDFLATEX'] = 'xelatex'
# generate tuple ('xxx.tex', 'xxx', 'tex') for all tex file in the repo 
texFiles = ((f.name,)+os.path.splitext(f.name) for f in Glob("*.tex") if "story" not in f.name)
projects = {}
clones = {}
for tfile, basename, ext in texFiles:
	projects[basename] = env.PDF(target=[basename+'.tmp.pdf'], source=[tfile])
	env.Alias(basename, tfile) # make xxx.tex available as rule xxx
	# the following lines handles the 2 successive compilations requires to handle proper pdf generation
	clones[basename] = env.Command(target=[basename+'.pdf'], source=[tfile], action='xelatex $SOURCES')
	Requires(clones[basename], projects[basename])

logging.warning("Found %d projects: %s" % (len(projects), projects.keys()))
