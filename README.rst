pip-outdated
============

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

  usage: pip-outdated [-h] [-v] [<file> [<file> ...]]

  Find outdated dependencies in your requirements.txt or setup.cfg file.

  positional arguments:
    <file>         Read dependencies from requirements files. This option
                   accepts glob pattern. (default: ['requirements.txt',
                   'setup.cfg'])

  optional arguments:
    -h, --help     show this help message and exit
    -v, --verbose  Print verbose information. (default: False)
    
Check files under ``requirements`` folder::

  pip-outdated requirements/*.txt
  
Use glob pattern for ``dev/test-requirements``::

  pip-outdated *-requirements.txt
  
Todos
-----

* Add options to update the package?
* Add options to update the requirements.txt/setup.cfg file?
* Add options to list all packages? (e.g. ``-g, --global``)

Changelog
---------

* 0.1.0 (Next)

  - First release.

