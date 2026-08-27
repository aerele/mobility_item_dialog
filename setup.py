import re
import ast
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mobility_advanced_item_dialog/__init__.py
with open("mobility_advanced_item_dialog/__init__.py") as f:
	for line in f:
		match = re.match(r"^__version__\s*=\s*(.+)$", line)
		if match:
			version = ast.literal_eval(match.group(1))
			break

setup(
	name="mobility_advanced_item_dialog",
	version=version,
	description="Mobility-Advanced-Item-Dialog",
	author="Aerele Technologies",
	author_email="hello@aerele.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
