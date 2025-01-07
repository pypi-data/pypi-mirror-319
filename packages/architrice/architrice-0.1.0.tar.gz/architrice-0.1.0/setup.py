import setuptools

with open("architrice/__init__.py", "r") as f:
    for line in f:
        if "__version__" in line:
            version = line.split("=")[1].strip().replace('"', "")

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="architrice",
    version=version,
    url="https://github.com/OwenFeik/architrice.git",
    author="Owen Feik",
    author_email="owen.h.feik@gmail.com",
    description="Utility to sync MtG decklists with online sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    download_url="https://github.com/OwenFeik/architrice/archive/refs/tags/0.1.0.tar.gz",
    install_requires=["requests", "bs4"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7",
)
