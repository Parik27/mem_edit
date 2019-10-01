#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('mem_edit/VERSION', 'r') as f:
    version = f.read().strip()

setup(name='mem_edit',
      version=version,
      description='Multi-platform library for memory editing',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Jan Petykiewicz',
      author_email='anewusername@gmail.com',
      url='https://mpxd.net/code/jan/mem_edit',
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
      package_data={
          'mem_edit': ['VERSION']
      },
      install_requires=[
            'typing',
      ],
      extras_require={
      },
      )

