from setuptools import setup, find_packages

setup(
    name="boat_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "structlog",
        "prometheus-client",
    ],
) 