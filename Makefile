run: venv/bin/activate
	python3 main.py
setup: requirements.txt
	pip install -r requirements.txt
clean:
	rm -rf venv
	rm -rf __pycache__
