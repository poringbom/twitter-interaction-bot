.PHONY: run clean pipinstall

run:
	python main.py

clean:
	rm -f log.txt

install:
	pip install -r requirements.txt
