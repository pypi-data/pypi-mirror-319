import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animeworld",
    version="1.6.5",
    author="MainKronos",
    description="AnimeWorld UNOFFICIAL API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mainkronos.github.io/AnimeWorld-API/",
    packages=setuptools.find_packages(),
    install_requires=['httpx', 'httpx[http2]', 'youtube_dl', 'beautifulsoup4'],
	license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Topic :: Utilities",
    ],
    python_requires='>= 3.7',
)