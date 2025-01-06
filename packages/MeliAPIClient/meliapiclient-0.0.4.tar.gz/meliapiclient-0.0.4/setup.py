from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.4'
DESCRIPTION = 'Este paquete nos permite consumir el API de mercado libre'
PACKAGE_NAME = 'MeliAPIClient'
AUTHOR = 'Camilo Andrés Rodríguez Higuera'
EMAIL = 'hola@camilordz.com'
GITHUB_URL = 'https://github.com/andresroh/MeliAPIClient'

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    keywords=['python', 'mercado libre', 'mercadolibre.com'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
