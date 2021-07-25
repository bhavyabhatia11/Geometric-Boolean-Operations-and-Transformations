import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gbot",
    version="0.0.1",
    author="Bhavya Bhatia",
    author_email="bhavya2603@gmail.com",
    description="A set of functions to perform Geometric Boolean Operations and Tranformations(GBOT) ",
    long_description="This is a compiled package of the assignments given as part of the course ME/MF F342 Computer Aided Design, this package is useful in performing 3D projective tranformations on numpy matrices and also performing geometric boolean operations like intersection union and difference on polygons.",
    long_description_content_type="text/markdown",
    url="https://github.com/bhvya2603/Geometric-Boolean-Operations-and-Transformations",
    project_urls={
        "Bug Tracker": "https://github.com/bhvya2603/Geometric-Boolean-Operations-and-Transformations/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)