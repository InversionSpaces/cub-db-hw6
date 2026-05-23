.PHONY: generate lint test clean

generate:
	java -jar antlr4-tool.jar -Dlanguage=Python3 -visitor -no-listener -o src/dbms/generated grammar/SimpleSQL.g4
	@mv src/dbms/generated/grammar/* src/dbms/generated/ 2>/dev/null || true
	@rmdir src/dbms/generated/grammar 2>/dev/null || true

lint:
	uv run mypy src/dbms tests

test:
	uv run pytest -v

clean:
	rm -f antlr4-tool.jar
	rm -rf src/dbms/generated/*.interp src/dbms/generated/*.tokens src/dbms/generated/__pycache__