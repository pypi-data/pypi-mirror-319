import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HITphysics_curve_fit_package",
    version="0.0",
    author="Shangjing Liu",
    author_email="2022110002@stu.hit.edu.cn",
    description="A self-used package for curve fitting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['torch', 'numpy', 'matplotlib', 'simpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
