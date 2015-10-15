from contextlib import contextmanager
from errno import ENOENT
import os
import shutil
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
