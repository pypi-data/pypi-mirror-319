# Contributing

Anybody is welcome to submit bug reports and make feature requests. You are
also welcome submit pull requests (PRs) with new code to improve this package.
Below are some general guidelines for requesting changes or submitting a PR.


## Reporting Issues

If you encounter a problem or find a bug in this package, please open an Issue
on the
[GitHub Issues page](https://github.com/radioactivedecay/radioactivedecay/issues).

When submitting an Issue please state the version of ``radioactivedecay`` that
you are using, and include a minimal example of code or information which
demonstrates the problem.


## Requesting New Features

Anyone is welcome to suggest new features or ideas for this project. Please
start a new thread over on the
[Discussions](https://github.com/radioactivedecay/radioactivedecay/discussions)
page.


## Pull Requests

If you would like to contribute code, bug fixes or documentation improvements
to the project, please fork the GitHub repository, make your changes, then
submit a [Pull Request](https://github.com/radioactivedecay/radioactivedecay/pulls).

Below are the code standards used by this project. Note they are not rigid
requirements, but goals to aim for when submitting a PR. If you are not sure
how to do something, please feel free to contact one of the existing developers
for assistance.

The project uses GitHub Actions for CI/CD. Unit tests, code coverage reports,
Black code formatting checks, and documentation build checks are run
automatically on each PR. Check your GitHub notifications for the results!


### Code Formatting & Linting

The project uses [Black](https://black.readthedocs.io/en/stable/) to
standardize code formatting. Black is a command line utility that can be
installed via [pip](https://pypi.org/project/black/) or
[conda-forge](https://anaconda.org/conda-forge/black).

Please run ``black .`` from the base directory before making commits for PRs.
This will automatically format the code into a standard format.

[Pylint](https://www.pylint.org/) is used for basic error checking and
refactoring (installable from [pip](https://pypi.org/project/pylint/) or
[conda-forge](https://anaconda.org/conda-forge/pylint)). Run
``pylint radioactivedecay`` from the base directory and try to fix any new
warnings that are raised.

[isort](https://github.com/PyCQA/isort) is used to sort imports.


### Type Hints

This project requires Python 3.9+ and type hints are included in the headers of
all functions and methods exposed to users. Please add type hints for any new
functions you create.

Type hints are checked using [Mypy](http://mypy-lang.org/). Mypy is installable
via [pip](https://pypi.org/project/mypy/) or
[conda-forge](https://anaconda.org/conda-forge/mypy).

Run ``mypy radioactivedecay`` from the base directory. This currently raises a
number of errors. These can be ignored, but please aim to not increase the
error count with your changes. 😊


### Tests

The project uses Python's
[unittest](https://docs.python.org/3/library/unittest.html) framework for
testing. Please write unit tests for any new functionality you add. The
tests are stored in the
[tests](https://github.com/radioactivedecay/radioactivedecay/tree/main/tests)
sub-directory.

Run the tests by excecuting the command ``python -m unittest discover`` from
the base directory.


### Docstrings and Documentation

Documentation is handled via the
[README.md](https://github.com/radioactivedecay/radioactivedecay/blob/main/README.md)
file and the reStructuredText files in the
[docs/source](https://github.com/radioactivedecay/radioactivedecay/tree/main/docs/source/)
sub-directory. [Spinx](http://www.sphinx-doc.org/en/master/) is used for compiling the
docs (run ``make html`` from within the
[docs](https://github.com/radioactivedecay/radioactivedecay/tree/main/docs/)
 sub-directory).

Code docstrings follow the
[NumPy format](https://numpydoc.readthedocs.io/en/latest/format.html). Please
create new or update existing docstrings as appropriate. The doctrings are
automatically harvested by Sphinx to create the API section of the
[documentation](https://radioactivedecay.github.io/api.html).


## Release Guidelines

These notes describe the steps for cutting a new release:

* Update the version number in `radioactivedecay/__init__.py`
* Make sure
[CHANGELOG.md](https://github.com/radioactivedecay/radioactivedecay/blob/main/CHANGELOG.md)
documents the changes
* Create a new
[Release](https://github.com/radioactivedecay/radioactivedecay/releases)
on GitHub. CI/CD Actions workflows will automatically upload the new version to
[PyPI](https://pypi.org/project/radioactivedecay/) and
[conda-forge](https://anaconda.org/conda-forge/radioactivedecay).
