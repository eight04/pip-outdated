pip-outdated
============

.. image:: https://travis-ci.com/eight04/pip-outdated.svg?branch=master
    :target: https://travis-ci.com/eight04/pip-outdated
    
.. image:: https://codecov.io/gh/eight04/pip-outdated/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/eight04/pip-outdated

Find outdated dependencies in your requirements.txt or setup.cfg file. Report missing/outdated/incompatible packages with table and colors.

This tool compares the version number with the version specifier in ``requirements.txt`` or ``setup.cfg``. If you just want to list all updatable package, simply use ``pip list --outdated`` command.

Installation
------------

From `pypi <https://pypi.org/project/pip-outdated/>`__

::

	pip install pip-outdated

Usage
-----

::

  usage: pip-outdated [-h] [-v] [-q] [<file> [<file> ...]]

  Find outdated dependencies in your requirements.txt or setup.cfg file.

  positional arguments:
    <file>         Read dependencies from requirements files. This option
                   accepts glob pattern. (default: ['requirements.txt',
                   'setup.cfg'])

  optional arguments:
    -h, --help     show this help message and exit
    -v, --verbose  Print verbose information. (default: False)
    -q, --quiet    Don't return exit code 1 if not everything is up to date.
                   (default: False)
    
Check multiple files e.g. ``test-requirements.txt`` and ``dev-requirements.txt``::

  pip-outdated *-requirements.txt
  
Check files under ``requirements`` folder::

  pip-outdated requirements/*.txt
  
Todos
-----

* Add options to update the package?
* Add options to update the requirements.txt/setup.cfg file?
* Add options to list all packages? (e.g. ``-g, --global``)

Changelog
---------

* 0.7.0 (Aug 13, 2024)

  - Change: ignore ``InvalidVersion`` error.

* 0.6.0 (Jan 1, 2023)

  - Bump dependencies.
  - Drop cchardet.
  - Change: fetch package version from ``pip`` CLI, so we can get package version in venv.

* 0.5.0 (Jan 12, 2022)

  - Bump dependencies.
  - Add: typehint.

* 0.4.0 (Jan 30, 2020)

  - **Breaking: bump Python to 3.7**
  - Add: request in parallel.
  - Add: ``--quiet`` option.

* 0.3.0 (Oct 13, 2019)

  - **Breaking: set exit code to 1 if not all good.**
  - Fix: don't check prereleases.
  - Add: check ``setup_requires`` and ``extras_require`` in cfg files.

* 0.2.0 (Feb 10, 2019)

  - Bump dependencies:
  
    - colorama@0.4.x
    - packaging@19.x
    - requests@2.x
    - termcolor@1.x
    - terminaltables@3.x

* 0.1.0 (May 12, 2018)

  - First release.

