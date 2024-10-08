from setuptools import setup, find_packages

setup(
    name='auto_reflection',
    version='0.1',
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'PyYAML',  # Do not include 'json'
        'pypubsub'
    ],
    entry_points={
        'console_scripts': [
            'blog_writer=auto_reflection.main:main',
        ],
    },
    package_data={
        '': ['config/*.yaml'],  # Add necessary YAML files
    },
    include_package_data=True,
    author='Your Name',
    description='A reflection-based blog-writing pipeline using YAML configs and mock data handling',
    url='https://github.com/your_username/auto_reflection',
)
