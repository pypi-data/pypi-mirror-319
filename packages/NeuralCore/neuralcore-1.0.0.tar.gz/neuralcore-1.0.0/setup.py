from setuptools import setup, find_packages

setup(
    name="neuralcore",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    author="NeuralCore",
    author_email="neuralcoreorganization@gmail.com",
    description="A Python client for NeuralCore AI API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://neuralcore.org",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)