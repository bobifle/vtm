import os
import logging

build = 'build'
src = 'src'

# that's the environment
env = Environment()

# before setting the VariantDir 
texlib = list(Glob('texlib/*'))

# copy all sources into the build directory
VariantDir(build, src)
Clean('.', build)
env['PDFLATEX'] = 'xelatex'
Export('env')

# generate tuple ('xxx.tex', 'xxx', 'tex') for all tex file in the repo 
texFiles = (f for f in Glob(build+'/**/*.tex') if "story" not in f.tpath)

for t in texFiles:
	pdf = env.PDF(os.path.splitext(t.path)[0]+'.pdf', source=t.path)
	env.AddPostAction(pdf, action = AlwaysBuild(env.PDF(os.path.splitext(t.path)[0]+'.pdf', source=t.path)))
	for tlib in texlib:
		target, source = os.path.join(t.path_elements[-2].path, tlib.name), tlib.path
		Requires(pdf, Command(target, source, Copy(target, source)))
		# objs = SConscript(os.path.join(t.path_elements[-2].path, 'sconscript'))
		# import IPython; IPython.core.debugger.Tracer()()

		# for obj in objs: Requires(obj, Command(target, source, Copy(target, source)))


