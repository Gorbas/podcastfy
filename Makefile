lint:
	black podcastfy/*.py
	black tests/*.py
	mypy podcastfy/*.py

test:
	python3 -m pytest tests
    
doc-gen:
	sphinx-apidoc -f -o ./docs/source ./podcastfy
	(cd ./docs && make clean && make html)
	