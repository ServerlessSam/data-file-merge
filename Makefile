lint:
	poetry run black .
	poetry run isort .
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive .
	poetry run flake8 .
lint-check:
	poetry run black --check .
	poetry run isort --check .
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive --check .
	poetry run flake8 .
