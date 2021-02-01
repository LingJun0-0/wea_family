# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import versioneer

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('HISTORY.md', encoding='utf-8') as f:
    history = f.read()


requirements = [
    'flask',
    'pandas',
    'numpy',
    'gunicorn',
    'pyyaml',
    'rqdatac',
    'rqdatac_bond',
    'rqams-utils',
]

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='ricequant assets management',
    long_description=readme + '\n\n' + history,
    author='Ricequant',
    author_email='public@ricequant.com',
    keywords='wea_family',
    url='https://www.ricequant.com/',
    include_package_data=True,
    packages=find_packages(include=['wea_family', 'wea_family.*']),
    install_requires=requirements,
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    zip_safe=False,
)
