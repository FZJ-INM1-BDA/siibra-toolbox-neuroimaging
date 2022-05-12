from setuptools import setup, find_packages
import os
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_version():
    path_to_init=os.path.join(ROOT_DIR, os.getenv("SIIBRA_TOOLBOX_SRC", "siibra_toolbox_template"), '__init__.py')
    with open(path_to_init, 'r', encoding="utf-8") as f:
        content=f.read()
        version_match=re.search(r"^__version__\W*?=\W*?['\"](.*?)['\"]$", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError('version cannot be found!')

with open(os.path.join(ROOT_DIR,"README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=os.getenv("SIIBRA_TOOLBOX_NAME", "siibra_toolbox_template"),
    version=find_version(),
    # author="Peter Smith",
    # author_email="peter@example.come",
    description="siibra-toolbox-template - A template for creating toolbox for siibra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/FZJ-INM1-BDA/siibra-toolbox-template",
    packages=find_packages(include=[ os.getenv("SIIBRA_TOOLBOX_SRC", "siibra_toolbox_template")]),
    # packages=find_packages(include=['.']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
    install_requires=['siibra>=0.3a17']
)

