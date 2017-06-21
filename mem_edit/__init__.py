"""
mem_edit

mem_edit is a multiplatform (Windows and Linux) python package for
  reading, writing, and searching in the working memory of running
  programs.

To get started, try:

    from mem_edit import Process
    help(Process)

"""
__author__ = 'Jan Petykiewicz'


import platform

from .utils import MemEditError


system = platform.system()
if system == 'Windows':
    from .windows import Process
elif system == 'Linux':
    from .linux import Process
else:
    raise MemEditError('Only Linux and Windows are currently supported.')
