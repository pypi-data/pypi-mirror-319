from setuptools import setup, find_packages

# Leer el contenido de el archivo README.md

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="consolepy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Ángel David Vásquez Pedrozo",
    description="Una biblioteca para mostrar los mensajes por consola de una forma más estética",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
