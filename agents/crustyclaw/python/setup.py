from setuptools import setup, find_packages

setup(
    name="crustyclaw",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "crustyclaw=crustyclaw.main:main",
        ],
    },
)
