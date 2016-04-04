from contextlib import contextmanager
from errno import ENOENT
import os
import shutil
import socket
import tempfile


@contextmanager
def dir(suffix='', prefix='tmp', dir=None):
    name = tempfile.mkdtemp(suffix, prefix, dir)

    try:
        yield name
    finally:
        try:
            shutil.rmtree(name)
        except OSError as e:
            if e.errno != 2:  # not found
                raise


@contextmanager
def file(mode='w+b', suffix='', prefix='tmp', dir=None, ignore_missing=False):
    # note: bufsize is not supported in Python3, try to prevent problems
    #       stemming from incorrect api usage
    if isinstance(suffix, int):
        raise ValueError('Passed an integer as suffix. Did you want to '
                         'specify the deprecated parameter `bufsize`?')

    fp = tempfile.NamedTemporaryFile(mode=mode,
                                     suffix=suffix,
                                     prefix=prefix,
                                     dir=dir,
                                     delete=False)
    try:
        yield fp
    finally:
        try:
            os.unlink(fp.name)
        except OSError as e:
            # if the file does not exist anymore, ignore
            if e.errno != ENOENT or ignore_missing is False:
                raise


@contextmanager
def unix_socket(sock=None, socket_name='tmp.socket', close=True):
    sock = sock or socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    with dir() as dtmp:
        addr = os.path.join(dtmp, socket_name)
        sock.bind(addr)

        try:
            yield sock, addr
        finally:
            if close:
                sock.close()
