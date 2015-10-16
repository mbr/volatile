import os

import pytest
import volatile


def test_ntf_simple_persistance():
    with volatile.file() as tmp:
        assert os.path.exists(tmp.name)
        tmp.close()
        assert os.path.exists(tmp.name)

    assert not os.path.exists(tmp.name)


def test_keeps_content():
    with volatile.file() as tmp:
        tmp.write(b'foo')
        tmp.close()

        assert b'foo' == open(tmp.name, 'rb').read()


def test_unlink_raises():
    with pytest.raises(OSError):
        with volatile.file() as tmp:
            os.unlink(tmp.name)


def test_can_ignore_missing():
    with volatile.file(ignore_missing=True) as tmp:
        os.unlink(tmp.name)


def test_temp_dir():
    with volatile.dir() as dtmp:
        assert os.path.exists(dtmp)
        assert os.path.isdir(dtmp)

    assert not os.path.exists(dtmp)


def test_can_remove_dir_without_error():
    with volatile.dir() as dtmp:
        os.rmdir(dtmp)


def test_socket():
    with volatile.unix_socket() as (sock, addr):
        assert hasattr(sock, 'close')
        assert os.path.exists(addr)

    assert not os.path.exists(addr)


def test_file_cleanup_after_exception():
    try:
        with volatile.file() as tmp:
            name = tmp.name
            assert os.path.exists(name)
            raise RuntimeError()
            pass
    except RuntimeError:
        print 'caught runtime error'

    assert not os.path.exists(name)


def test_dir_cleanup_after_exception():
    try:
        with volatile.dir() as dtmp:
            name = dtmp
            assert os.path.exists(name)
            raise RuntimeError()
            pass
    except RuntimeError:
        print 'caught runtime error'

    assert not os.path.exists(name)


def test_socket_cleanup_after_exception():
    try:
        with volatile.unix_socket() as (_, addr):
            name = addr
            assert os.path.exists(name)
            raise RuntimeError()
            pass
    except RuntimeError:
        print 'caught runtime error'

    assert not os.path.exists(name)
