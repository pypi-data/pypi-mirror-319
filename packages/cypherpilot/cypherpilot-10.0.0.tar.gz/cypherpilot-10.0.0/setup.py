from setuptools import setup, find_packages

setup(
    name='cypherpilot',
    version='10.0.0',
    packages=find_packages(),
    install_requires=[
        'neo4j>=4.4.0',
    ],
    license='MIT',
    author='Yaki Naftali',
    author_email='yaki.naftali@accenture.com',
    description='Python Library for Database Interaction with Neo4j',
    long_description_content_type='text/markdown',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
],
)
