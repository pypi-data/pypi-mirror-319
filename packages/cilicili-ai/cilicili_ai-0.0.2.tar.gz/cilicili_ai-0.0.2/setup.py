from setuptools import setup, find_packages

setup(
    name="cilicili-ai",
    version="0.0.2",
    description="A task management decorator for Cilicili AI service.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Amiee",
    author_email="1223411083@qq.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
