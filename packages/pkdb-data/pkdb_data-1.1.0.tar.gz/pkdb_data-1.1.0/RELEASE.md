# Release information

## Make release
* update release notes in `release-notes` with commit
* make sure all tests run (`tox -p`)
* check formating and linting (`ruff check`)
* test bump version (`uvx bump-my-version bump [major|minor|patch] --dry-run -vv`)
* bump version (`uvx bump-my-version bump [major|minor|patch]`)
* `git push --tags` (triggers release)
* `git push`
* merge devel branch on github
* test installation in virtualenv from pypi
```bash
uv venv --python 3.13
uv pip install pkdb_data
```
# Setup
## uv
```bash
uv sync
# install dev dependencies
uv pip install -r pyproject.toml --extra test
```

## Setup pre-commit
```bash
uvx pre-commit install
uvx pre-commit run
```

## Setup tox testing
See information on https://github.com/tox-dev/tox-uv
```bash
uv tool install tox --with tox-uv
```
Run single tox target
```bash
tox r -e py312
```
Run all tests in parallel
```bash
tox run-parallel
```
