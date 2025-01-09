import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="rumoderatorai",
    version="0.1.0",
    author="PyWebSol",
    description="Библиотека для использования RuModeratorAI (https://moderator.pysols.ru)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://moderator.pysols.ru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["requests", "aiohttp", "Pillow", "boltons"],
)
