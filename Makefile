APP_PATH=./app

PYTHON_VER=python3.10
IGNORED_ERRORS=E128
REQUIREMENTS=requirements.txt requirements-dev.txt

VENV_PATH=./.venv
VENV=. ${VENV_PATH}/bin/activate

ENVIRONMENTS=production development
ENVIRONMENTS_PATH=./config/environments

SECRETS_LENGTH=32
SECRETS_FILENAME=secrets.yaml
SECRETS_KEYS=SECRET_KEY SECRET_FLAG
SECRETS_CMD="import secrets; print(secrets.token_hex(${SECRETS_LENGTH}))"


.PHONY: deps
deps:
	${PYTHON_VER} -m venv ${VENV_PATH}
	@for REQUIREMENT in $(REQUIREMENTS) ; do \
		echo "Installing requirements from $$REQUIREMENT..." ; \
		${VENV} ; if [ -f $$REQUIREMENT ]; then \
			pip install -r $$REQUIREMENT ; \
		fi \
	done

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
	find . -name "${SECRETS_FILENAME}" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: setup
setup: deps
	@for ENVIRONMENT in $(ENVIRONMENTS) ; do \
		SECRETS_FILE=${ENVIRONMENTS_PATH}/$$ENVIRONMENT/${SECRETS_FILENAME} ; \
		if [ ! -f $$SECRETS_FILE ]; then \
			echo "Generating secrets: $$SECRETS_FILE" ; \
			for SECRET_KEY in $(SECRETS_KEYS) ; do \
				printf "$$SECRET_KEY: " >> $$SECRETS_FILE ; \
				${PYTHON_VER} -c ${SECRETS_CMD} >> $$SECRETS_FILE ; \
			done \
		fi \
	done

.PHONY: dev
dev: setup
	${VENV} ; FLASK_ENV=development flask run --extra-files=${CONFIG_PATH}