"""
Implementation of Process class for Linux
"""

from typing import List, Tuple
from os import strerror
import os
import os.path
import signal
import ctypes
import ctypes.util
import logging

from .abstract import Process as AbstractProcess
from .utils import ctypes_buffer_t, MemEditError


logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)


ptrace_commands = {
        'PTRACE_GETREGS': 12,
        'PTRACE_SETREGS': 13,
        'PTRACE_ATTACH': 16,
        'PTRACE_DETACH': 17,
        'PTRACE_SYSCALL': 24,
        'PTRACE_SEIZE': 16902,
        }


# import ptrace() from libc
_libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
_ptrace = _libc.ptrace
_ptrace.argtypes = (ctypes.c_ulong,) * 4
_ptrace.restype = ctypes.c_long


def ptrace(command: int, pid: int = 0, arg1: int = 0, arg2: int = 0) -> int:
    """
    Call ptrace() with the provided pid and arguments. See the ```man ptrace```.
    """
    logger.debug('ptrace({}, {}, {}, {})'.format(command, pid, arg1, arg2))
    result = _ptrace(command, pid, arg1, arg2)
    if result == -1:
        err_no = ctypes.get_errno()
        if err_no:
            raise MemEditError('ptrace({}, {}, {}, {})'.format(command, pid, arg1, arg2) +
                               ' failed with error {}: {}'.format(err_no, strerror(err_no)))
    return result


class iovec(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p),
                ("iov_len", ctypes.c_size_t)]

class Process(AbstractProcess):
    pid = None

    def __init__(self, process_id: int):
        self.pid = process_id

    def close(self):
        self.pid = None

    def write_memory(self, base_address: int, write_buffer: ctypes_buffer_t):

        _libc.process_vm_readv(
            self.pid,
            (iovec * 1)(
                iovec(ctypes.addressof(write_buffer), ctypes.sizeof(write_buffer))
            ),
            1,
            (iovec * 1)(iovec(base_address, ctypes.sizeof(write_buffer))),
            1,
            0
        )

    def read_memory(self, base_address: int, read_buffer: ctypes_buffer_t) -> ctypes_buffer_t:

        _libc.process_vm_readv(
            self.pid,
            (iovec * 1)(
                iovec(ctypes.addressof(read_buffer), ctypes.sizeof(read_buffer))
            ),
            1,
            (iovec * 1)(iovec(base_address, ctypes.sizeof(read_buffer))),
            1,
            0
        )
        
        return read_buffer

    def get_path(self) -> str:
        try:
            with open('/proc/{}/cmdline', 'rb') as f:
                return f.read().decode().split('\x00')[0]
        except FileNotFoundError:
            return ''

    @staticmethod
    def list_available_pids() -> List[int]:
        pids = []
        for pid_str in os.listdir('/proc'):
            try:
                pids.append(int(pid_str))
            except ValueError:
                continue
        return pids

    @staticmethod
    def get_pid_by_name(target_name: str) -> int or None:
        for pid in Process.list_available_pids():
            try:
                logger.info('Checking name for pid {}'.format(pid))
                with open('/proc/{}/cmdline'.format(pid), 'rb') as cmdline:
                    path = cmdline.read().decode().split('\x00')[0]
            except FileNotFoundError:
                continue

            name = os.path.basename(path)
            logger.info('Name was "{}"'.format(name))
            if path is not None and name == target_name:
                return pid

        logger.info('Found no process with name {}'.format(target_name))
        return None

    def list_mapped_regions_by_name(self,
                                    writeable_only=True,
                                    name=None,
                                    include_anons=True) -> List[Tuple[int, int]]:
        regions = []
        with open('/proc/{}/maps'.format(self.pid), 'r') as maps:
            for line in maps:

                bounds, privileges = line.split()[0:2]
                
                if (not include_anons or name is not None) and len(line.split()) < 6:
                    continue

                _name = os.path.basename(''.join(line.split()[5:]))
                print(_name == name)
                if name is not None and _name != name:
                    continue
                
                if 'r' not in privileges:
                    continue

                if writeable_only and 'w' not in privileges:
                    continue

                start, stop = (int(bound, 16) for bound in bounds.split('-'))
                regions.append((start, stop))
        return regions
