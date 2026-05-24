.PHONY: generate lint test clean coverage loadtest

generate:
	uv run antlr4 -Dlanguage=Python3 -visitor -no-listener -o src/dbms/generated grammar/SimpleSQL.g4
	@mv src/dbms/generated/grammar/* src/dbms/generated/ 2>/dev/null || true
	@rmdir src/dbms/generated/grammar 2>/dev/null || true

lint:
	uv run mypy src/dbms tests

test:
	uv run pytest -v

coverage:
	uv run coverage run -m pytest
	uv run coverage report
	uv run coverage html

loadtest:
	uv run python tests/load/test.py

clean:
	rm -rf src/dbms/generated/*.interp src/dbms/generated/*.tokens src/dbms/generated/__pycache__