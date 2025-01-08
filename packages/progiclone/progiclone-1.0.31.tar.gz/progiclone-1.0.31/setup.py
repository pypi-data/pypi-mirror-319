# setup.py

from setuptools import setup, find_packages

setup(
    name="progiclone",
    version="1.0.31",
    author="VLTN x Progiseize",
    author_email="v.denis@progiseize.fr",
    description="Outil d'anonymisation des données sécurisé pour Dolibarr",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/valent1d/progiclone",
    packages=find_packages(),
    install_requires=[
        # Listez vos dépendances ici
        'pyfiglet',
        'tqdm',
        'Faker',
        'mysql-connector-python',
        'requests',
        'time',
        'os',
        'getpass',
        'sys',
        'subprocess',
        'logging',
        'argparse',
        'import_module',
        ],
    entry_points={
        "console_scripts": [
            "progiclone=progiclone.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
