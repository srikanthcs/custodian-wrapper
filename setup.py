# Automatically generated from poetry/pyproject.toml
# flake8: noqa
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custodian_v2']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete (>=1.12.1,<2.0.0)',
 'attrs (>=20.2.0,<21.0.0)',
 'boto3 (>=1.15.11,<2.0.0)',
 'botocore (>=1.18.11,<2.0.0)',
 'c7n (>=0.9.6,<0.10.0)',
 'click>=7.0,<8.0',
 'importlib-metadata (>=1.7.0,<2.0.0)',
 'jmespath (>=0.10.0,<0.11.0)',
 'jsonpickle (>=1.3,<2.0)',
 'jsonschema (>=3.2.0,<4.0.0)',
 'pyrsistent (>=0.17.3,<0.18.0)',
 'python-dateutil (>=2.8.1,<3.0.0)',
 'pyyaml (>=5.3.1,<6.0.0)',
 's3transfer (>=0.3.3,<0.4.0)',
 'six (>=1.15.0,<2.0.0)',
 'tabulate (>=0.8.7,<0.9.0)',
 'urllib3 (>=1.25.10,<2.0.0)',
 'zipp (>=3.3.0,<4.0.0)']

entry_points = \
{'console_scripts': ['custodian_v2 = custodian_v2.cli:main']}

setup_kwargs = {
    'name': 'custodian_v2',
    'version': '0.0.0',
    'description': 'Cloud Custodian - Custom version',
    'long_description': 'Cloud Custodian with custom actions',
    'long_description_content_type': 'text/markdown',
    'author': 'Cloud Custodian Project - Modified',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cloudcustodian.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
