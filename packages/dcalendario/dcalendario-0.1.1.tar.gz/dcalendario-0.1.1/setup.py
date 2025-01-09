from setuptools import setup, find_packages

setup(
    name="dcalendario",
    version="0.1.1",
    author="Carlos Antonio",
    author_email="carlos22martinssilva@gmail.com",
    description="Pacote para gerar uma tabela dCalendário com Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CarlosEX/dCalendario",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "numpy"
    ],
)
