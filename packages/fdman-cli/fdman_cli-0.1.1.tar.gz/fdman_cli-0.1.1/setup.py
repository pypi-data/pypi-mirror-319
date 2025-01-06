from setuptools import setup, find_packages


setup(
    name="fdman-cli",
    version="0.1.1",
    description="A CLI tool that manages files and directories.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ayoub A.",
    author_email="aberbach.me@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        "click",
        "colorama",
        "importlib-metadata; python_version < '3.12'",
    ],
    entry_points={
        "console_scripts": [
            "fdman = fdman.fdman:cli",
        ],
    },
    url="https://github.com/ayoub-aberbach/fdman",
)
