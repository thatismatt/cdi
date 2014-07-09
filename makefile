.PHONY: test bootstrap

test:
	sh -c '. _virtualenv/bin/activate; nosetests'

bootstrap: _virtualenv
ifneq ($(wildcard test-requirements.txt),)
	_virtualenv/bin/pip install -r test-requirements.txt
endif

_virtualenv:
	virtualenv _virtualenv
	_virtualenv/bin/pip install --upgrade pip
	_virtualenv/bin/pip install --upgrade setuptools
