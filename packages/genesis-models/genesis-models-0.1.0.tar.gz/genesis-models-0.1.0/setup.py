# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['genesis_models']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'genesis-models',
    'version': '0.1.0',
    'description': 'Shared database models for Genesis services',
    'long_description': None,
    'author': 'stevenge',
    'author_email': 'stevenge@godscode.com.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
