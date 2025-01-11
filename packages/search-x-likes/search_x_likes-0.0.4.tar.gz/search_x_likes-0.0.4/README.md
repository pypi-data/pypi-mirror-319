# search-x-likes

[![Release](https://img.shields.io/github/v/release/cast42/search-x-likes)](https://img.shields.io/github/v/release/cast42/search-x-likes)
[![Build status](https://img.shields.io/github/actions/workflow/status/cast42/search-x-likes/main.yml?branch=main)](https://github.com/cast42/search-x-likes/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/cast42/search-x-likes/branch/main/graph/badge.svg)](https://codecov.io/gh/cast42/search-x-likes)
[![Commit activity](https://img.shields.io/github/commit-activity/m/cast42/search-x-likes)](https://img.shields.io/github/commit-activity/m/cast42/search-x-likes)
[![License](https://img.shields.io/github/license/cast42/search-x-likes)](https://img.shields.io/github/license/cast42/search-x-likes)

Search posts from x that have liked yourself using the archive download files

- **Github repository**: <https://github.com/cast42/search-x-likes/>
- **Documentation** <https://cast42.github.io/search-x-likes/>
- **Pypy package** <https://pypi.org/project/search-x-likes/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:cast42/search-x-likes.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

### 5. Set OPENAI_API_KEY key

```bash
export OPENAI_API_KEY=<your key>
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/cast42/search-x-likes/settings/secrets/actions/new).
- Create a [new release](https://github.com/cast42/search-x-likes/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).

## Development

Use `ruff` for linting and formatting, `mypy` for static code analysis, and `pytest` for testing.

The documentation is built with `mkdocs`, `mkdocs-material` and `mkdocstrings`.

## Contributing

All contributions are welcome, including more documentation, examples, code, and tests. Even questions.

## License - MIT

The package is open-sourced under the conditions of the [MIT license](https://choosealicense.com/licenses/mit/).

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
