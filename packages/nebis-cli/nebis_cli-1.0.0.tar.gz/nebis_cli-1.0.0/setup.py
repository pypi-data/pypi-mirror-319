from setuptools import setup, find_packages

setup(
    name='nebis-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',  
    ],
    entry_points={
        'console_scripts': [
            'nebis=nebis.cli:main', 
        ],
    },
    author='Livrädo Sandoval',
    author_email='livrasand@outlook.com',
    description='A CLI tool for managing Nebis databases.',
    url='https://github.com/livrasand/nebis-cli',  
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
