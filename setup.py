from setuptools import setup, find_packages

setup(
    name="bitbucket_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "tabulate",
        "pyyaml",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "bitbucket_cli=bitbucket_cli.cli:main"
        ]
    },
)