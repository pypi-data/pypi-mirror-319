from setuptools import setup, find_packages

# Read the dependencies from gerri/gerri/requirements.txt
with open("gerri/requirements.txt") as f:
    requirements = f.read().splitlines()

# Read README for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gerri",
    version="1.0.0",
    author="Kanav Kahol PhD",
    author_email="kanav.kahol@example.com",
    description="Giant Eagle Retrieval and Response Interface (Gerri) Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giant-eagle/Gerri_library",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
)
