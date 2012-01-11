from distutils.core import setup, Command
from distutils.command.build import build as _build
import os, sys
import shutil

class build(_build):
  sub_commands = _build.sub_commands + [('build_server', lambda self: True)]

class build_server(Command):
  description = 'custom build command'
  user_options = []

  def initialize_options(self):
    self.cwd = None
  def finalize_options(self):
    self.cwd = os.getcwd()
  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root.'
    os.system('qmake && make')
    try:
      os.remove('build/lib/webkit_server')
    except: pass
    shutil.move('src/webkit_server', 'build/lib')

setup(name='webkit-server',
      version='0.8',
      description='a Webkit-based, headless browser instance',
      author='Niklas Baumstark',
      author_email='niklas.baumstark@gmail.com',
      license='MIT',
      url='https://github.com/niklasb/webkit-server',
      py_modules=['webkit_server'],
      cmdclass={
        'build': build,
        'build_server': build_server,
        })
