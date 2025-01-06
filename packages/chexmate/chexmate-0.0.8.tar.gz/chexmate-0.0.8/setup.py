from setuptools import setup, find_packages


setup(
    name="chexmate",
    version="0.0.8",
    description="An (unofficial and incomplete) package used to integrate with the SeamlessChex API quickly and easily.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="William Hinz",
    author_email="faugermire@gmail.com",
    url="https://github.com/Faugermire/chexmate",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "setuptools~=75.6.0",
        "requests~=2.32.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',  # Developed using 3.12.5. Other python versions are not guaranteed to work.
)