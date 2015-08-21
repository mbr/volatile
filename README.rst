temp
====

A replacement for ``tempfile.NamedTemporaryFile`` that does not delete the file
on ``close()``, but still unlinks it after the context manager ends.
