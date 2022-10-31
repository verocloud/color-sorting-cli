#!  /bin/bash

./venv/bin/pip install mypy flake8 black isort
./venv/bin/mypy harmony
./venv/bin/flake8 harmony tests --max-line-length=88
./venv/bin/black harmony tests --check
./venv/bin/isort harmony tests --check-only --profile black