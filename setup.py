#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mem_edit',
      version='0.1',
      description='Multi-platform library for memory editing',
      author='Jan Petykiewicz',
      author_email='anewusername@gmail.com',
      url='https://mpxd.net/gogs/jan/mem_edit',
      keywords=[
            'memory',
            'edit',
            'editing',
            'ReadProcessMemory',
            'WriteProcessMemory',
            'proc',
            'mem',
            'ptrace',
            'multiplatform',
            'scan',
            'scanner',
            'search',
            'debug',
            'cheat',
            'trainer',
      ],
      classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Topic :: Software Development',
            'Topic :: Software Development :: Debuggers',
            'Topic :: Software Development :: Testing',
            'Topic :: System',
            'Topic :: Games/Entertainment',
            'Topic :: Utilities',
      ],
      packages=find_packages(),
      install_requires=[
            'ctypes',
            'typing',
      ],
      extras_require={
      },
      )

