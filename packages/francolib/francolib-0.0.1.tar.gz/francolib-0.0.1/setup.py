from setuptools import setup, find_packages

setup(
    name="francolib",               # Nome del pacchetto su PyPI
    version="0.0.1",                # Versione del pacchetto
    packages=["francolib"],         # Nome del modulo esplicito
    package_dir={"francolib": "francolib"},  # Mapping chiaro
    install_requires=[              # Dipendenze
        "nptdms",                   # Libreria per leggere file TDMS
        "matplotlib",               # Libreria per i grafici
        "pandas",                   # Libreria per la gestione dei dati
        "numpy",
        "scipy"                     # Libreria per l'analisi dei dati
    ],
    author="Franco De Angelis",
    author_email="fd23111991@gmail.com",
    description="Libreria per gestire TDMS e grafici",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/libfranco/",  # URL del progetto (es. GitHub)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
