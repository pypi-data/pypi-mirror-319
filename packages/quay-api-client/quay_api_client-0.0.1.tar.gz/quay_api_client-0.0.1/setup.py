from setuptools import setup, find_packages 

setup(
    name='quay-api-client',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author='Benjamin Ruland',
    author_email='benjamin.ruland@gmail.com',
    description='Quay API Client is a Python Client for the Red Hat Quay Container Registry',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/benruland/quay-python-client',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license_expression="Apache-2.0",
    python_requires='>=3.11',
)