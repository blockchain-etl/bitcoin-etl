import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='bitcoin-etl',
    version='1.0.0',
    author='Omidiora Samuel',
    author_email='samparsky@gmail.com',
    description='Tools for exporting Bitcoin blockchain data to CSV or JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blockchain-etl/bitcoiin-etl',
    packages=find_packages(exclude=['schemas', 'tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='bitcoin',
    python_requires='>=3.5.3,<3.8.0',
    install_requires=[
        'python-dateutil==2.7.0',
        'click==6.7',
        'python-bitcoinrpc==1.0'
    ],
    extras_require={
        'dev': [
            'pytest~=3.2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'bitcoinetl=bitcoinetl.cli:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/blockchain-etl/bitcoin-etl/issues',
        'Chat': 'https://gitter.im/bitcoin-etl/Lobby',
        'Source': 'https://github.com/blockchain-etl/bitcoin-etl',
    },
)
