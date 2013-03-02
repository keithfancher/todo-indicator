#!/usr/bin/env python


from distutils.core import setup


setup(name='todo_indicator',
      version='0.3.0',
      description='Ubuntu app indicator for todo.txt-style todo lists',
      author='Keith Fancher',
      author_email='keith.fancher@gmail.com',
      license='GPLv3',
      url='https://github.com/keithfancher/Todo-Indicator',
      scripts=['todo_indicator.py'],
      install_requires=[
          'argparse',
          'pyinotify'
      ]
)
