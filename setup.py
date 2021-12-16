import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="o_re",
    version="0.0.1",
    author="Ilja Orlovs",
    author_email="vrghost@gmail.com",
    description="Objective regular expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VRGhost/objective_regex",
    project_urls={
        "Bug Tracker": "https://github.com/VRGhost/objective_regex/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)