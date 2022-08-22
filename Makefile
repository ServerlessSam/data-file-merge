lint:
	poetry run black .
	poetry run isort .
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive .
	poetry run flake8 .
