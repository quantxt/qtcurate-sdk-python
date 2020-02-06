from setuptools import setup
import io


def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(
    name="qtcurate",
    version="1.1.0",
    description="Theia SDK Search and Data Extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantxt/qtcurate-sdk-python",
    author="Milojko Bjelanovic",
    author_email="mbjelanovic@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["qtcurate"],
    include_package_data=True,
    install_requires=["requests"],
    python_requires=">=3.5",
    project_urls={
        'Bug Reports': 'support@quantxt.com',
        'Say Thanks!': 'http://quantxt.com',
        'Source': 'https://github.com/quantxt/qtcurate-sdk-python',
    }
)
