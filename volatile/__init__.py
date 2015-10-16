from contextlib import contextmanager
from errno import ENOENT
import os
import shutil
import socket
import tempfile


@contextmanager
def dir(*args, **kwargs):
    name = tempfile.mkdtemp(*args, **kwargs)

    yield name

    try:
        shutil.rmtree(name)
    except OSError as e:
        if e.errno != 2:  # not found
            raise


@contextmanager
def file(*args, **kwargs):
    ignore_missing = kwargs.pop('ignore_missing', False)

    fp = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
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

        yield sock, addr

        if close:
            sock.close()
