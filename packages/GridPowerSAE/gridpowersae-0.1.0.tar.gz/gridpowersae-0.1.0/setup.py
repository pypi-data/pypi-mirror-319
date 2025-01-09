import os
import platform
from setuptools import setup, find_packages


if platform.system() != "Windows":
    raise OSError("This package can only be installed on Windows systems.")


class RunTestsCommand:
    """Пользовательская команда для запуска тестов"""
    
    def run(self):
        import unittest
        loader = unittest.TestLoader()
        tests = loader.discover('tests')
        runner = unittest.TextTestRunner()
        result = runner.run(tests)
        if not result.wasSuccessful():
            raise SystemExit(1)
        

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()


if os.path.exists("CHANGELOG.md"):
    with open("CHANGELOG.md", "r", encoding="utf-8") as f:
        long_description += "\n\n" + f.read()

setup(
    name='GridPowerSAE',
    version="0.1.0",
    description="Python-пакет для анализа электрической сети (ЕЭС ЭЭС) на ПВК RastrWin3",
    package_dir={},
    packages=find_packages(where='.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitverse.ru/Shurik412/GridPowerSAE",
    author="Shurik412",
    author_email="shurik412@mail.ru",
    license="GitVerse 1.0",
    entry_points={
            'console_scripts': [
                'run-tests-gridpowersae=tests.test_run_rastr_win:main',
            ],
        },
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
    ],
    platforms=['Windows'],
    install_requires=['PyRastrWin'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt'],
    },
    keywords=['PyRastrWin','RastrWin3', 'RastrWin', 'RUSTab', 'Rastr', 'rastr_win', 'rastr_win3', 'GridPowerSAE', 'GridPower'],
)
