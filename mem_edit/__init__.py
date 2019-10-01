"""
mem_edit

mem_edit is a multi-platform (Windows and Linux) python package for
  reading, writing, and searching in the working memory of running
  programs.

To get started, try:

    from mem_edit import Process
    help(Process)

"""
import platform
import pathlib

from .utils import MemEditError


__author__ = 'Jan Petykiewicz'

with open(pathlib.Path(__file__).parent / 'VERSION', 'r') as f:
    __version__ = f.read().strip()
version = __version__


system = platform.system()
if system == 'Windows':
    from .windows import Process
elif system == 'Linux':
    from .linux import Process
else:
    raise MemEditError('Only Linux and Windows are currently supported.')
