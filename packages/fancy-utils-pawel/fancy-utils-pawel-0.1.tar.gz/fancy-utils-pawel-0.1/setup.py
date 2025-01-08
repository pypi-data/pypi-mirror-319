from setuptools import setup, find_packages




setup(
    name="fancy-utils-pawel",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy"],
    description="A fancy utility library for string and array operations",
    author="Pasha",
    author_email="pawelstasinskiuk@gmail.com",
    url="https://github.com/your_github/fancy-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
