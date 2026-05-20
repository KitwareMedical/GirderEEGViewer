# Contributing to GirderEEGViewer

1. Clone the repository using ``git clone``
2. Install the dev dependencies in your
   [dev environment](#install-and-run-in-development-mode)
3. Run ``pre-commit install`` to set up pre-commit hooks
4. Make changes to the code, and commit your changes to a separate branch
5. Create a fork of the repository on GitHub
6. Push your branch to your fork, and open a pull request

## Install and run in development mode

```
# Install project and each dependencies in editable mode in your environment
pip install -e ."[dev]"
```

## Commit messages

GirderEEGViewer follows trame\'s commit message convention to be compatible with
its CI features including the auto semantic release.

## Tips

1. When first creating a new project, it is helpful to run
   ``pre-commit run --all-files`` to ensure all files pass the pre-commit checks.
2. A quick way to fix ``black`` issues is by installing black
   (``pip install black``) and running the ``black`` command at the root of your
   repository.
4. A quick way to fix ``codespell`` issues is by installing codespell
   (``pip install codespell``) and running the ``codespell -w`` command at the root
   of your directory.
5. The
   [.codespellrc file](https://github.com/codespell-project/codespell#using-a-config-file)
   can be used fix any other codespell issues, such as ignoring certain files,
   directories, words, or regular expressions.
