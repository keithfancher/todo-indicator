#!/usr/bin/env python


from distutils.core import setup


setup(name='todo_indicator',
      version='0.1.0-dev',
      description='Ubuntu app indicator for todo.txt-style todo lists',
      author='Keith Fancher',
      author_email='keith.fancher@gmail.com',
      url='https://github.com/keithfancher/Todo-Indicator',
      scripts=['todo_indicator.py'],
      install_requires=[
          'argparse',
          'pyinotify'
      ]
)
