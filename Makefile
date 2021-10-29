APP_PATH=./app
VENV_PATH=./venv
PYTHON_PATH=python3

.PHONY: deps
deps:
	"${PYTHON_PATH}" -m venv "${VENV_PATH}"
	source "${VENV_PATH}/bin/activate" ; \
		pip install -r requirements.txt ; \
		pip install -r requirements-dev.txt

.PHONY: check
check: deps
	flake8 "${APP_PATH}" --show-source --statistics
	mypy --ignore-missing-import "${APP_PATH}"

.PHONY: clean
clean:
	rm -rf "${VENV_PATH}"
	rm -rf ./.mypy_cache
	find . -type d -name "__pycache__" -delete
