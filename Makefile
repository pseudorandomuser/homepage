FLASK_APP=homepage
PREFIX ?= .

PYTHON_VER=python3.9
IGNORED_ERRORS=E128
REQUIREMENTS=requirements.txt requirements-dev.txt

VENV_PATH=.venv
VENV=. ${VENV_PATH}/bin/activate

ENVIRONMENTS=production development
ENVIRONMENTS_PATH=instance

SECRETS_LENGTH=32
SECRETS_FILENAME=secrets.yaml
SECRETS_KEYS=SECRET_KEY SECRET_FLAG
SECRETS_CMD="import secrets; print(secrets.token_hex(${SECRETS_LENGTH}))"


.PHONY: deps
deps: ${VENV_PATH}/.deps
${VENV_PATH}/.deps:
	${PYTHON_VER} -m venv ${VENV_PATH}
	@for REQUIREMENT in $(REQUIREMENTS) ; do \
		echo "Installing requirements from $$REQUIREMENT..." ; \
		if [ -f $$REQUIREMENT ]; then \
			${VENV} ; pip install -r $$REQUIREMENT ; \
		fi \
	done
	@touch "${@}"

.PHONY: check
check: deps
	${VENV} ; pylint -Ev ${FLASK_APP}
	${VENV} ; flake8 --ignore=${IGNORED_ERRORS} --show-source --statistics ${FLASK_APP}
	${VENV} ; mypy --ignore-missing-import ${FLASK_APP}

.PHONY: build
build: deps
	${VENV} ; ${PYTHON_VER} setup.py bdist_wheel

.PHONY: install
install: deploy-artifacts secrets

.PHONY: deploy-artifacts
deploy-artifacts:
	mkdir -p ${PREFIX}
	rsync -rlptv ./instance ${PREFIX}
	${PYTHON_VER} -m venv ${PREFIX}/${VENV_PATH}
	. ${PREFIX}/${VENV_PATH}/bin/activate ; \
		pip install --force-reinstall ./dist/*.whl

.PHONY: clean
clean:
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./*.egg-info
	rm -rf ./.mypy_cache
	rm -rf ${VENV_PATH}
	find . -name ".DS_Store" -delete
	find . -name "${SECRETS_FILENAME}" -delete
	find . -type d -name "__pycache__" -exec rm -rfv {} \;

.PHONY: setup
setup: deps secrets

.PHONY: secrets
secrets:
	@for ENVIRONMENT in $(ENVIRONMENTS) ; do \
		SECRETS_FILE=${PREFIX}/${ENVIRONMENTS_PATH}/$$ENVIRONMENT/${SECRETS_FILENAME} ; \
		if [ ! -f $$SECRETS_FILE ]; then \
			echo "Generating secrets: $$SECRETS_FILE" ; \
			for SECRET_KEY in $(SECRETS_KEYS) ; do \
				printf "$$SECRET_KEY: " >> $$SECRETS_FILE ; \
				. ${PREFIX}/${VENV_PATH}/bin/activate ; \
					${PYTHON_VER} -c ${SECRETS_CMD} >> $$SECRETS_FILE ; \
			done \
		fi \
	done

.PHONY: dev
dev: setup
	${VENV} ; FLASK_ENV=development FLASK_APP=${FLASK_APP} flask run --extra-files=${CONFIG_PATH}