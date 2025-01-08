from setuptools import setup, find_packages

setup(
    name="cafle",
    version="1.0.1",
    author="kphong",
    author_email="kphong16@daum.net",
    description="a cash flow estimating tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kphong16",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas>=2.0", 
        "numpy",
        "xlsxwriter"
    ]
)
