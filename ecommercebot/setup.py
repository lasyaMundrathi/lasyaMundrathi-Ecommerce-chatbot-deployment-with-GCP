from setuptools import find_packages, setup
try:
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

setup(
    name="Ecommercebot",
    version="0.0.1",
    packages=find_packages(),
    author="Lasya Mundrathi",
    author_email="lasyamundrathi.1701@gmail.com",

    install_requires=requirements,
)
