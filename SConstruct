import os
import logging

build = 'build'
src = 'src'

# that's the environment
env = Environment(ENV={'PATH': os.environ['PATH']+r';C:\texlive\2016\bin\win32'}) if Platform().name == 'win32' else Environment()
env['ENV']['PYTHONPATH'] =  os.path.join(Dir('.').abspath, 'lib')

# before setting the VariantDir 
texlib = list(Glob('texlib/*'))

lib = list(Glob('lib/*'))

# img src
#imgSrc = list(Glob('src/*/*.jpg')) + list(Glob('src/*/*.png'))

# copy all sources into the build directory
#import pdb; pdb.set_trace()
VariantDir(build, src)

Clean('.', build)
env['PDFLATEX'] = 'xelatex'
Export('env')

pyFiles = Glob(build+'/**/*.py') 
for py in pyFiles:
	sources = Glob(os.path.split(py.path)[0]+'/*.jpeg')
	sources.append(py.path)
	env.Command(os.path.splitext(py.path)[0]+'.tex', sources, action="python %s %s" % (py.path, os.path.split(py.path)[0]))

texFiles = (f for f in Glob(build+'/**/*.tex') if "story" not in f.tpath)

for t in texFiles:
	pdf = env.PDF(os.path.splitext(t.path)[0]+'.pdf', source=t.path)
	for tlib in texlib:
		target, source = os.path.join(t.path_elements[-2].path, tlib.name), tlib.path
		Requires(pdf, Command(target, source, Copy(target, source)))


