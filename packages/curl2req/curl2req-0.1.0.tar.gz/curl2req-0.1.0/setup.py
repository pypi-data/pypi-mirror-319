from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='curl2req',
    version='0.1.1',
    author='weiz',
    author_email='azhao.1981@gmail.com',
    description='bash curl transfer to requests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/azhao1981/curl2req',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'pydantic',
        'jsonpath_ng',
        "requires-python",
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'sphinx',
        ]
    },
)
