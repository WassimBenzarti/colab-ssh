from pathlib import Path

def render_template(filename, params):
	with open(f"{Path(__file__).resolve().parent}/{filename}") as f:
		template = f.read()
		return template.format(**params)