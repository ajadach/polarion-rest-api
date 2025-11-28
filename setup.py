"""
Setup configuration for polarion-rest-api package.
"""
from setuptools import setup, find_packages

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='polarion-rest-api',
    version='0.1.0',
    author='Artur Ziolkowski',
    author_email='artur.k.ziolkowski@gmail.com',
    description='Python client library for Polarion REST API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ajadach/polarion-rest-api',
    packages=['polarion_rest_api', 'polarion_rest_api.modules'],
    package_dir={'polarion_rest_api': 'polarion_rest_api'},
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.25.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.12.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='polarion rest api client',
)
