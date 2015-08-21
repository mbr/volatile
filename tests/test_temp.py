import os

from temp import NamedTemporaryFile
import pytest


def test_ntf_simple_persistance():
    with NamedTemporaryFile() as tmp:
        assert os.path.exists(tmp.name)
        tmp.close()
        assert os.path.exists(tmp.name)

    assert not os.path.exists(tmp.name)


def test_keeps_content():
    with NamedTemporaryFile() as tmp:
        tmp.write(b'foo')
        tmp.close()

        assert b'foo' == open(tmp.name, 'rb').read()


def test_unlink_raises():
    with pytest.raises(OSError):
        with NamedTemporaryFile() as tmp:
            os.unlink(tmp.name)


def test_can_ignore_missing():
    with NamedTemporaryFile(ignore_missing=True) as tmp:
        os.unlink(tmp.name)
