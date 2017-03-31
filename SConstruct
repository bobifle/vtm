import os
import logging
# that's the environment
env = Environment()
# generate tuple ('xxx.tex', 'xxx', 'tex') for all tex file in the repo 
texFiles = ((f.name,)+os.path.splitext(f.name) for f in Glob("*.tex"))
projects = {}
for tfile, basename, ext in texFiles:
	projects[basename] = env.PDF(target=[basename+'.pdf'], source=[tfile])
	env.Alias(basename, tfile) # make xxx.tex available as rule xxx

logging.warning("Found %d projects: %s" % (len(projects), projects.keys()))
