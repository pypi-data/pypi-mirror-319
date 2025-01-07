from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyRastrWin',
    version="0.1.1",
    description="Python-пакет для взаимодействия с RastrWin3",
    package_dir={"PyRastrWin": "PyRastrWin"},
    packages=find_packages(where='PyRastrWin'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitverse.ru/Shurik412/PyRastrWin",
    author="Shurik412",
    author_email="shurik412@mail.ru",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=['pywin32 >= 306'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
