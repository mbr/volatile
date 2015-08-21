volatile
========

A replacement for ``tempfile.NamedTemporaryFile`` that does not delete the file
on ``close()``, but still unlinks it after the context manager ends.

* Mostly reuses the stdlib implementation, supporting the same signatures.
* Due to that, uses the OS's built-in temporary file facilities, no custom
  schemes.
* Tested on Python 2.6+ and 3.3+


Usage
-----

A typical use-case that is not possible with the regular
``NamedTemporaryFile``:

.. code-block:: python

    import volatile

    with volatile.file() as tmp:
        # tmp behaves like a regular NamedTemporaryFile here, except for that
        # it gets unlinked at the end of the context manager, instead of when
        # close() is called.

        tmp.close()

        # run the users $EDITOR
        run_editor(tmp.name)

        buf = open(tmp.name).read()

        # ...
