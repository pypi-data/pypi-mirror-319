import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PepperPepper",
    version="0.0.9.4",
    python_requires='>=3.7',
    author="Aohua Li",
    author_email="liah24@mails.jlu.edu.cn",
    description="A Deep Learning package developed by Aohua Li. This release adds patch_embed for dicing operations prior to mamba input.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/username/PepperPepper",
    packages=setuptools.find_packages(),
    zip_safe=True,
    install_requires=[
        "numpy>=1.21.0",
        "torch>=1.10.0",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)