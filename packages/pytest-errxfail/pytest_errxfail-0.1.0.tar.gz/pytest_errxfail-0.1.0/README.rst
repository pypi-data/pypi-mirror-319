===============
pytest-errxfail
===============

.. image:: https://img.shields.io/pypi/v/pytest-errxfail.svg
    :target: https://pypi.org/project/pytest-errxfail
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-errxfail.svg
    :target: https://pypi.org/project/pytest-errxfail
    :alt: Python versions

.. image:: https://github.com/eltimen/pytest-errxfail/actions/workflows/main.yml/badge.svg
    :target: https://github.com/eltimen/pytest-errxfail/actions/workflows/main.yml
    :alt: See Build Status on GitHub Actions

----

A `pytest`_ plugin that adds the ``xfail_err`` marker to xfail a test that failed with the specified error message in the `captured`_ stdout, stderr or `log`_ output.

This plugin can be useful in the following cases:

* there are many tests failing due to sporadic problems (e.g., caused by an unstable network or sporadic crashes of a running third-party subprocess) and you want to save time analyzing test reports by splitting known flaky tests failures from meaningful software defects
* it is necessary to ensure that the original error in the test marked as xfail does not change in future revisions


Requirements
------------

* Python >= 3.8
* pytest >= 6.2.0


Installation
------------

::

    pip install pytest-errxfail


Usage
-----

Just add the ``xfail_err`` marker to the tests you need with the following arguments:

* positional argument with the error message pattern (can be also specified as the ``pattern`` kwarg)
* ``reason`` keyword argument - xfail reason (optional)
* ``matcher`` keyword argument - the type of message pattern matching (optional):

  * ``plain`` - simple substring search (default)
  * ``re`` - regular expression (with `re.MULTILINE`_ flag)
  * ``glob`` - Unix shell-style wildcard (via `fnmatch`_)

Example:

.. code-block:: python

    @pytest.mark.xfail_err('Error when downloading https://example.com/data* - connection refused',
                           matcher='glob', reason='unstable network')
    def test_download_file():
        run("echo 'Error when downloading https://example.com/data12 - connection refused' && exit 1",
            shell=True, check=True)


Output::

    $ pytest -v
    =============================== test session starts ================================
    platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0 -- /tmp/venv/bin/python3
    cachedir: .pytest_cache
    rootdir: /media/eltio/d893d5b1-92cd-4a48-a51e-7e94a871dbf1/repo/current/test_py
    plugins: errxfail-0.1.0
    collected 1 item

    test_demo.py::test_download_file XFAIL (unstable network)                    [100%]

    ================================ 1 xfailed in 0.03s ================================


Issues
------

If you encounter any problems, feel free to `file an issue`_ along with a detailed description and a minimal reproducible example.


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-errxfail" is free and open source software


.. _`MIT`: https://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/eltimen/pytest-errxfail/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`re.MULTILINE`: https://docs.python.org/3/library/re.html#re.MULTILINE
.. _`fnmatch`: https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch
.. _`captured`: https://docs.pytest.org/en/latest/how-to/capture-stdout-stderr.html
.. _`log`: https://docs.pytest.org/en/latest/how-to/logging.html
