import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyautd3",
    version="0.2.4",
    author="Shun Suzuki",
    author_email="suzuki@hapis.k.u-tokyo.ac.jp",
    description="AUTD3 library wrapper for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shinolab/pyautd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_dir={'pyautd3': 'pyautd'},
    packages=['pyautd3'],
    package_data={
        'pyautd3': ['*.dll'],
    },
    python_requires='>=3.6',
)
