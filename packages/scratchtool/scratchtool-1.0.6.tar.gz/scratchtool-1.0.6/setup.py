from setuptools import setup, find_packages

#python setup.py sdist bdist_wheel
#python -m twine upload dist/*


setup(
    name='scratchtool',
    version='1.0.6',
    author="itijiku",
    author_email="kanjukuitijuku@gmail.com",
    description="A package for working with Scratch data.",
    url="https://github.com/itijuku/scratchtool",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.3',
        'asyncio',
        'websockets',
        'json'
    ],
    entry_points={
        'console_scripts': [
            'scratchtool=scratchtool.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
