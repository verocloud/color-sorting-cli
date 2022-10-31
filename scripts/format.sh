#! /bin/bash

./venv/bin/pip install autoflake black isort
./venv/bin/autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place harmony tests --exclude=__init__.py
./venv/bin/black harmony tests
./venv/bin/isort harmony tests --profile black