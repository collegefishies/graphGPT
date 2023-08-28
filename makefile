auto:
	find . -name "*.py" | entr -r python main.py

docs:
	pdoc3 --html ./ --force --output-dir ./docs