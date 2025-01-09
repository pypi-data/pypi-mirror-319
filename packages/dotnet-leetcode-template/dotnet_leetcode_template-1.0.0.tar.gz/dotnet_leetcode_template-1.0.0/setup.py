# Importing the setup tools
from setuptools import setup, find_packages

# Defining the setup
setup(
    # Defining the name of the package
    name='dotnet-leetcode-template',
    # Defining the version of the package
    version='1.0.0',
    # Defining the author name
    author='Sasank Peetha',
    # Defining the dependencies
    install_requires=[],
    # Defining the email of the author
    author_email='sasank85@outlook.com',
    # Defining the description of the package
    description='Automation script to create a new LeetCode problem solutions in C#',
    # Defining the long description of the package
    long_description=open('README.md').read(),
    # Defining the content type of the long description
    long_description_content_type='text/markdown',
    # Defining the url of the package
    url='https://github.com/SasankPeetha8/Dotnet-Leetcode-Template',
    # Defining the classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
    ],
    # Defining the python version required
    python_requires='>=3.7',
    # Defining the dependencies
    project_urls={
        # Adding link to .NET installation page
        'Dotnet Dependency': 'https://dotnet.microsoft.com/',
    },
    # Defining the entry points
    entry_points={
        'console_scripts': [
            'dotnet-leetcode-template=Dotnet_Leetcode_Template.Dotnet_Leetcode_Template_Script:main',
        ],
    },
)