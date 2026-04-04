from setuptools import setup, find_packages

setup(
    name="rustypycraw",
    version="0.1.0",
    description="RustyPyCraw - Hybrid code crawler",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    install_requires=["groq"],
)
