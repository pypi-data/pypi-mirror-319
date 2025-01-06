from setuptools import setup, find_packages

setup(
    name="markdown-importer",
    version="1.0.0",
    author="VirtualExecutive",
    description="Markdown dosyalarını modüler bir şekilde yönetmenizi sağlayan araç",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VirtualExecutive/Markdown-Importer",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "markdown-importer=markdown_importer.__main__:main",
        ],
    },
    install_requires=[],
) 