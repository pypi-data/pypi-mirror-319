from setuptools import setup, find_packages

setup(
    name='chatollamaagent',
    version=open("version.txt").read(),
    author='Matthew Sanchez',
    author_email='',
    description='A visual node-based programming system for creating and managing agent-based workflows.',
    long_description=open('pypi_readme.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        "": ["**/*"],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'chatollama',
        'websockets',
    ],
)
