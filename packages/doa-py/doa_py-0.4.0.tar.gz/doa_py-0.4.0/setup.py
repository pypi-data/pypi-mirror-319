from setuptools import find_packages, setup


def find_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def find_version():
    with open("doa_py/__init__.py", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split()[-1][1:-1]
    return ""


setup(
    name="doa_py",
    version=find_version(),
    packages=find_packages(),
    description="DOA estimation algorithms implemented in Python",
    author="Qian Xu",
    author_email="xuq3196@outlook.com",
    url="https://github.com/zhiim/doa_py",
    long_description=find_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=["numpy", "matplotlib", "scipy", "scikit-image", "cvxpy"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
