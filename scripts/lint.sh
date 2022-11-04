#!  /bin/bash

./venv/bin/pip install mypy pylint flake8 black isort
./venv/bin/mypy harmony
./venv/bin/pylint harmony --disable=C0114,C0209,R0903
./venv/bin/flake8 harmony tests --max-line-length=88
./venv/bin/black harmony tests --check
./venv/bin/isort harmony tests --check-only --profile black