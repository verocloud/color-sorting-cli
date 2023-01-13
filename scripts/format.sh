#! /bin/bash

./venv/bin/pip install ruff black isort
./venv/bin/ruff harmony tests --fix
./venv/bin/black harmony tests
./venv/bin/isort harmony tests --profile black