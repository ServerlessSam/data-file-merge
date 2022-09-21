format:
	poetry run black .
	poetry run isort .
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive .
	poetry run flake8 .
format-check:
	poetry run black --check .
	poetry run isort --check .
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive --check .
	poetry run flake8 .
create-cli:
	poetry run pyinstaller src/cli.py --onefile --name dfm