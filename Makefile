APP_PATH=./app
VENV_PATH=./venv
PYTHON_PATH=python3.9
VENV=. ${VENV_PATH}/bin/activate

.PHONY: deps
deps:
	${PYTHON_PATH} -m venv ${VENV_PATH}
	${VENV} ; \
		pip install -r requirements.txt ; \
		pip install -r requirements-dev.txt

.PHONY: check
check: deps
	${VENV} ; pylint -Ev ${APP_PATH}
	${VENV} ; flake8 --show-source --statistics ${APP_PATH}
	${VENV} ; mypy --ignore-missing-import ${APP_PATH}

.PHONY: clean
clean:
	rm -rf ${VENV_PATH}
	rm -rf ./.mypy_cache
	find . -type d -name __pycache__ -delete
