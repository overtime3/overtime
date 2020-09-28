import setuptools

version = "v0.0.1"
long_description = "An open-source library, for the analysis and visualization of temporal networks."

setuptools.setup(
    name="overtime",
    version=version,
    author="Seán O'Callaghan",
    author_email="soca.mailbox@gmail.com",
    description="An open-source temporal networks library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/overtime3/overtime/",
    download_url = 'https://github.com/overtime3/overtime/archive/'+ version + '.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'imageio>=2.9.0',
        'matplotlib>=3.3.0',
        'networkx>=2.4',
        'numpy>=1.19.0',
        'pandas>=1.1.0',
        'requests==2.24.0',
    ],
)
