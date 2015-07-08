PYTHON=python
PYFLAKES=pyflakes

pep:
	pep8 app tests

flake:
	$(PYFLAKES) app tests

test: pep flake
	$(PYTHON) -m unittest discover -v $(FILTER)

run: 
	$(PYTHON) app/server.py
