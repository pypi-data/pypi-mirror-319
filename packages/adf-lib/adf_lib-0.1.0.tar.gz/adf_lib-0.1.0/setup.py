from setuptools import setup, find_packages

setup(
    name="adf-lib",
    version="0.1",
    package_dir={"adf_lib": "adf_lib"},
    packages=find_packages(where="adf_lib"),
    python_requires=">=3.8",
)