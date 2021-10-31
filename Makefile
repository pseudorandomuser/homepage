APP_PATH=./app

PYTHON_VER=python3.9
IGNORED_ERRORS=E128

VENV_PATH=./.venv
VENV=. ${VENV_PATH}/bin/activate

CONFIG_PATH=./config
ENVIRONMENTS_PATH=./config/environments
SECRETS_LENGTH=32
SECRETS_FILE=secrets.yaml
SECRETS_CMD="import secrets; print(f'SECRET_KEY: {secrets.token_hex(${SECRETS_LENGTH})}')"
SECRETS_DEV=${ENVIRONMENTS_PATH}/development/${SECRETS_FILE}
SECRETS_PROD=${ENVIRONMENTS_PATH}/production/${SECRETS_FILE}

.PHONY: deps
deps:
	${PYTHON_VER} -m venv ${VENV_PATH}
	${VENV} ; \
		if [ -f requirements.txt ]; then pip install -r requirements.txt ; fi ; \
		if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt ; fi

.PHONY: check
check: deps
	${VENV} ; pylint -Ev ${APP_PATH}
	${VENV} ; flake8 --ignore=${IGNORED_ERRORS} --show-source --statistics ${APP_PATH}
	${VENV} ; mypy --ignore-missing-import ${APP_PATH}

.PHONY: clean
clean:
	rm -rf "${VENV_PATH}"
	rm -rf "./.mypy_cache"
	find . -name ".DS_Store" -delete
	find . -name "${SECRETS_FILE}" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: setup
setup: deps
	${VENV} ; \
		if [ ! -f ${SECRETS_DEV} ]; then ${PYTHON_VER} -c ${SECRETS_CMD} > ${SECRETS_DEV} ; fi ; \
		if [ ! -f ${SECRETS_PROD} ]; then ${PYTHON_VER} -c ${SECRETS_CMD} > ${SECRETS_PROD} ; fi

.PHONY: run
run: setup
	${VENV} ; FLASK_ENV=development flask run --extra-files=${CONFIG_PATH}
