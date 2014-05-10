from distutils.core import setup, Command
from distutils.command.build import build as _build
import os, sys
import shutil

class build_server(_build):
  description = 'custom build command'
  sub_commands = []

  def initialize_options(self):
    _build.initialize_options(self)
    self.cwd = None
  def finalize_options(self):
    _build.finalize_options(self)
    self.cwd = os.getcwd()
  def run(self):
    if os.environ.get('READTHEDOCS', None) == 'True':
      # won't build on readthedocs.org
      return
    assert os.getcwd() == self.cwd, 'Must be in package root.'
    os.system('qmake && make')
    try:
      os.remove(os.path.join(self.build_purelib, 'webkit_server'))
    except: pass      
    try:
      os.remove(os.path.join(self.build_platlib, 'webkit_server'))
    except: pass
    try:
      os.makedirs(self.build_platlib)
    except: pass
    try:
      os.makedirs(self.build_purelib)
    except: pass
    shutil.copy('src/webkit_server', self.build_purelib)
    shutil.copy('src/webkit_server', self.build_platlib)

setup(name='webkit-server',
      version='0.9',
      description='a Webkit-based, headless browser instance',
      author='Niklas Baumstark',
      author_email='niklas.baumstark@gmail.com',
      license='MIT',
      url='https://github.com/niklasb/webkit-server',
      py_modules=['webkit_server'],
      cmdclass={
        'build': build_server,
        })
