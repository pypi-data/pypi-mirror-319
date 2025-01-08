from setuptools import setup, find_packages
import platform

if platform.system() != "Windows":
    raise OSError("This package can only be installed on Windows systems.")


with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyRastrWin',
    version="0.1.3",
    description="Python-пакет для взаимодействия с RastrWin3",
    package_dir={},
    packages=find_packages(where='.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitverse.ru/Shurik412/PyRastrWin",
    author="Shurik412",
    author_email="shurik412@mail.ru",
    license="GitVerse 1.0",
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
    ],
    platforms=['Windows'],
    install_requires=['pywin32 >= 306'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    keywords=['PyRastrWin','RastrWin3', 'RastrWin', 'RUSTab', 'Rastr', 'rastr_win', 'rastr_win3'],
)
