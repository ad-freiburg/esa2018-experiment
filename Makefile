all: compile test checkstyle

compile:
	python3 -m py_compile *.py
test:
	python3 -m doctest *.py

checkstyle:
	flake8 *.py

clean:
	rm -f test.tsv
	rm -rf __pycache__
	rm -rf tmp
